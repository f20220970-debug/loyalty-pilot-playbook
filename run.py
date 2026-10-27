"""Run the loyalty analysis on the Instacart data and write results/ plus the pilot tracker.

    python run.py --data ../qcommerce-retention-sql/data
"""
import argparse
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent


def connect(data: Path):
    con = duckdb.connect()
    p = lambda f: (data / f).as_posix()
    con.execute(f"CREATE VIEW orders AS SELECT * FROM read_csv_auto('{p('orders.csv')}') WHERE eval_set IN ('prior','train')")
    con.execute(f"""CREATE VIEW order_items AS SELECT * FROM read_csv_auto('{p('order_products__prior.csv')}')
                    UNION ALL SELECT * FROM read_csv_auto('{p('order_products__train.csv')}')""")
    con.execute(f"CREATE VIEW products AS SELECT * FROM read_csv_auto('{p('products.csv')}')")
    con.execute(f"CREATE VIEW departments AS SELECT * FROM read_csv_auto('{p('departments.csv')}')")
    return con


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default=str(ROOT / "data")); a = ap.parse_args()
    con = connect(Path(a.data))
    (ROOT / "results").mkdir(exist_ok=True)
    out = {}
    for f in sorted((ROOT / "sql").glob("*.sql")):
        df = con.execute(f.read_text()).df(); out[f.stem] = df
        (df.head(2000) if f.stem.startswith("03") else df).to_csv(ROOT / "results" / f"{f.stem}.csv", index=False)
        print(f"\n=== {f.stem} ({len(df):,} rows) ===\n{df.head(8).to_string(index=False)}")
    seg = out["01_loyal_segments"].set_index("segment")
    coh = out["03_pilot_cohort"]
    top = out["02_what_champions_value"].iloc[0]
    ch = seg.loc["Champions"]
    lines = ["# Results summary", "",
             f"- Champions (30+ orders, ordering about weekly) are {100 * ch.share_of_customers:.1f}% of customers but place {100 * ch.share_of_orders:.1f}% of orders.",
             f"- Their biggest department is {top.department} ({100 * top.champions_share_of_items:.0f}% of their items, reorder rate {100 * top.champions_reorder_rate:.0f}%).",
             f"- Pilot cohort: {len(coh):,} Champions with a personal hero product; test {int((coh.arm == 'test').sum()):,} / control {int((coh.arm == 'control').sum()):,}."]
    (ROOT / "results" / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    main()

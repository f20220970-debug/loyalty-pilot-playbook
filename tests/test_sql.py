from pathlib import Path

import duckdb
import pytest

SQL = Path(__file__).resolve().parents[1] / "sql"


@pytest.fixture
def con():
    c = duckdb.connect()
    rows = []
    oid = 0
    for uid, n, gap in [(1, 40, 7.0), (2, 20, 10.0), (3, 5, 30.0)]:
        for k in range(1, n + 1):
            oid += 1
            rows.append((oid, uid, "prior", k, None if k == 1 else gap))
    c.execute("CREATE TABLE orders(order_id INT, user_id INT, eval_set VARCHAR, order_number INT, days_since_prior_order DOUBLE)")
    c.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
    c.execute("CREATE TABLE products AS SELECT * FROM (VALUES (1,'Milk',1,1),(2,'Chips',2,2)) t(product_id,product_name,aisle_id,department_id)")
    c.execute("CREATE TABLE departments AS SELECT * FROM (VALUES (1,'dairy eggs'),(2,'snacks')) t(department_id,department)")
    c.execute("""CREATE TABLE order_items AS
        SELECT order_id, CASE WHEN user_id = 1 THEN 1 ELSE 2 END AS product_id, 1 AS add_to_cart_order, 1 AS reordered FROM orders""")
    return c


def run(con, f):
    return con.execute((SQL / f).read_text()).df()


def test_segments(con):
    s = run(con, "01_loyal_segments.sql").set_index("segment")
    assert s.loc["Champions", "customers"] == 1 and s.loc["Regulars", "customers"] == 1
    assert s["share_of_orders"].sum() == pytest.approx(1.0, abs=1e-3)


def test_champions_value_dairy(con):
    v = run(con, "02_what_champions_value.sql")
    assert v.iloc[0]["department"] == "dairy eggs"


def test_cohort_has_hero_product(con):
    c = run(con, "03_pilot_cohort.sql")
    assert len(c) == 1 and c.iloc[0]["hero_product"] == "Milk" and c.iloc[0]["arm"] in ("test", "control")

# Loyalty Pilot Playbook: finding the most loyal customers and testing a surprise-and-delight pilot

How a quick-commerce team can find its most loyal customers in SQL, learn what they value, and run a small,
measurable surprise-and-delight pilot with a clear **scale, fix or stop** decision. Customer data comes from the
public Instacart dataset (3.4M orders, 206K customers).

## Key results
- **Champions** (30+ orders, ordering about weekly) are 11.7% of customers but place 38.3% of orders: median 48 orders, every 6 days.
- They lean towards fresh food: produce is 30% of their items (78% reorder rate) and dairy & eggs 18% (80%), the categories a quality-first grocer leads with.
- All 24,077 Champions have a personal hero product (e.g. almond milk, kombucha, coconut water), so a gesture can be personal at scale; the stable hash split gives 12,039 test vs 12,038 control.
- The plan pilots 200 + 200 first (about ₹50K), with orders per customer over 8 weeks as the primary metric and a scale / fix / stop rule in the tracker.

## What's inside
| Step | File | What it does |
| --- | --- | --- |
| 1. Find the loyal core | `sql/01_loyal_segments.sql` | Segments customers into Champions (30+ orders, weekly), Regulars and Occasional, with their share of orders |
| 2. Learn what they value | `sql/02_what_champions_value.sql` | Champions' top departments and reorder rates vs everyone else |
| 3. Build the cohort | `sql/03_pilot_cohort.sql` | Each Champion's personal "hero product" and a stable 50/50 test/control split |
| 4. Plan the pilot | [`docs/pilot_plan.md`](docs/pilot_plan.md) | Goal, gesture, budget, owners, timeline, metrics, guardrails and the decision rule |
| 5. Run and decide | [`pilot_tracker.xlsx`](pilot_tracker.xlsx) | Daily ops log and a results sheet that calculates lift, cost per incremental order and the scale / fix / stop call |

## Why a control group
Champions already order often, so "they ordered a lot after the gift" proves nothing on its own. Only the
difference against similar Champions who got nothing shows whether the gesture worked.

## Run it
```bash
pip install -r requirements.txt
pytest -q
python run.py --data PATH/TO/instacart/csvs
```

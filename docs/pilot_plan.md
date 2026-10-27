# Pilot plan: "Your favourites, noticed", a surprise-and-delight pilot for Champions

**Goal.** Find out whether a small, personal gesture to the most loyal customers makes them order more and talk
about the brand, at a cost that pays back.

**Who.** Champions: customers with 30+ orders who order about weekly (see `results/01_loyal_segments.csv`).
They are a small share of customers but a large share of orders, so keeping them matters most.

**The gesture.** With their next order, a handwritten note and a premium version of their personal *hero product*
(the item they reorder most, from `results/03_pilot_cohort.csv`), for example a new artisanal milk for a customer
whose hero product is milk. Personal, about food they already love, and in line with a quality-first brand.

**Design.**
| Item | Plan |
| --- | --- |
| Test vs control | Champions split 50/50 at random (stable hash of customer ID). Test gets the gesture; control gets nothing. |
| Size | Start with 200 test + 200 control in one city for 2 weeks of gestures, then 8 weeks of measurement. |
| Budget | About ₹250 per gesture (item + note + packing time): about ₹50,000 for 200 customers. |
| Owner and teams | Pilot owner (intern); ops for packing and delivery; vendor for the premium items; CX for reactions. |
| Timeline | Week 0 setup and vendor sourcing; weeks 1-2 gestures sent; weeks 3-10 measurement; week 11 readout. |

**Metrics.**
- **Primary:** orders per customer in the 8 weeks after the gesture, test vs control.
- **Secondary:** share of customers still ordering weekly at week 8; average order value; reactions (calls,
  messages, social posts) per 100 gestures; whether customers buy the premium item afterwards.
- **Guardrails:** cost per gesture within budget; delivery errors or delays caused by the extra packing step.

**Decision rule.**
- **Scale** if test orders are at least 5% higher than control *and* the extra gross margin covers the gesture cost.
- **Fix** if reactions are strong but the order lift is small (try a different gesture or moment, e.g. a milestone order).
- **Stop** if neither orders nor reactions move.

**Caveats.** 200 per arm detects only fairly large lifts; treat the first round as directional and run a second,
larger round before rolling out. Champions already order often, so look at the difference against control, never at
test customers alone.

**Tracker.** `pilot_tracker.xlsx`: daily operations log (gestures packed, delivered, reactions, cost) and a results
sheet that computes lift, cost per incremental order and the scale/fix/stop call from the entered numbers.

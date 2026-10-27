"""Build pilot_tracker.xlsx: a daily ops log and a results sheet with live formulas."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
log = wb.active; log.title = "Daily log"
head = ["Date", "Gestures packed", "Delivered", "Delivery issues", "Reactions (calls/msgs/posts)", "Cost (₹)", "Cumulative cost (₹)", "Notes"]
for i, h in enumerate(head, 1):
    c = log.cell(1, i, h); c.font = Font(bold=True, color="FFFFFF", name="Arial"); c.fill = PatternFill("solid", fgColor="2C7A7B")
for r in range(2, 32):
    log.cell(r, 7, f"=IF(F{r}=\"\",\"\",SUM($F$2:F{r}))")
for col, w in zip("ABCDEFGH", [12, 16, 11, 15, 26, 11, 20, 40]):
    log.column_dimensions[col].width = w

res = wb.create_sheet("Results")
blue = Font(color="0000FF", name="Arial")
rows = [
    ("Inputs (enter after 8 weeks)", None, None),
    ("Test customers", 200, "count"), ("Control customers", 200, "count"),
    ("Test orders in 8 weeks", None, "total"), ("Control orders in 8 weeks", None, "total"),
    ("Total gesture cost (₹)", "='Daily log'!G31", "from log (or type a number)"),
    ("Gross margin per order (₹)", 120, "assumption"),
    ("Lift threshold to scale", 0.05, "5%"),
    ("", None, None),
    ("Outputs", None, None),
    ("Orders per test customer", "=IF(B4=\"\",\"\",B4/B2)", ""),
    ("Orders per control customer", "=IF(B5=\"\",\"\",B5/B3)", ""),
    ("Lift (test vs control)", "=IF(OR(B11=\"\",B12=0),\"\",B11/B12-1)", ""),
    ("Incremental orders", "=IF(B11=\"\",\"\",(B11-B12)*B2)", ""),
    ("Extra gross margin (₹)", "=IF(B14=\"\",\"\",B14*B7)", ""),
    ("Cost per incremental order (₹)", "=IF(OR(B14=\"\",B14<=0),\"n/a\",B6/B14)", ""),
    ("Decision", "=IF(B13=\"\",\"enter results\",IF(AND(B13>=B8,B15>=B6),\"SCALE\",IF(B13>0,\"FIX\",\"STOP\")))", "scale if lift ≥ threshold and margin covers cost"),
]
for i, (a, b, c) in enumerate(rows, 1):
    res.cell(i, 1, a).font = Font(bold=a in ("Inputs (enter after 8 weeks)", "Outputs", "Decision"), name="Arial")
    if b is not None:
        cell = res.cell(i, 2, b)
        if not str(b).startswith("="):
            cell.font = blue
    res.cell(i, 3, c)
res["B13"].number_format = "0.0%"; res["B8"].number_format = "0%"
for col, w in zip("ABC", [34, 18, 44]):
    res.column_dimensions[col].width = w
wb.save("pilot_tracker.xlsx"); print("saved pilot_tracker.xlsx")

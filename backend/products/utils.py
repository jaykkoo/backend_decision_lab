from openpyxl import Workbook
from django.http import HttpResponse


def export_product_views_excel(result: dict) -> HttpResponse:
    wb = Workbook()

    # ---------------------------
    # Sheet 1 — Top views
    # ---------------------------
    ws_views = wb.active
    ws_views.title = "Top Viewed Products"

    ws_views.append(["Product ID", "Views"])

    for r in sorted(
        result["views_by_product"],
        key=lambda x: x["views"],
        reverse=True,
    ):
        ws_views.append([r["product_id"], r["views"]])

    # ---------------------------
    # Sheet 2 — Avg age
    # ---------------------------
    ws_age = wb.create_sheet("Average Age")

    ws_age.append(["Product ID", "Average Age"])

    for r in sorted(
        result["views_by_product"],
        key=lambda x: x["average_age"],
    ):
        ws_age.append([
            r["product_id"],
            round(r["average_age"], 1),
        ])

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )
    response["Content-Disposition"] = (
        'attachment; filename="product_views.xlsx"'
    )

    wb.save(response)
    return response

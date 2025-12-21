from flask import Blueprint, render_template, current_app
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)

# ---- 1 PREDEFINED QUERY ----
QUERY = """SELECT 
    venture_id "Venture ID",

    total_amount_received_from_that_party "Total Amount Received from that Party",

    expected_material_expense "Expected Sitewise Material Expense",
    actual_sitewise_material_expense "Actual Sitewise Material Expense",
    supplier_difference "Sitewise Supplier Balance",
    expected_sitewise_labour_expense "Expected Sitewise Labour Expense",
    actual_sitewise_actual_labour_expense "Actual Sitewise Actual Labour Expense",
    contractor_difference "Sitewise Contractor Balance"
FROM (
    SELECT 
        actual_supplier.venture_id AS venture_id,

        expected_supplier.total_amount AS total_amount_received_from_that_party,      

        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        (expected_supplier.supplier_total - actual_supplier.supplier_total)
            AS supplier_difference,

        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        (expected_contractor.contractor_total - actual_contractor.contractor_total)
            AS contractor_difference

    FROM 
        (SELECT venture_id, SUM(total_amount) AS total_amount, SUM(expected_material_expense) AS supplier_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_supplier

    INNER JOIN
        (SELECT venture_id, SUM(total_amount) AS supplier_total
         FROM outbound_payments
         WHERE supplier_id IS NOT NULL
         GROUP BY venture_id) AS actual_supplier
    ON actual_supplier.venture_id = expected_supplier.venture_id

    INNER JOIN
        (SELECT venture_id,SUM(expected_labour_expense) AS contractor_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_contractor
    ON expected_contractor.venture_id = expected_supplier.venture_id

    INNER JOIN
        (SELECT venture_id, SUM(total_amount) AS contractor_total
         FROM outbound_payments
         WHERE contractor_id IS NOT NULL
         GROUP BY venture_id) AS actual_contractor
    ON actual_contractor.venture_id = expected_supplier.venture_id
)

UNION ALL

SELECT
    'TOTAL',
    SUM(total_amount_received_from_that_party),
    SUM(expected_material_expense),
    SUM(actual_sitewise_material_expense),
    SUM(supplier_difference),
    SUM(expected_sitewise_labour_expense),
    SUM(actual_sitewise_actual_labour_expense),
    SUM(contractor_difference)
FROM (
    SELECT 

        expected_contractor.total_amount AS total_amount_received_from_that_party, 

        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        (expected_supplier.supplier_total - actual_supplier.supplier_total)
            AS supplier_difference,

        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        (expected_contractor.contractor_total - actual_contractor.contractor_total)
            AS contractor_difference

    FROM 
        (SELECT venture_id, SUM(expected_material_expense) AS supplier_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_supplier

    INNER JOIN
        (SELECT venture_id, SUM(total_amount) AS supplier_total
         FROM outbound_payments
         WHERE supplier_id IS NOT NULL
         GROUP BY venture_id) AS actual_supplier
    ON actual_supplier.venture_id = expected_supplier.venture_id

    INNER JOIN
        (SELECT venture_id, SUM(total_amount) AS total_amount,SUM(expected_labour_expense) AS contractor_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_contractor
    ON expected_contractor.venture_id = expected_supplier.venture_id

    INNER JOIN
        (SELECT venture_id, SUM(total_amount) AS contractor_total
         FROM outbound_payments
         WHERE contractor_id IS NOT NULL
         GROUP BY venture_id) AS actual_contractor
    ON actual_contractor.venture_id = expected_supplier.venture_id
);



"""

# ----- Database helper -----
def run_query(query):
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row   # returns rows as dict-like objects
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


@dashboard_bp.route("/")
def view_data():
    rows = run_query(QUERY)

    # Extract column names from the first row
    if rows:
        columns = rows[0].keys()
    else:
        columns = []

    return render_template(
        "dashboard.html",
        header="JNS Admin Dashboard",
        columns=columns,
        rows=rows
    )

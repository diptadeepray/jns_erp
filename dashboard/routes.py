from flask import Blueprint, render_template, current_app
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)


# total_expected_profit=0
# supplier_total_balance=0
# contractor_total_balance=0
# expected_office_expense=0
# actual_office_expense=0

# ---- 1 PREDEFINED QUERY ----

QUERY1 ="""SELECT 
    client_name "Client Name",
    total_amount_to_be_received_that_party "Contract Amount",
    total_amount_received_from_that_party "Amount Received",
    total_amount_to_be_received_from_that_party "Amount Pending",
    expected_material_expense "Expected Material",
    actual_sitewise_material_expense "Actual Material",
    supplier_difference "Supplier Balance",
    expected_sitewise_labour_expense "Expected Labour",
    actual_sitewise_actual_labour_expense "Actual Labour",
    contractor_difference "Contractor Balance",
    expected_sitewise_profit "Expected Profit",
    expected_sitewise_office_expense "Expected Office"
FROM
(
    -- ================= BASE DATA =================
    SELECT 
        all_clients.client_name AS client_name,
        all_clients.contract_amount AS total_amount_to_be_received_that_party,
        expected_supplier.total_amount AS total_amount_received_from_that_party,
        COALESCE(all_clients.contract_amount, 0) - COALESCE(expected_supplier.total_amount, 0)
                                           AS total_amount_to_be_received_from_that_party,


        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        COALESCE(expected_supplier.supplier_total,0) 
            - COALESCE(actual_supplier.supplier_total,0) AS supplier_difference,

        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        COALESCE(expected_contractor.contractor_total,0) 
            - COALESCE(actual_contractor.contractor_total,0) AS contractor_difference,

        expected_profit.expected_site_profit AS expected_sitewise_profit,
        expected_profit.expected_site_office_expense AS expected_sitewise_office_expense

    FROM (SELECT venture_id, client_name, contract_amount FROM all_clients) all_clients
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS total_amount,
               SUM(expected_material_expense) AS supplier_total
        FROM expected_ap
        WHERE venture_id IS NOT NULL
        GROUP BY venture_id
    ) expected_supplier ON all_clients.venture_id = expected_supplier.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS supplier_total
        FROM outbound_payments
        WHERE supplier_id IS NOT NULL
        GROUP BY venture_id
    ) actual_supplier ON all_clients.venture_id = actual_supplier.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(expected_labour_expense) AS contractor_total
        FROM expected_ap
        WHERE venture_id IS NOT NULL
        GROUP BY venture_id
    ) expected_contractor ON all_clients.venture_id = expected_contractor.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS contractor_total
        FROM outbound_payments
        WHERE contractor_id IS NOT NULL
        GROUP BY venture_id
    ) actual_contractor ON all_clients.venture_id = actual_contractor.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(expected_profit) AS expected_site_profit,
               SUM(expected_office_expense) AS expected_site_office_expense
        FROM expected_ap
        WHERE venture_id IS NOT NULL
        GROUP BY venture_id
    ) expected_profit ON all_clients.venture_id = expected_profit.venture_id
)

UNION ALL

-- ================= TOTAL ROW =================
SELECT
    'TOTAL',
    SUM(total_amount_to_be_received_that_party),
    SUM(total_amount_received_from_that_party),
    SUM(total_amount_to_be_received_from_that_party),
    SUM(expected_material_expense),
    SUM(actual_sitewise_material_expense),
    SUM(supplier_difference),
    SUM(expected_sitewise_labour_expense),
    SUM(actual_sitewise_actual_labour_expense),
    SUM(contractor_difference),
    SUM(expected_sitewise_profit),
    SUM(expected_sitewise_office_expense)
FROM
(
    -- reuse SAME BASE QUERY
    SELECT 
        all_clients.contract_amount AS total_amount_to_be_received_that_party,
        expected_supplier.total_amount AS total_amount_received_from_that_party,
        COALESCE(all_clients.contract_amount, 0) - COALESCE(expected_supplier.total_amount, 0)
                                           AS total_amount_to_be_received_from_that_party,


        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        COALESCE(expected_supplier.supplier_total,0) 
            - COALESCE(actual_supplier.supplier_total,0) AS supplier_difference,
        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        COALESCE(expected_contractor.contractor_total,0) 
            - COALESCE(actual_contractor.contractor_total,0) AS contractor_difference,
        expected_profit.expected_site_profit AS expected_sitewise_profit,
        expected_profit.expected_site_office_expense AS expected_sitewise_office_expense
    FROM (SELECT venture_id, contract_amount FROM all_clients) all_clients
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS total_amount,
               SUM(expected_material_expense) AS supplier_total
        FROM expected_ap
        WHERE venture_id IS NOT NULL
        GROUP BY venture_id
    ) expected_supplier ON all_clients.venture_id = expected_supplier.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS supplier_total
        FROM outbound_payments
        WHERE supplier_id IS NOT NULL
        GROUP BY venture_id
    ) actual_supplier ON all_clients.venture_id = actual_supplier.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(expected_labour_expense) AS contractor_total
        FROM expected_ap
        WHERE venture_id IS NOT NULL
        GROUP BY venture_id
    ) expected_contractor ON all_clients.venture_id = expected_contractor.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS contractor_total
        FROM outbound_payments
        WHERE contractor_id IS NOT NULL
        GROUP BY venture_id
    ) actual_contractor ON all_clients.venture_id = actual_contractor.venture_id
    LEFT JOIN (
        SELECT venture_id,
               SUM(expected_profit) AS expected_site_profit,
               SUM(expected_office_expense) AS expected_site_office_expense
        FROM expected_ap
        WHERE venture_id IS NOT NULL
        GROUP BY venture_id
    ) expected_profit ON all_clients.venture_id = expected_profit.venture_id
);

"""


# ---- 2 PREDEFINED QUERY ----
QUERY2 = """
  SELECT office_reason "Reason of Office Expense", 
         SUM(total_amount) "Expense Amount"
         FROM outbound_payments
         WHERE office_reason IS NOT NULL
         GROUP BY office_reason
         
         UNION ALL

   SELECT 'TOTAL', 
         sum(total_amount_per_reason) FROM (SELECT office_reason,
         SUM(total_amount) AS total_amount_per_reason
         FROM outbound_payments
         WHERE office_reason IS NOT NULL
         GROUP BY office_reason)

         ;
"""
# ---- 3 PREDEFINED QUERY ----
QUERY3 = """
  SELECT supplier_id "Supplier ID", 
         SUM(total_amount) "Promotional Amount"
         FROM inbound_payments
         WHERE supplier_id IS NOT NULL
         GROUP BY supplier_id
         
         UNION ALL

   SELECT 'TOTAL', 
         sum(total_amount_per_reason) FROM (SELECT supplier_id,
         SUM(total_amount) AS total_amount_per_reason
         FROM inbound_payments
         WHERE supplier_id IS NOT NULL
         GROUP BY supplier_id)

         ;
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
    rows = run_query(QUERY1)
    rows_office = run_query(QUERY2)
    rows_supplier_promotion = run_query(QUERY3)

    # Extract column names from the first row
    if rows:
        columns = rows[0].keys()
        total_last_row = rows[-1]  # last row
        total_expected_profit = total_last_row["Expected Profit"] or 0
        supplier_total_balance = total_last_row["Supplier Balance"] or 0
        contractor_total_balance = total_last_row["Contractor Balance"] or 0
        expected_office_expense = total_last_row["Expected Office"] or 0
        


    else:
        columns = []

    # Extract column names from the first row
    if rows_office:
        columns_office = rows_office[0].keys()
        total_last_row_office = rows_office[-1]  # last row
        actual_office_expense = total_last_row_office["Expense Amount"] or 0
    else:
        columns_office = []

    # Extract column names from the first row
    if rows_supplier_promotion:
        columns_supplier_promotion = rows_supplier_promotion[0].keys()
        total_last_row_supplier_promotion = rows_supplier_promotion[-1]  # last row
        actual_supplier_promotion_expense = total_last_row_supplier_promotion["Promotional Amount"] or 0
    else:
        columns_supplier_promotion = []

    # print(type(total_expected_profit))
    # print(type(supplier_total_balance))
    # print(type(contractor_total_balance))
    # print(type(expected_office_expense))
    # print(type(actual_office_expense))  

    total_profit= (total_expected_profit
                   + supplier_total_balance
                   + contractor_total_balance
                   + (expected_office_expense
                   - actual_office_expense)
                   + actual_supplier_promotion_expense)
    
    office_expense_balance = (expected_office_expense - actual_office_expense) or 0

    return render_template(
        "dashboard.html",
        header="JNS Admin Dashboard",
        columns=columns,
        rows=rows,
        columns_office=columns_office,
        rows_office=rows_office,
        rows_supplier_promotion=rows_supplier_promotion,
        columns_supplier_promotion=columns_supplier_promotion,
        total_profit=total_profit,
        office_expense_balance=office_expense_balance

)

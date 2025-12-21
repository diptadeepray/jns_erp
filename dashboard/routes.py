from flask import Blueprint, render_template, current_app
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)

# ---- 1 PREDEFINED QUERY ----
QUERY = """
(SELECT 
    venture_id "Venture ID",
    total_amount_to_be_received_that_party "Total Amount to be Received that Party",

    total_amount_received_from_that_party "Total Amount Received from that Party",

    expected_material_expense "Expected Sitewise Material Expense",
    actual_sitewise_material_expense "Actual Sitewise Material Expense",
    supplier_difference "Sitewise Supplier Balance",
    expected_sitewise_labour_expense "Expected Sitewise Labour Expense",
    actual_sitewise_actual_labour_expense "Actual Sitewise Actual Labour Expense",
    contractor_difference "Sitewise Contractor Balance",

    expected_sitewise_profit "Expected Sitewise Profit"
--column names will be taken from here only 
--because it is UNION ALL


--################################################################################################################
    

FROM (
    SELECT 
        all_clients.venture_id AS venture_id, 
        all_clients.contract_amount AS total_amount_to_be_received_that_party,

        expected_supplier.total_amount AS total_amount_received_from_that_party,      

        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        (COALESCE(expected_supplier.supplier_total, 0) - COALESCE(actual_supplier.supplier_total, 0)) AS supplier_difference,



        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        (COALESCE(expected_contractor.contractor_total, 0) - COALESCE(actual_contractor.contractor_total, 0)) AS contractor_difference,

        expected_profit.expected_site_profit AS expected_sitewise_profit

--##########################################

    FROM 
(
    (SELECT venture_id, contract_amount from all_clients) AS all_clients

        LEFT JOIN
            (SELECT venture_id, SUM(total_amount) AS total_amount, SUM(expected_material_expense) AS supplier_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_supplier

    ON all_clients.venture_id = expected_supplier.venture_id

    LEFT JOIN
        (SELECT venture_id, SUM(total_amount) AS supplier_total
         FROM outbound_payments
         WHERE supplier_id IS NOT NULL
         GROUP BY venture_id) AS actual_supplier

    ON all_clients.venture_id = actual_supplier.venture_id

    LEFT JOIN
        (SELECT venture_id,SUM(expected_labour_expense) AS contractor_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_contractor

    ON all_clients.venture_id = expected_contractor.venture_id

    LEFT JOIN
        (SELECT venture_id, SUM(total_amount) AS contractor_total
         FROM outbound_payments
         WHERE contractor_id IS NOT NULL
         GROUP BY venture_id) AS actual_contractor
    ON all_clients.venture_id = actual_contractor.venture_id

       LEFT JOIN
    (SELECT venture_id, SUM(expected_profit) AS expected_site_profit
         FROM expected_ap
         GROUP BY venture_id) AS expected_profit

    ON all_clients.venture_id = expected_profit.venture_id
) AS venture_data 
))










UNION ALL








(
SELECT
    'TOTAL',
    SUM(total_amount_to_be_received_that_party),
    SUM(total_amount_received_from_that_party),
    SUM(expected_material_expense),
    SUM(actual_sitewise_material_expense),
    SUM(supplier_difference),
    SUM(expected_sitewise_labour_expense),
    SUM(actual_sitewise_actual_labour_expense),
    SUM(contractor_difference),
    SUM(expected_sitewise_profit)



--################################################################################################################
    


FROM (
    SELECT 

        --Here 'TOTAL' will be displayed instead of venture_id
        all_clients.contract_amount AS total_amount_to_be_received_that_party,
    
        expected_supplier.total_amount AS total_amount_received_from_that_party, 

        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        (COALESCE(expected_supplier.supplier_total, 0) - COALESCE(actual_supplier.supplier_total, 0)) AS supplier_difference,

        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        (COALESCE(expected_contractor.contractor_total, 0) - COALESCE(actual_contractor.contractor_total, 0)) AS contractor_difference,

        expected_profit.expected_site_profit AS expected_sitewise_profit

            
--##########################################
FROM 
(
    (SELECT venture_id, contract_amount from all_clients) AS all_clients

        LEFT JOIN

        (SELECT venture_id,SUM(total_amount) AS total_amount, SUM(expected_material_expense) AS supplier_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_supplier

    ON all_clients.venture_id = expected_supplier.venture_id

    LEFT JOIN
        (SELECT venture_id, SUM(total_amount) AS supplier_total
         FROM outbound_payments
         WHERE supplier_id IS NOT NULL
         GROUP BY venture_id) AS actual_supplier
    ON all_clients.venture_id = actual_supplier.venture_id

    LEFT JOIN
        (SELECT venture_id, SUM(expected_labour_expense) AS contractor_total
         FROM expected_ap
         GROUP BY venture_id) AS expected_contractor
    ON all_clients.venture_id = expected_contractor.venture_id

    LEFT JOIN
        (SELECT venture_id, SUM(total_amount) AS contractor_total
         FROM outbound_payments
         WHERE contractor_id IS NOT NULL
         GROUP BY venture_id) AS actual_contractor
    ON all_clients.venture_id = actual_contractor.venture_id)

    LEFT JOIN
    (SELECT venture_id, SUM(expected_profit) AS expected_site_profit
         FROM expected_ap
         GROUP BY venture_id) AS expected_profit

    ON all_clients.venture_id = expected_profit.venture_id ) AS venture_data ))
;
"""
# Not working



QUERY1 ="""SELECT 
    venture_id "Venture ID",
    total_amount_to_be_received_that_party "Total Amount to be Received that Party",
    total_amount_received_from_that_party "Total Amount Received from that Party",
    expected_material_expense "Expected Sitewise Material Expense",
    actual_sitewise_material_expense "Actual Sitewise Material Expense",
    supplier_difference "Sitewise Supplier Balance",
    expected_sitewise_labour_expense "Expected Sitewise Labour Expense",
    actual_sitewise_actual_labour_expense "Actual Sitewise Actual Labour Expense",
    contractor_difference "Sitewise Contractor Balance",
    expected_sitewise_profit "Expected Sitewise Profit"
FROM
(
    -- ================= BASE DATA =================
    SELECT 
        all_clients.venture_id AS venture_id,
        all_clients.contract_amount AS total_amount_to_be_received_that_party,
        expected_supplier.total_amount AS total_amount_received_from_that_party,

        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        COALESCE(expected_supplier.supplier_total,0) 
            - COALESCE(actual_supplier.supplier_total,0) AS supplier_difference,

        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        COALESCE(expected_contractor.contractor_total,0) 
            - COALESCE(actual_contractor.contractor_total,0) AS contractor_difference,

        expected_profit.expected_site_profit AS expected_sitewise_profit
    FROM (SELECT venture_id, contract_amount FROM all_clients) all_clients
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS total_amount,
               SUM(expected_material_expense) AS supplier_total
        FROM expected_ap
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
               SUM(expected_profit) AS expected_site_profit
        FROM expected_ap
        GROUP BY venture_id
    ) expected_profit ON all_clients.venture_id = expected_profit.venture_id
)

UNION ALL

-- ================= TOTAL ROW =================
SELECT
    'TOTAL',
    SUM(total_amount_to_be_received_that_party),
    SUM(total_amount_received_from_that_party),
    SUM(expected_material_expense),
    SUM(actual_sitewise_material_expense),
    SUM(supplier_difference),
    SUM(expected_sitewise_labour_expense),
    SUM(actual_sitewise_actual_labour_expense),
    SUM(contractor_difference),
    SUM(expected_sitewise_profit)
FROM
(
    -- reuse SAME BASE QUERY
    SELECT 
        all_clients.contract_amount AS total_amount_to_be_received_that_party,
        expected_supplier.total_amount AS total_amount_received_from_that_party,
        expected_supplier.supplier_total AS expected_material_expense,
        actual_supplier.supplier_total AS actual_sitewise_material_expense,
        COALESCE(expected_supplier.supplier_total,0) 
            - COALESCE(actual_supplier.supplier_total,0) AS supplier_difference,
        expected_contractor.contractor_total AS expected_sitewise_labour_expense,
        actual_contractor.contractor_total AS actual_sitewise_actual_labour_expense,
        COALESCE(expected_contractor.contractor_total,0) 
            - COALESCE(actual_contractor.contractor_total,0) AS contractor_difference,
        expected_profit.expected_site_profit AS expected_sitewise_profit
    FROM (SELECT venture_id, contract_amount FROM all_clients) all_clients
    LEFT JOIN (
        SELECT venture_id,
               SUM(total_amount) AS total_amount,
               SUM(expected_material_expense) AS supplier_total
        FROM expected_ap
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
               SUM(expected_profit) AS expected_site_profit
        FROM expected_ap
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

   SELECT 'TOTAL', sum(total_amount_per_reason) FROM (SELECT office_reason,
         SUM(total_amount) AS total_amount_per_reason
         FROM outbound_payments
         WHERE office_reason IS NOT NULL
         GROUP BY office_reason)

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

    # Extract column names from the first row
    if rows:
        columns = rows[0].keys()
    else:
        columns = []

    # Extract column names from the first row
    if rows_office:
        columns_office = rows_office[0].keys()
    else:
        columns_office = []

    return render_template(
        "dashboard.html",
        header="JNS Admin Dashboard",
        columns=columns,
        rows=rows,
        columns_office=columns_office,
        rows_office=rows_office)
        #total_profit=total_profit

    #)

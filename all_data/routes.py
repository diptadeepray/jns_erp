from flask import Blueprint, render_template, current_app
import sqlite3

all_data_bp = Blueprint('all_data', __name__)




QUERY1 = """SELECT
 client_name "Client Name",
 site_name "Site Name", 
 contract_type "Contract Type", 
 venture_id "Venture ID", 
 contract_amount "Contract Amount", 
 entry_date "Entry Date"
FROM all_clients;"""

QUERY2 = """SELECT supplier_name "Supplier Name",
 supplier_firm_name "Supplier Firm Name",
 supplier_id "Supplier ID"
FROM all_suppliers;"""

QUERY3 = """SELECT contractor_name "Contractor Name",
 contractor_type "Contractor Type",
 contractor_id "Contractor ID" 
FROM all_contractors;"""

QUERY4=""" SELECT id "ID",
    source "Source",	
    client_name "Client Name",	
    category "Category",
    site_name "Site Name",	
    venture_id "Venture ID",	
    supplier_name "Supplier Name",	
    supplier_id "Supplier ID",	
    cash_amount "Cash Amount",	
    cheque_amount "Cheque Amount",	
    total_amount "Total Amount",	
    	
    cash_name "Cash Name",	
    cheque_name "Cheque Name",	
    cheque_date "Cheque Date",	
    cheque_bank "Cheque Bank",	
    cheque_number "Cheque Number",	

    entry_date "Entry Date",
    amount_number "Amount Number"
FROM inbound_payments;"""

QUERY5=""" SELECT id "ID",
    destination "Destination",
    client_name "Client Name",
    site_name "Site Name",
    venture_id "Venture ID",
    supplier_name "Supplier Name",
    supplier_id "Supplier ID",
    material_description "Material Description",
    contractor_name "Contractor Name",
    contractor_id "Contractor ID",
    labour_description "Labour Description",
    office_reason "Office Reason",
    cash_amount "Cash Amount",
    cheque_amount "Cheque Amount",
    total_amount "Total Amount",
    amount_number "Amount Number",
    cash_name "Cash Name",
    cheque_name "Cheque Name",
    cheque_date "Cheque Date",
    cheque_bank "Cheque Bank",	
cheque_number	"Cheque Number",	
entry_date	"Entry Date"
FROM outbound_payments;"""









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


@all_data_bp.route("/")
def view_data():
    rows_clients = run_query(QUERY1)
    rows_suppliers = run_query(QUERY2)
    rows_contractors = run_query(QUERY3)
    rows_inbound_payments = run_query(QUERY4)
    rows_outbound_payments = run_query(QUERY5)

    # Extract column names from the first row
    if rows_clients:
        columns_clients = rows_clients[0].keys()
        
    else:
        columns_clients = []

    # Extract column names from the first row
    if rows_suppliers:
        columns_suppliers = rows_suppliers[0].keys()
        
    else:
        columns_suppliers = []

    # Extract column names from the first row
    if rows_contractors:
        columns_contractors = rows_contractors[0].keys()

    else:
        columns_contractors = []

    if rows_inbound_payments:
        columns_inbound_payments = rows_inbound_payments[0].keys()
    
    else:
        columns_inbound_payments = []
    if rows_outbound_payments:
        columns_outbound_payments = rows_outbound_payments[0].keys()
    else:
        columns_outbound_payments = []




    return render_template(
        "all_data.html",
        header="View All Data",
        columns_clients=columns_clients,
        rows_clients=rows_clients,
        columns_suppliers=columns_suppliers,
        rows_suppliers=rows_suppliers,
        columns_contractors=columns_contractors,
        rows_contractors=rows_contractors,
        rows_inbound_payments=rows_inbound_payments,
        columns_inbound_payments=columns_inbound_payments,
        rows_outbound_payments=rows_outbound_payments,
        columns_outbound_payments=columns_outbound_payments

)

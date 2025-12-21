
from flask import Blueprint, render_template, request, redirect, current_app
import sqlite3

from config import CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE, SUPPLIER_MONEY_DISTRIBUTION

inbound_payments_bp = Blueprint('inbound_payments', __name__, template_folder='templates')







# Utility to get DB connection
def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn







@inbound_payments_bp.route('/', methods=['GET', 'POST'])
def inbound_payments_home():

    client_categories = list(CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE.keys())
    supplier_categories = list(SUPPLIER_MONEY_DISTRIBUTION.keys())
    
    conn = get_db_connection()
    c = conn.cursor()








    # This following lines will be executed for both GET and POST requests

    # === fetch DROPDOWN DATA FROM onboarding tables ===
    c.execute("SELECT client_name, site_name, venture_id FROM all_clients")
    client_data = c.fetchall()   
    # List of rows (client_name, site_name, venture_id)
    # client_data returns a list of tuples i.e. rows

    c.execute("SELECT supplier_name, supplier_id FROM all_suppliers")
    supplier_data = c.fetchall()  
    # List of rows (supplier_name, supplier_id)
    # client_data returns a list of tuples i.e. rows

    c.execute("SELECT contractor_name, contractor_id FROM all_contractors")
    contractor_data = c.fetchall()  
    # List of rows (contractor_name, contractor_id)
    # client_data returns a list of tuples i.e. rows


    message = ""
    









    
    if request.method == 'POST':










        
        check_category=request.form.get("category")
        check_client_name=request.form.get("client_name")
        check_site_name=request.form.get("site_name")
        known_venture_id = request.form.get("venture_id")

        print("Went correctly")


        conn = get_db_connection()
        c = conn.cursor()

        c.execute("""
    SELECT client_name, site_name, contract_type 
    FROM all_clients 
    WHERE venture_id = ?
""", (known_venture_id,))

        row = c.fetchone()

        if row:
            actual_client_name, actual_site_name, actual_contract_type = row
            if (actual_client_name == check_client_name and 
                actual_site_name == check_site_name and
                actual_contract_type == check_category):
                message = "Previous entry was successfully added."


                # Indentaion level indicates this code is inside the above if-block
                        














                # Extract posted fields
                fields = [
                "source", "category", "client_name", "site_name", "venture_id",
                "supplier_name", "supplier_id", "cash_amount", "cheque_amount",
                "total_amount", "amount_number", "cash_name", "cheque_name",
                "cheque_date", "cheque_bank", "cheque_number",
                "entry_date", "ar_id"
            ]

                data = [request.form.get(f) for f in fields]



                c.execute("""
                INSERT INTO inbound_payments 
                (source, category, client_name, site_name, venture_id,
                supplier_name, supplier_id, cash_amount, cheque_amount, total_amount,
                amount_number, cash_name, cheque_name, cheque_date, cheque_bank,
                cheque_number, entry_date, ar_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)



            #print("Total Amount:", data[9])  # Debug print for total_amount

            # ===== DETERMINE EXPECTED AP BREAKUP =====
                breakup = [0,0,0,0]  # Initialize breakup

                if data[0].lower()=="client":
                    breakup=CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE[data[1]]
                elif data[0].lower()=="supplier":
                    breakup=SUPPLIER_MONEY_DISTRIBUTION[data[1]]
                else:
                    print("Unknown category entered. Check code very carefully")

                
                print(type(data[9]), type(breakup[0]))  # Debug print to check types


                # ===== INSERT INTO expected_ap =====
                expected_ap_data = [
                request.form.get("source"),
                request.form.get("category"),
                request.form.get("client_name"),
                request.form.get("site_name"),
                request.form.get("venture_id"),
                request.form.get("supplier_name"),
                request.form.get("supplier_id"),
                request.form.get("total_amount"),   # → total_amount_received_from_that_party

            
                # You need to convert to float for multiplication

                # Previously data[9] was a string from form input
                # SQLite table saids REAL type for these fields
                # So SQLite internally converts to float anyway

                # But to be safe, we convert explicitly here

                float(data[9])*breakup[0],   # expected_office_expense (default)
                float(data[9])*breakup[1],   # expected_material_expense (default)
                float(data[9])*breakup[2],   # expected_labour_expense (default)
                float(data[9])*breakup[3]   # expected_profit (default)
                        ]

                c.execute("""
                INSERT INTO expected_ap
                (source, category, client_name, site_name, venture_id,
                supplier_name, supplier_id, total_amount,
                expected_office_expense, expected_material_expense,
                expected_labour_expense, expected_profit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, expected_ap_data)
                


                conn.commit()
                
                conn.close()
                # it automatically closes all associated cursors.













    

            else:
                print("Mismatch found:")
                if actual_client_name != check_client_name:
                    print(f"Client Name mismatch: expected {actual_client_name}, got {check_client_name}")
                    message = f"Client Name mismatch: expected {actual_client_name}, got {check_client_name}. Validation done with Venture_ID"
                if actual_site_name != check_site_name:
                    print(f"Site Name mismatch: expected {actual_site_name}, got {check_site_name}")
                    message = f"Site Name mismatch: expected {actual_site_name}, got {check_site_name}. Validation done with Venture_ID."
                if actual_contract_type != check_category:
                    print(f"Category mismatch: expected {actual_contract_type}, got {check_category}")
                    message = f"Category mismatch: expected {actual_contract_type}, got {check_category}. Validation done with Venture_ID"
        else:
            print("No match found. Check everything carefully")
            message = "Previous entry did not exist."




















        
        
        
    
















    return render_template('inbound_payments.html', client_data=client_data, supplier_data=supplier_data, 
                           client_categories=client_categories, supplier_categories=supplier_categories, message=message)
    # This line will be executed for both GET and POST requests
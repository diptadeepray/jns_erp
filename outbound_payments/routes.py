from flask import Blueprint, render_template, request, redirect, current_app
import sqlite3

from config import OFFICE_EXPENSE_CATEGORIES

outbound_payments_bp = Blueprint('outbound_payments', __name__, template_folder='templates')

# Utility to get DB connection
def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@outbound_payments_bp.route('/', methods=['GET', 'POST'])
def outbound_payments_home():
    
    conn = get_db_connection()
    c = conn.cursor()

    # === fetch DROPDOWN DATA FROM onboarding tables ===
    c.execute("SELECT client_name, site_name, venture_id FROM all_clients")
    client_data = c.fetchall()   # List of rows (client_name, site_name, venture_id)

    c.execute("SELECT supplier_name, supplier_id FROM all_suppliers")
    supplier_data = c.fetchall()  # List of rows (supplier_name, supplier_id)

    c.execute("SELECT contractor_name, contractor_id FROM all_contractors")
    contractor_data = c.fetchall()  # List of rows (contractor_name, contractor_id)
    
    message = ""







    if request.method == 'POST':







        check_client_name=request.form.get("client_name")
        check_site_name=request.form.get("site_name")
        known_venture_id = request.form.get("venture_id")

        #print("Went correctly")


        conn = get_db_connection()
        c = conn.cursor()

        c.execute("""
    SELECT client_name, site_name 
    FROM all_clients 
    WHERE venture_id = ?
""", (known_venture_id,))

        row = c.fetchone()

        if row:
            actual_client_name, actual_site_name = row
            if (actual_client_name == check_client_name and 
                actual_site_name == check_site_name):
                message = "Previous entry was successfully added."








#------------------------------

                # Extract posted fields — MUST match your SQLite table columns
                fields = [
                    "destination",
                    "client_name",
                    "site_name",
                    "venture_id",
                    "supplier_name",
                    "supplier_id",
                    "material_description",
                    "contractor_name",
                    "contractor_id",
                    "labour_description",
                    "office_reason",
                    "cash_amount",
                    "cheque_amount",
                    "total_amount",
                    "amount_number",
                    "cash_name",
                    "cheque_name",
                    "cheque_date",
                    "cheque_bank",
                    "cheque_number",
                    "entry_date",
                    "actual_ap_id"
                ]

                # Read values from HTML form
                data = [request.form.get(f) for f in fields]






                print(data)

                # Get the index
                cash_index = fields.index("cash_amount")
                cheque_index = fields.index("cheque_amount")
                total_index = fields.index("total_amount")

                cash_value = float(data[cash_index].replace(",", "")) if data[cash_index] else 0
                cheque_value = float(data[cheque_index].replace(",", "")) if data[cheque_index] else 0

                # Put the cleaned values back into the list
                data[cash_index] = cash_value
                data[cheque_index] = cheque_value

                # Compute total_amount and put it into the list
                data[total_index] = cash_value + cheque_value

                print(data)










                # Insert query MUST match the column order above
                c.execute("""
                    INSERT INTO outbound_payments (
                        destination, client_name, site_name, venture_id,
                        supplier_name, supplier_id, material_description,
                        contractor_name, contractor_id, labour_description,
                        office_reason, cash_amount, cheque_amount, total_amount,
                        amount_number, cash_name, cheque_name, cheque_date,
                        cheque_bank, cheque_number, entry_date, actual_ap_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)

                conn.commit()
                conn.close()
                
                # The following redirect line is redundant for the following reason:
                '''<input name="venture_id" disabled>  is disabled initially in HTML form.
                   So venture_id was not being sent in the POST request on refresh.
                   So Flask received request.form.get("venture_id") = None.
                   There is a else block which says "No match found. Check everything carefully"
                   So duplicate entry was not happening on refresh.'''
                #return redirect('/outbound_payments')
                #Why this line is commented out?
                '''When you call redirect(), Flask tells the browser: 
                   "Go make a new GET request to /outbound_payments."
                   Any variables in memory (like message) are lost because a new request is happening.'''


        #------------------------------

            else:
                print("Mismatch found:")
                if actual_site_name != check_site_name:
                    print(f"Site Name mismatch: expected {actual_site_name}, got {check_site_name}")
                    message = f"Site Name mismatch: expected {actual_site_name}, got {check_site_name}. Validation done with Venture_ID."
                if actual_client_name != check_client_name:
                    print(f"Client Name mismatch: expected {actual_client_name}, got {check_client_name}")
                    message = f"Client Name mismatch: expected {actual_client_name}, got {check_client_name}. Validation done with Venture_ID"


        else:
            print("No match found. Check everything carefully")
            message = "The entered VentureID does not exist."









    return render_template('outbound_payments.html', office_expense_categories=OFFICE_EXPENSE_CATEGORIES, client_data=client_data, supplier_data=supplier_data, contractor_data=contractor_data, message=message)

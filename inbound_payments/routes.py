
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

        given_supplier_id = request.form.get("supplier_id")

        #print("Went correctly")


        conn = get_db_connection()
        c = conn.cursor()

        c.execute("""
    SELECT client_name, site_name, contract_type 
    FROM all_clients 
    WHERE venture_id = ?
""", (known_venture_id,))

        row = c.fetchone()

        if row and (given_supplier_id is None ):
            actual_client_name, actual_site_name, actual_contract_type = row
            if (actual_client_name == check_client_name and 
                actual_site_name == check_site_name and
                actual_contract_type == check_category):
                message = "Previous entry of client was successfully added."


                        














                
                fields = [
                "source", "category", "client_name", "site_name", "venture_id",
                "supplier_name", "supplier_id", "cash_amount", "cheque_amount",
                "total_amount", "amount_number", "cash_name", "cheque_name",
                "cheque_date", "cheque_bank", "cheque_number",
                "entry_date", "ar_id"]

                # Extract all posted fields at once
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



                c.execute("""
                INSERT INTO inbound_payments 
                (source, category, client_name, site_name, venture_id,
                supplier_name, supplier_id, cash_amount, cheque_amount, total_amount,
                amount_number, cash_name, cheque_name, cheque_date, cheque_bank,
                cheque_number, entry_date, ar_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
                
                conn.commit()

                last_id = c.lastrowid




            #print("Total Amount:", data[9])  # Debug print for total_amount

            # ===== DETERMINE EXPECTED AP BREAKUP =====
                breakup = [0,0,0,0]  # Initialize breakup

                if data[0].lower()=="client":
                    # The category is taken as key of the dictionary-CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE
                    breakup=CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE[data[1]]
                elif data[0].lower()=="supplier":
                    breakup=SUPPLIER_MONEY_DISTRIBUTION[data[1]]
                else:
                    print("Unknown category entered. Check code very carefully")

                
                # print(type(data[9]), type(breakup[0]))    # Debug print to check types


                # ===== INSERT INTO expected_ap =====
                expected_ap_data = [
                request.form.get("source"),
                request.form.get("category"),
                request.form.get("client_name"),
                request.form.get("site_name"),
                request.form.get("venture_id"),
                request.form.get("supplier_name"),
                request.form.get("supplier_id"),
                data[total_index],   # → total_amount_received_from_that_party

            
                # You need to convert to float for multiplication

                # Previously data[9] was a string from form input
                # SQLite table saids REAL type for these fields
                # So SQLite internally converts to float anyway

                # But to be safe, we convert explicitly here

                float(data[total_index])*breakup[0],   # expected_office_expense (default)
                float(data[total_index])*breakup[1],   # expected_material_expense (default)
                float(data[total_index])*breakup[2],   # expected_labour_expense (default)
                float(data[total_index])*breakup[3],   # expected_profit (default)
                last_id
                        ]

                c.execute("""
                INSERT INTO expected_ap
                (source, category, client_name, site_name, venture_id,
                supplier_name, supplier_id, total_amount,
                expected_office_expense, expected_material_expense,
                expected_labour_expense, expected_profit, inbound_payments_column_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, expected_ap_data)
                


                conn.commit()
                
                conn.close()

                print(f"Data inserted {expected_ap_data}")


                # The following redirect line is redundant for the following reason:
                '''<input name="venture_id" disabled>  is disabled initially in HTML form.
                   So venture_id was not being sent in the POST request on refresh.
                   So Flask received request.form.get("venture_id") = None.
                   There is a else block which says "No match found. Check everything carefully"
                   So duplicate entry was not happening on refresh.'''
                #return redirect('/inbound_payments')
                #Why this line is commented out?
                '''When you call redirect(), Flask tells the browser: 
                   "Go make a new GET request to /inbound_payments."
                   Any variables in memory (like message) are lost because a new request is happening.'''





        




    

            else:
                print("Mismatch found:")
                if actual_site_name != check_site_name:
                    print(f"Site Name mismatch: expected {actual_site_name}, got {check_site_name}")
                    message = f"Site Name mismatch: expected {actual_site_name}, got {check_site_name}. Validation done with Venture_ID."
                if actual_contract_type != check_category:
                    print(f"Category mismatch: expected {actual_contract_type}, got {check_category}")
                    message = f"Category mismatch: expected {actual_contract_type}, got {check_category}. Validation done with Venture_ID"
                if actual_client_name != check_client_name:
                    print(f"Client Name mismatch: expected {actual_client_name}, got {check_client_name}")
                    message = f"Client Name mismatch: expected {actual_client_name}, got {check_client_name}. Validation done with Venture_ID"




        elif (row is None) and given_supplier_id:
            message = "Previous entry of supplier was successfully added."

                
            fields = [
                "source", "category", "client_name", "site_name", "venture_id",
                "supplier_name", "supplier_id", "cash_amount", "cheque_amount",
                "total_amount", "amount_number", "cash_name", "cheque_name",
                "cheque_date", "cheque_bank", "cheque_number",
                "entry_date", "ar_id"]

            # Extract all posted fields at once
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



            c.execute("""
                INSERT INTO inbound_payments 
                (source, category, client_name, site_name, venture_id,
                supplier_name, supplier_id, cash_amount, cheque_amount, total_amount,
                amount_number, cash_name, cheque_name, cheque_date, cheque_bank,
                cheque_number, entry_date, ar_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)

            conn.commit()
                
            conn.close()
        
        else:
            print("No match found. Check everything carefully")
            message = "The entered VentureID/SupplierID is not entered or does not exist."


















    return render_template('inbound_payments.html', client_data=client_data, supplier_data=supplier_data, 
                           client_categories=client_categories, supplier_categories=supplier_categories, message=message)
    # This line will be executed for both GET and POST requests
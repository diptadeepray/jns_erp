from flask import Blueprint, render_template, request, redirect, current_app
import sqlite3

from config import CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE, CONTRACTOR_WORK_CATEGORIES

onboarding_bp = Blueprint('onboarding', __name__, template_folder='templates')

# Utility to get DB connection
def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@onboarding_bp.route('/', methods=['GET', 'POST'])
def onboarding_home():
    conn = get_db_connection()
    c = conn.cursor()

    client_categories = list(CLIENT_MONEY_DISTRIBUTION_CATEGORYWISE.keys())

    # === FETCH DROPDOWN DATA FROM onboarding TABLE ===
    c.execute("SELECT client_name, site_name, venture_id FROM all_clients")
    client_data = c.fetchall()   
    # # List of rows (client_name, site_name, venture_id) 
    # # Returns a list of tuples

    c.execute("SELECT supplier_name, supplier_firm_name, supplier_id FROM all_suppliers")
    supplier_data = c.fetchall()  
    # # List of rows (supplier_name, supplier_id)
    # # Returns a list of tuples

    c.execute("SELECT contractor_name, contractor_type, contractor_id FROM all_contractors")
    contractor_data = c.fetchall()  
    # # List of rows (contractor_name, contractor_id)
    # # Returns a list of tuples
    
    if request.method == 'POST':
        form_type = request.form.get("form_type")

        if form_type == "add_client":

            


            client_name = request.form["client_name"]
            site_name = request.form["site_name"]
            contract_type = request.form["contract_type"]
            entry_date = request.form["entry_date"]
            contract_amount = request.form["contract_amount"]
            contract_amount=float(contract_amount.replace(",", "")) # Clean commas if any
            venture_id = client_name[0:3].upper() + site_name[0:3].upper() + contract_type[0:1].upper()
            existing_ids = {row[2] for row in client_data}   # Set of all venture_id values

            n=0
            a=1
            while n==0:
                if venture_id in existing_ids:
                    venture_id = venture_id[0:7]+str(a)
                    a+=1
                else:
                    n=1


            c.execute("""
                INSERT INTO all_clients 
                (client_name, site_name, contract_type, entry_date, contract_amount, venture_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (client_name, site_name, contract_type, entry_date, contract_amount, venture_id))

            conn.commit()
            
            conn.close()
            # it automatically closes all associated cursors.
            
            return redirect('/onboarding')
        
        elif form_type == "add_supplier":
            supplier_name = request.form["supplier_name"]
            supplier_firm_name = request.form["supplier_firm_name"]
            supplier_id = supplier_name[0:3].upper()+supplier_firm_name[0:3].upper()

            existing_ids = {row[2] for row in supplier_data}   # Set of all supplier_id values

            n=0
            a=1
            while n==0:
                if supplier_id in existing_ids:
                    supplier_id = supplier_id[0:6]+str(a)
                    a+=1
                else:
                    n=1




            c.execute("INSERT INTO all_suppliers (supplier_name, supplier_firm_name, supplier_id) VALUES (?, ?, ?)", (supplier_name, supplier_firm_name, supplier_id))
            conn.commit()
            conn.close()
            return redirect('/onboarding')
        
        elif form_type == "add_contractor":
            contractor_name = request.form["contractor_name"]
            contractor_type = request.form["contractor_type"]
            contractor_id = contractor_name[0:3].upper()+contractor_type[0:3].upper()

            existing_ids = {row[2] for row in contractor_data}   # Set of all contractor_id values

            n=0
            a=1
            while n==0:
                if contractor_id in existing_ids:
                    contractor_id = contractor_id[0:6]+str(a)
                    a+=1
                else:
                    n=1




            c.execute("INSERT INTO all_contractors (contractor_name, contractor_type, contractor_id) VALUES (?, ?, ?)", (contractor_name, contractor_type, contractor_id))
            conn.commit()
            conn.close()
            return redirect('/onboarding')
    


    return render_template('onboarding.html', client_categories=client_categories, contractor_work_categories=CONTRACTOR_WORK_CATEGORIES)
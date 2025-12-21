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
    
    if request.method == 'POST':

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
        
        return redirect('/outbound_payments')   # redirect to same page

    return render_template('outbound_payments.html', office_expense_categories=OFFICE_EXPENSE_CATEGORIES, 
                           client_data=client_data, supplier_data=supplier_data, contractor_data=contractor_data)

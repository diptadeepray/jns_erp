from flask import Blueprint, render_template, current_app, request
import sqlite3

delete_data_bp = Blueprint('delete_data', __name__)


BACKUP_FILE = "deleted_data.txt"













@delete_data_bp.route("/", methods=['GET', 'POST'])
# Internally Flask treats it as:
# @delete_data_bp.route("/", methods=["GET"])
def delete_data():
    message = ""
    result = ""

    if request.method == 'POST':

        delete_table = request.form.get("table")
        delete_parameter = request.form.get("parameter")
        delete_value = request.form.get("value").strip() #If mistakenly user adds spaces







        if delete_table and delete_parameter and delete_value:
            db_path = current_app.config['DATABASE']
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()

            try:
                select_query = f"SELECT * FROM {delete_table} WHERE {delete_parameter} = ?"
                cur.execute(select_query, (delete_value,))
                row = cur.fetchone()
                if row:
                    if delete_table == "inbound_payments":

                        # id in inbound_payment is there
                        # same id is also in expected_ap table called inbound_payments_id
                        # we aldo need to delete that record

                        # Steps to delete from expected_ap
                        # 1. Select that value from expected_ap
                        # 2. Put that value to row and append that to result
                        # 3. Delete that value from expected_ap
                        # 4. Select the value from inbound_payments
                        # 6. Put that value to row and append that to result
                        # 7. Delete the value from inbound_payments


                        id_expected_ap_ = f"SELECT * FROM expected_ap WHERE inbound_payments_column_id = ?"
                        cur.execute(id_expected_ap_, (delete_value,))
                        # execute() always expects parameters as a sequence (tuple/list)
                        row = cur.fetchone()
                        if row:
                            delete_row_from_expected_ap = f"DELETE FROM expected_ap WHERE inbound_payments_column_id = ?"
                            cur.execute(delete_row_from_expected_ap, (delete_value,))
                            message+=f"Record deleted from expected_ap for inbound_payments_column_id = {delete_value}. "
                            result+=str(row)
                        else:
                            message+=f"No matching records found in expected_ap to delete for inbound_payments_column_id = {delete_value}."
                            result+=""



                        select_query = f"SELECT * FROM {delete_table} WHERE {delete_parameter} = ?"
                        cur.execute(select_query, (delete_value,))
                        row = cur.fetchone()
                        

                        delete_query = f"DELETE FROM {delete_table} WHERE {delete_parameter} = ?"
                        cur.execute(delete_query, (delete_value,))
                        
                        message = f"Deleted records from {delete_table} where {delete_parameter} = {delete_value}."
                        result += str(row)

                    else:

                        delete_query = f"DELETE FROM {delete_table} WHERE {delete_parameter} = ?"
                        cur.execute(delete_query, (delete_value,))

                        message = f"Deleted records from {delete_table} where {delete_parameter} = {delete_value}."
                        result = row
                        
                else:
                    message = "No matching records found to delete."
                    result = ""

            except sqlite3.OperationalError as e:

                if "no such column" in str(e):
                    message = f"Error: The column '{delete_parameter}' does not exist."
                    result = ""
                else:
                    message = f"Database error: {e}"
                    result = ""

            conn.commit()
            conn.close()
            







        else:
            message = "Please provide table name, parameter name and value name."
            result = ""







    return render_template(
        "delete_data.html",
        header="Delete Data",
        message=message,
        result=result,
        all_table_names=["all_clients", "all_suppliers", "all_contractors", "inbound_payments", "outbound_payments"],
        all_ids=["venture_id", "supplier_id", "contractor_id", "id"]
)
#The second code


import sqlite3, os


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

        # Execute a query to get all data from the table
# cursor.execute(f"SELECT id, source, category, site_name, venture_id, expected_office_expense, expected_material_expense, expected_labour_expense, expected_profit FROM expected_ap")


Q="""
SELECT
    'TOTAL',
    SUM(total_amount_to_be_received_that_party) ,
    SUM(total_amount_received_from_that_party),
    SUM(expected_material_expense),
    SUM(actual_sitewise_material_expense),
    SUM(supplier_difference),
    SUM(expected_sitewise_labour_expense),
    SUM(actual_sitewise_actual_labour_expense),
    SUM(contractor_difference),
    SUM(expected_sitewise_profit)

    


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
))"""

cursor.execute(Q)

rows = cursor.fetchall()

# Print column names
column_names = [description[0] for description in cursor.description]
print(" | ".join(column_names))
print("-" * 50)

        # Print all rows of the table
for row in rows:
        print(row)

        # Close the connection
conn.close()
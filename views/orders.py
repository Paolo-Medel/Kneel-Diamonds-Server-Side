import sqlite3
import json

def list_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.metal_id,
            c.carats_id,
            c.style_id,
            c.price
        FROM CUSTORDER c
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        orders=[]
        for row in query_results:
            orders.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_orders = json.dumps(orders)

    return serialized_orders

def retrieve_orders(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.metal_id,
            c.carats_id,
            c.style_id,
            c.price
        FROM CUSTORDER c
        WHERE c.id = ?
        """, (pk,))

        query_results = db_cursor.fetchone()

        order = dict(query_results)
        serialized_order = json.dumps(order)

        return serialized_order
    
def delete_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM CUSTORDER WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False

def insert_order(order_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO CUSTORDER VALUES (NULL, ?, ?, ?, ?)
            """,
            (order_data['metal_id'], order_data['carats_id'], order_data['style_id'], order_data['price'])
        )

        serialized_hauler = "Post Successfully Added"

    return serialized_hauler
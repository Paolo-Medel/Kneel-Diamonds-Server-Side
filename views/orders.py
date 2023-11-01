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

def expand_order_by_id(url, pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if url["pk"] != "":
            # If _embed is set to "ships," join the Ship table to get haulers and their ships
            db_cursor.execute("""
            SELECT
                c.id AS CUSTORDER_id,
                c.metal_id,
                c.carats_id,
                c.style_id, 
                c.price AS order_price,
                m.id,
                m.metal,
                m.price AS metal_price,
                z.id,
                z.carats,
                z.price AS size_price,
                s.id,
                s.style,
                s.price AS style_price
            FROM CUSTORDER c
            LEFT JOIN Metals m ON c.metal_id = m.id
            LEFT JOIN Sizes z ON c.carats_id = z.id
            LEFT JOIN Styles s ON c.style_id = s.id
            WHERE c.id = ?;
            """, (pk,))

            query_results = db_cursor.fetchone()
            query_results_dict = dict(query_results)

            orders_data = {
                "id": query_results_dict['CUSTORDER_id'],
                "metal_id": query_results_dict['metal_id'],
                "carats_id": query_results_dict['carats_id'],
                "style_id": query_results_dict['style_id'],
                "price": query_results_dict['order_price'],
            }

            if "_expand" in url["query_params"] and "metals" in url["query_params"]["_expand"]:
                metal = {
                    "id": query_results_dict['metal_id'],
                    "metal": query_results_dict['metal'],
                    "price": query_results_dict['metal_price']
                }
                orders_data["metal"] = metal

            if "_expand" in url["query_params"] and "styles" in url["query_params"]["_expand"]:
                styles = {
                    "id": query_results_dict['style_id'],
                    "style": query_results_dict['style'],
                    "price": query_results_dict['style_price']
                }
                orders_data["styles"] = styles

            if "_expand" in url["query_params"] and "sizes" in url["query_params"]["_expand"]:
                sizes = {
                    "id": query_results_dict['carats_id'],
                    "carats": query_results_dict['carats'],
                    "price": query_results_dict['size_price']
                }
                orders_data["sizes"] = sizes
            # Extract hauler data from the dictionary and convert it to a list
            # orders = list(orders_data.values())

        serialized_orders = json.dumps(orders_data)
        return serialized_orders

def expand_order(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                c.id AS CUSTORDER_id,
                c.metal_id,
                c.carats_id,
                c.style_id, 
                c.price AS order_price,
                m.id,
                m.metal,
                m.price AS metal_price,
                z.id,
                z.carats,
                z.price AS size_price,
                s.id,
                s.style,
                s.price AS style_price
            FROM CUSTORDER c
            LEFT JOIN Metals m ON c.metal_id = m.id
            LEFT JOIN Sizes z ON c.carats_id = z.id
            LEFT JOIN Styles s ON c.style_id = s.id
            """)

        expanded_orders = []
        query_results = db_cursor.fetchall()
        for row in query_results:
            query_results_dict = dict(row)

            orders_data = {
                "id": query_results_dict['CUSTORDER_id'],
                "metal_id": query_results_dict['metal_id'],
                "carats_id": query_results_dict['carats_id'],
                "style_id": query_results_dict['style_id'],
                "price": query_results_dict['order_price'],
            }
            if "metals" in url["query_params"]["_expand"] or "*" in url["query_params"]["_expand"]:
                metal = {
                    "id": query_results_dict['metal_id'],
                    "metal": query_results_dict['metal'],
                    "price": query_results_dict['metal_price']
                }
                orders_data["metal"] = metal
            if "styles" in url["query_params"]["_expand"] or "*" in url["query_params"]["_expand"]:
                styles = {
                    "id": query_results_dict['style_id'],
                    "style": query_results_dict['style'],
                    "price": query_results_dict['style_price']
            }
                orders_data["styles"] = styles
            if "sizes" in url["query_params"]["_expand"] or "*" in url["query_params"]["_expand"]:
                sizes = {
                    "id": query_results_dict['carats_id'],
                    "carats": query_results_dict['carats'],
                    "price": query_results_dict['size_price']
            }
                orders_data["sizes"] = sizes

            expanded_orders.append(orders_data)
        # Extract hauler data from the dictionary and convert it to a list
        # orders = list(orders_data.values())

        serialized_orders = json.dumps(expanded_orders)
        return serialized_orders

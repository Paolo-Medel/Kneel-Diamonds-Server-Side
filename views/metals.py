import sqlite3
import json

def list_metals():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        metals=[]
        for row in query_results:
            metals.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_metals = json.dumps(metals)

    return serialized_metals

def retrieve_metal(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        WHERE m.id = ?
        """, (pk,))

        query_results = db_cursor.fetchone()

        metal = dict(query_results)
        serialized_metal = json.dumps(metal)

        return serialized_metal
    
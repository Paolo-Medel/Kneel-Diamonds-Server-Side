import sqlite3
import json

def list_sizes():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.carats,
            s.price
        FROM Sizes s
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        Sizes=[]
        for row in query_results:
            Sizes.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_sizes = json.dumps(Sizes)

    return serialized_sizes

def retrieve_size(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.carats,
            s.price
        FROM Sizes s
        WHERE s.id = ?
        """, (pk,))

        query_results = db_cursor.fetchone()

        size = dict(query_results)
        serialized_size = json.dumps(size)

        return serialized_size
    
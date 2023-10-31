import sqlite3
import json

def list_styles():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.style,
            s.price
        FROM Styles s
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        Styles=[]
        for row in query_results:
            Styles.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_styles = json.dumps(Styles)

    return serialized_styles

def retrieve_style(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.style,
            s.price
        FROM Styles s
        WHERE s.id = ?
        """, (pk,))

        query_results = db_cursor.fetchone()

        style = dict(query_results)
        serialized_style = json.dumps(style)

        return serialized_style
    
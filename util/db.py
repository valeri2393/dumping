from sqlite3 import Connection


def request_sql(conn: Connection, query: str):
    with conn:
        cursor = conn.cursor()
        data = cursor.execute(query).fetchall()
        cursor.close()
        return data


def get_cards_info(conn: Connection, resource: str) -> list:
    query = "SELECT id, url FROM cards " +\
            f"WHERE resource = '{resource}'"
    data = request_sql(conn, query)
    urls = [el[1] for el in data]
    ids = [el[0] for el in data]
    return urls, ids

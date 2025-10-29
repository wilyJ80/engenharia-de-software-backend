from db.connection import Connection


_connection = Connection()

def get_db():
    conn = _connection.get_conn()
    try:
        yield conn
    finally:
        _connection.release_conn(conn)
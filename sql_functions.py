import psycopg2-binary

def create_tables(conn):
    commands = ("""
        CREATE TABLE users (
            user_id VARCHAR(255) PRIMARY KEY,
            reminder_on BOOLEAN,
            under_who VARCHAR(255)
        )
    """,
    """
    CREATE TABLE settings (
        user_id VARCHAR(255) PRIMARY KEY,
        message TEXT,
        frequency TEXT,
        time INT
    )
    """
    )

    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()

def insert_user(conn, user_id):
    command = f"""
        INSERT INTO users (user_id)
        VALUES ({user_id})
    """

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
import psycopg2

def create_tables(conn):
    commands = ("""
        CREATE TABLE users (
            user_id VARCHAR(255) PRIMARY KEY,
            user_name VARCHAR(255)
            first_name VARCHAR(255),
            reminder_on BOOLEAN,
            under_who VARCHAR(255)
        );
    """,
    """
    CREATE TABLE settings (
        user_id VARCHAR(255) PRIMARY KEY,
        message TEXT,
        frequency TEXT,
        time INT
    );
    """
    )

    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()

def insert_user(conn, user_id, user_name, first_name):
    command = f"""
        INSERT INTO users (user_id, user_name, first_name, reminder_on)
        VALUES ({user_id}, '{user_name}', '{first_name}', false);
    """

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()

## check if reminder already set and toggle.
def toggle_reminder(conn, user_id):
    command = f"""
        SELECT reminder_on
        FROM users
        WHERE user_id='{user_id}';
    """
    cur = conn.cursor()
    cur.execute(command)
    # gets the current setting
    curr_setting = cur.fetchone()[0]
    new_setting = not curr_setting
    print(curr_setting[1])

    command = f"""
        UPDATE users
        SET reminder_on={new_setting}
        WHERE user_id='{user_id}';
    """
    cur.execute(command)
    cur.close()
    conn.commit()
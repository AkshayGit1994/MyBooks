import mysql.connector


def get_db(config):
    return mysql.connector.connect(
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"]
    )


def query_db(config, sql, params=()):
    conn = None
    cursor = None

    try:
        conn = get_db(config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


def execute_db(config, sql, params=()):
    conn = None
    cursor = None

    try:
        conn = get_db(config)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

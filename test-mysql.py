import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="183.82.6.191",          # or public IP / DNS of your DB server
        port=3306,
        database="examportal_db",
        user="examportal_admin",
        password="examportal_admin@7799!"
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"✅ Connected to MySQL Server version {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"📂 You're connected to database: {record[0]}")

except Error as e:
    print(f"❌ Error while connecting to MySQL: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("🔒 MySQL connection is closed")

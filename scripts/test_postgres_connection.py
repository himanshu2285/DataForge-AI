import psycopg2

# Update these credentials
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "demodb"
DB_USER = "postgres"
DB_PASSWORD = "Admin"
#DB_URL = "postgresql://postgres:admin@localhost:5432/demodb"

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
    )
    
    cursor = connection.cursor()
    print("PostgreSQL Connection Successful!")

    # Execute a test query
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ;")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
        
    # close connection  
    cursor.close()
    connection.close()

except Exception as e:
    print("Database error:", e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
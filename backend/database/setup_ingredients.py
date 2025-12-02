import pymysql
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Connect to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='databrew'
)

try:
    with connection.cursor() as cursor:
        # Read SQL file
        sql_file = os.path.join(script_dir, 'create_ingredients_tables.sql')
        with open(sql_file, 'r') as f:
            sql_script = f.read()
        
        # Split into individual statements
        statements = sql_script.split(';')
        
        # Execute each statement
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"[OK] Executed: {statement[:50]}...")
                except Exception as e:
                    print(f"[ERROR] Error: {str(e)[:100]}")
        
        connection.commit()
        print("\n[SUCCESS] Database tables created successfully!")
        
finally:
    connection.close()

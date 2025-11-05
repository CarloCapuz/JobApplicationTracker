
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('job_tracker.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()


# Execute the query to fetch all rows from the "job_applications" table
cursor.execute("SELECT * FROM status_history;")
# cursor.execute("SELECT applied_date,* FROM job_applications;")

# cursor.execute("PRAGMA table_info(job_applications);")
rows = cursor.fetchall()  # Fetch all rows from the query

# Get column names (the cursor.description will now work because we executed the query)
columns = [desc[0] for desc in cursor.description]  # Column names

# Create a DataFrame from the query result
data_df = pd.DataFrame(rows, columns=columns)

# Display the results as a table
print("\nData from job_applications table:")
print(data_df)


# Close the connection
conn.close()


'''
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('job_tracker.db')
cursor = conn.cursor()

# Define the SQL update query
update_query = """
UPDATE status_history
SET changed_at = '2025-10-28 00:00:00'
WHERE id = 2;
"""

# Execute the update query
cursor.execute(update_query)

# Commit the changes to save them permanently
conn.commit()

# Optionally check how many rows were updated
print(f"{cursor.rowcount} row(s) updated.")

# Close the connection
conn.close()
'''
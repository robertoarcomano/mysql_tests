#!/usr/bin/python3
import mysql.connector
import time

dbconn = mysql.connector.connect(
host="localhost",
user="admin",
password="admin",
auth_plugin='mysql_native_password',
db="db"
)
mycursor = dbconn.cursor()

def execute_query(query):
  mycursor.execute(query)

# 0. Constants
NUM_ROWS=1000
NUM_INSERTS=100
TABLE="users"
NUM_COLS=1
TOT_ROWS=NUM_ROWS*NUM_INSERTS
# 1. Drop table
execute_query("drop table if exists " + TABLE)

# 2. Create table
create_table_query="create table users(id integer auto_increment,"
for i in range(0,NUM_COLS):
  create_table_query += "name"+str(i+1)+" char(100)"
  if i != NUM_COLS-1:
    create_table_query += ","
create_table_query += ",primary key(id))"
execute_query(create_table_query)

# 3. Delete from table
execute_query("delete from " + TABLE)

# 4. Insert into table
start = time.time()
for insert in range(0,NUM_INSERTS):
  insert_query = "insert into " + TABLE + " values "
  for row in range(0,NUM_ROWS): 
    n=(insert)*NUM_ROWS + row + 1
    insert_query += "(" + str(n) + ", "
    for col in range(0,NUM_COLS):
      insert_query += "'user_" + str(n) + "_" + str(col+1) + "'"
      if col != (NUM_COLS-1):
        insert_query += ","
    insert_query += ")"
    if row != (NUM_ROWS-1):
      insert_query += ","
  insert_query += ";"
  execute_query(insert_query)
execute_query("commit")
elapsed = round(time.time() - start)

print("Rows inserted: " + str(TOT_ROWS))
print("Time elapsed: " + str(elapsed) + " s")
print("Speed: " + str(round(TOT_ROWS/elapsed)) + " rows/s")

dbconn.close()


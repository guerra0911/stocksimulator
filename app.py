import database
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="GUERRA", user="postgres", password="ferrari11", port=5432)

cur = conn.cursor()     #Create Cursor

cur.close()
conn.close()


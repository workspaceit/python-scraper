import mysql.connector


cnx = mysql.connector.connect(user='root', password='1', host='localhost', database='awesome_store')
cursor = cnx.cursor()
sql = """INSERT INTO products(title, price)
         VALUES ('ABC', 2000)"""
try:
   cursor.execute(sql)
   cnx.commit()
except:
   cnx.rollback()
cnx.close()
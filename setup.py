import mysql.connector
db=mysql.connector.connect(
	host='localhost',
	username='root',
	password='1234',
	database='csprojectbank'
)
cursor=db.cursor()
q1='''CREATE TABLE customers(id int,name VARCHAR(100),username varchar(100) PRIMARY KEY,password INT,balance float,age int, gender char(1),kyc varchar(10) DEFAULT 'False',act_type varchar(15) default 'debit')'''

q2="DROP TABLE customers"

q3="SELECT * from Customers"

q4="CREATE TABLE helpcenter(name varchar(100),category varchar(20), emailid varchar(100),contactno int)"
q5="ALTER TABLE customers add acct_type varchar(10)"
q6="CREATE TABLE logs(Transaction_from varchar(100),Transaction_to varchar(100),Amount float,ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
def add_helpcenteremployee():
			n=int(input("number of employees to be added: "))
			for i in range(n):
				name,category,emailid,contactno=input("name: "),input("category: "),input("emailid: "),input("contactno: ")
				q="INSERT INTO helpcenter values(%s,%s,%s,%s)"
				cursor.execute(q,(name,category,emailid,contactno))
				db.commit()
cursor.execute("SELECT * FROM logs")

for i in cursor:
	print(i)
import random
from getpass import getpass 
import stdiomask
import mysql.connector
db=mysql.connector.connect(
	host='localhost',
	username='root',
	password='1234',
	database='csprojectbank'	
)
cursor=db.cursor()
ctr=0
bank=1
while bank==1:

	print("-"*35)
	print('''Press 1 for Online Banking
Press 2 for Registering a new bank account
Press 3 for Deleting your account
Press 4 for Customer Help Services
Press 5 for exit''')
	print("-"*35)
	choice=input("Option :- ")
	print("-"*35)
	if choice=="1":
		def welcome_message():
			print("-"*35)
			print('WELCOME TO BANK OF INDIA')
			print("-"*35)
		def login():
			while True:
				us=input("Enter your username :- ")
				try:
					p=int(stdiomask.getpass(prompt="Enter your Password: ",mask="X"))
				except Exception as error:
					print("-"*35)
					print("Error",error)
					print("PLEASE TRY AGAIN: ")
					print("-"*35)
					login()
				
				print("-"*35)
				value=(us,p)
				query="""SELECT * from customers where username=%s and password=%s """
				cursor.execute(query,value)
				data_login=cursor.fetchall()
				if len(data_login)!=0:
					globals()['ctr']=1
					break
				else:
					print('LOGIN UNSUCCSESSFUL')
					print("USERNAME OR PASSWORD IS WRONG")
					print("-"*35)
			
			return data_login
		def interface():
			welcome_message()
			b=login()
			if globals()['ctr']==1:
				i=b[0][0]
				name=b[0][2]
				print("LOGIN SUCCESSFUL")
				print("-"*35)
				c=1
				while c==1:
					print('''Press 1 for depositing money
Press 2 for withdrawing money
Press 3 for doing kyc
Press 4 for checking balance
Press 5 for Transferring money
Press 6 for logging out''')
					print("-"*35)
					ch=input("Enter your option :- ")
					if ch=="1":
						money_deposit=int(input('Amount to be deposited :- '))
						print("-"*35)
						cursor.execute("INSERT INTO logs (Transaction_from,Transaction_to,Amount)values(%s,%s,%s)",("self",name,money_deposit))
						cursor.execute('UPDATE customers set balance=balance+%s where id=%s',(money_deposit,i))
						db.commit()
						q='SELECT balance from customers where id=%s and username=%s'
						cursor.execute(q,(i,name))
						a=cursor.fetchall()
						a=a[0]
						for x in a:
							print("Updated Balance :- ",x)
							print("-"*35)
					elif ch=="2":
						money_withdrawn=int(input('Amount to be withdrawn :- '))
						cursor.execute("SELECT * from  customers where id=%s and username=%s",(i,name))
						rows=cursor.fetchall()
						if len(rows)>0:
							row=rows[0]
							atype,mbalance=row[8],row[4]
							if(atype=="debit" and mbalance<money_withdrawn):
								print("-"*35)
								print("YOU HAVE  INSUFFICIENT BALANCE")
								print("-"*35)
							elif(atype=="credit" and money_withdrawn-mbalance>10000):
								print("-"*35)
								print('''TRANSACTION FAILED!!!
YOU HAVE PASSED THE CREDIT LIMIT''')
								print("-"*35)
							else:
								print("-"*35)
								cursor.execute('UPDATE customers set balance=balance-%s where id=%s',(money_withdrawn,i))
								cursor.execute("INSERT INTO logs (Transaction_from,Transaction_to,Amount)values(%s,%s,%s)",(name,"self",money_withdrawn))
								db.commit()
								q='SELECT balance from customers where id=%s and username=%s'
								cursor.execute(q,(i,name))
								a=cursor.fetchall()
								a=a[0]
								for x in a:
									print("Updated Balance :- ",x)
								print("-"*35)
					elif ch=="3":
						q='SELECT kyc from customers where id=%s and username=%s'
						cursor.execute(q,(i,name))
						a=cursor.fetchall()
						a=a[0]
						for x in a:
							condition=x
						if condition=='false':
							print('''For KYC you need to provide details from one of these government id')
Press 1 for Aadhar Card
Press 2 for Voter Id Card
Press 3 for Pan Card
Press 4 for Driving License''')
							print("-"*35)
							cho=input("Enter your choice :- ")
							print("-"*35)
							if cho=="1":
								ad=int(input("Aadhar Number :- "))
								cursor.execute('UPDATE customers set kyc="true" where id=%s and username=%s',(i,name))
								db.commit()
								print("KYC Done")
							elif cho=="2":
								vi=int(input("Voter Id Number :- "))
								cursor.execute('UPDATE customers set kyc="true" where id=%s and username=%s',(i,name))
								db.commit()
								print("KYC Done")
							elif cho=="3":
								pc=int(input("Pan Card Number :- "))
								cursor.execute('UPDATE customers set kyc="true" where id=%s and username=%s',(i,name))
								db.commit()
								print("KYC Done")
							elif ch=="4":
								dl=int(input("Driving License Number :- "))
								cursor.execute('UPDATE customers set kyc="true" where id=%s and username=%s',(i,name))
								db.commit()
								print("KYC Done")
							else:
								print('Wrong Choice')
						else:
							print('KYC Already Done')
						print("-"*35)
					elif ch=="4":
						q='SELECT balance from customers where id=%s and username=%s'
						cursor.execute(q,(i,name))
						a=cursor.fetchall()
						a=a[0]
						for x in a:
							print("Balance :- ",x)
							print("-"*35)
					elif ch=="6":
						c=0
					elif ch=="5":
							def moneytransfer():
								usert=input("enter the username of the user you want to transfer money: ")
								amount=float(input("enter the amount of money you want to send: "))
								cursor.execute("SELECT * from  customers where id=%s and username=%s",(i,name))
								rows=cursor.fetchall()
								if len(rows)>0:
									row=rows[0]
									atype,mbalance=row[8],row[4]
									if((atype=="debit" and mbalance<amount)):
										print("-"*35)
										print("you have low balance")
										print("-"*35)
									elif(atype=="credit" and amount-mbalance>10000):
											print("-"*35)
											print('''TRANSACTION FAILED!!!
YOU HAVE PASSED THE CREDIT LIMIT''')
											print("-"*35)
											
									else:
											cursor.execute("UPDATE customers set balance=balance-%s WHERE id=%s",(amount,i))
											cursor.execute("UPDATE customers set balance=balance+%s where username=%s",(amount,usert))
											cursor.execute("INSERT INTO logs (Transaction_from,Transaction_to,Amount)values(%s,%s,%s)",(name,usert,amount))
											db.commit()
											print("-"*35)
											print('Transaction Successful')
											print("-"*35)
											
							moneytransfer()
					else:
						print("Wrong Option ")
						print("-"*35)

		interface()
	elif choice=="2":
		print('Fill these details to register your account ')
		idea=random.randint(6,1000)
		name=input("Enter your name :- ")
		username=input('Enter your username :- ')
		pas=int(input('Enter your password :- '))
		balance=float(input('Enter your balance :- '))
		age=int(input('Enter your age :- '))
		gender=input('Enter your gender (M/F) :- ')
		act_type=input("Enter the type of account you want(credit/debit):- ")
		print("-"*35)
		kyc='false'
		query='INSERT into customers values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		value=(idea,name,username,pas,balance,age,gender,kyc,act_type)
		cursor.execute(query,value)
		db.commit()
	elif choice=="3":
		def delete_act():
			us=input("Enter your username :- ")
			try:
				p=int(stdiomask.getpass("Enter your password :-"))
			except Exception as error:
						print("-"*35)
						print("Error",error)
						print("PLEASE TRY AGAIN: ")
						print("-"*35)
						delete_act()
			print("-"*35)
			value=(us,p)
			query="SELECT * from customers where username=%s and password=%s "
			cursor.execute(query,value)
			data_login=cursor.fetchall()
			cursor.execute('DELETE from customers where id=%s and username=%s',(data_login[0][0],data_login[0][2]))
			db.commit()
		delete_act()
	elif choice=="4":
		def help():
			print('Press 1 For Technical Help')
			print('Press 2 for help with banking')
			print('Press 3 for help with Loans')
			print("-"*35)
			
			hinp=input("Enter your Choice: ")
			print("-"*35)
			qtech='''SELECT name,emailid, contactno FROM helpcenter WHERE category="tech"'''
			qbanking='''SELECT name,emailid, contactno FROM helpcenter WHERE category="banking"'''
			qloans='''SELECT name,emailid, contactno FROM helpcenter WHERE category="loan"'''
			if (hinp=="1"):
				cursor.execute(qtech)
				print("Please Contact one of the following for help")
				for i in cursor:
						print(i)
						
			elif(hinp=='2'):
				cursor.execute(qbanking)
				print("Please Contact one of the following for help")
				for i in cursor:
						print(i)
			elif(hinp=='3'):
				cursor.execute(qloans)
				print("Please Contact one of the following for help")
				for i in cursor:
						print(i)
			else:
				print("Wrong Input.")
				help()

		help()
	elif choice=="5":
    		bank=0
	else:
		print('Wrong Option')
		print("-"*35)
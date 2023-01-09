"""
Project credits:
    Jacob Biju : XII B
    Sidharth S : XII B
"""

import mysql.connector as a

database, table = "shop", "inventory"

mydb = a.connect(host="localhost", user="root", passwd="tiger")

mycursor = mydb.cursor()

try:
    mycursor.execute(f"create database {database}")
    print(f"New database created: {database}")
except a.errors.DatabaseError:
    pass
	
mydb.database = "shop"

try:
    mycursor.execute(f"create table {table} (code int(4) primary key, name varchar(20), cost decimal(6, 2), quantity int(4))")
    print(f"New table crated: {table}")
except a.errors.ProgrammingError:
    pass
	
def search(code):
    mycursor.execute(f"select * from {table} where code={code}")
    data = mycursor.fetchone()
    return False if data == None else True
	
while True:
    print("---Options---\n1. View inventory\n2. Sell goods\n3. Add more goods\n4. Search for goods\n0. Exit")
    ch = int(input("Enter the number of your option: "))
	
    if ch == 1:
        print("---Viewing---")
        mycursor.execute(f"select * from {table}")
        data = mycursor.fetchall()
        print("Item code, item name, item cost, item quantity")
        total = 0
        for i in data:
            print(i)
            total += 1
        print(f"{total} items found!")
            
    elif ch == 2:
        while True:
            print("---Selling---")
            code = int(input("Enter the item code: "))
            total = 0
            if search(code):
                quantity = int(input("Enter the quantity of items you would want: "))
                mycursor.execute(f"update {table} set quantity = quantity - {quantity} where code = {code}")
                mycursor.execute(f"select cost from {table} where code = {code}")
                total += quantity*mycursor.fetchone()[0]
            else:
                print("No such  found!")
            x = input("Would you sell more items? (y/n): ")
            if x[0].lower() == "n":
                print(f"Your total cost is: {total}")
                break
                            
    elif ch == 3:
        while True:
            print("---Adding---")
            code = int(input("Enter the item code: "))
            total = 0
            quantity = int(input("Enter the quantity of items you would want: "))
            if search(code):
                mycursor.execute(f"update {table} set quantity = quantity + {quantity} where code = {code}")
            else:
                name = input("Enter the name of the product: ")
                cost = float(input("Enter the cost of the product: "))
                mycursor.execute(f"insert into {table} values ({code}, '{name}', {cost}, {quantity})")
            mycursor.execute(f"select cost from {table} where code = {code}")
            total += quantity*mycursor.fetchone()[0]
            x = input("Would you buy more items? (y/n): ")
            if x[0].lower() == "n":
                print(f"Your total cost is: {total}")
                break
    elif  ch == 4:
        print("---Searching---")
        code = int(input("Enter the item code: "))
        mycursor.execute(f"select * from {table} where code = {code}")
        data = mycursor.fetchone()
        print(data if data != None else f"No such product with code: {code}")
            
    elif ch == 69: # to be removed after development
        print("---Debug---")
        print("Shop inventory software debug mode activated!\n Here, you can directly tamper with mySQL")
        while True:
            code = input(">>>")
            if code.lower() == "exit":
                break
            elif code.lower() == "breakpoint":
                breakpoint()
                print("Broken out of break point!")
            else:
                mycursor.execute(code)
            try:
                for i in mycursor.fetchall(): print(i)
            except Exception as e:
                print(e)

    elif ch == 0:
        print("---Good bye---")
        break
                    
    else:
        print(f"No such option as {ch}!")
        
    mydb.commit()
	
mydb.close()


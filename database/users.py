import datetime
import psycopg2
from portfolio import *
from stocks import getPrice

conn = psycopg2.connect(host="localhost", dbname="GUERRA", user="postgres", password="ferrari11", port=5432)
print("Connected to the database")
cur = conn.cursor()

###ADMIN###
def createUser(username, password):
    if usernameExists(username):
        print("Username Already Exists, Please Try Again.\n")
        return
    
    if not username.isalnum():
        print("Invalid Username. Only use Numbers & Letters.\n")
        return
    
    if len(username) > 20:
        print("Username is too Long. Do not exceed 20 Characters\n")
        return

    #Pass All Checks
    #Create table for user, username, password
    cur.execute("""INSERT INTO users (username, password, balance) VALUES
                (%s, %s, %s)  
                """,
                (username, password, 0))  
    conn.commit() 
    
    print("User Successfully Created")
    
def removeUser(user):
    #Delete Table and portfolio in database
    pass

def loginUser(username, password):
    if usernameExists(username):
        verifyUserAndPass(username, password)
    else:
        print("Username Does Not Exist\n")
        return

def usernameExists(username):
    #Check to See if Username Exists in 1 row in users tabe
    cur.execute("""SELECT EXISTS (SELECT 1 FROM users WHERE
                username = %s
                )""",
                (username,))

    return cur.fetchone()[0]        #0 if Valid, 1 if Username Exists

def verifyUserAndPass(username, password):
    #Check to See if Username and Pass Exist in 1 Row
    user_data = getUserData(username)
    if user_data is not None and user_data['password'] == password:
        print("Username & Password Match\n")
    else:
        print("Username & Password do Not Match\n")
    

###USERS###
def getUserData(username):
    cur.execute("""SELECT * FROM users WHERE
                username = %s
                """,
                (username,))
    
    row = cur.fetchone()            #Store row of all user column data ('user', 'pass', data[1,2,3])

    if row is None:
        return None
    else:
        #Get the column names from the cursor description
        colnames = [desc[0] for desc in cur.description]

        #Create a dictionary that pairs column names with row data
        user_data = dict(zip(colnames, row))
        return user_data
    
        # colnames = []
        # for desc in cur.description:        
        #     #desc is a tuple containing the following elements:
        #     #desc[0]: name - The name of the column returned.
        #     #desc[1]: type_code - The PostgreSQL data type code for the column.
        #     #desc[2]: display_size - The actual length of the column in bytes.
        #     #desc[3]: internal_size - The internal size of the column in bytes.
        #     #desc[4]: precision - The precision of the column for numeric data types.
        #     #desc[5]: scale - The scale of the column for numeric data types.
        #     #desc[6]: null_ok - A flag indicating if the column can accept null values.
        #     colname = desc[0]   
        #     colnames.append(colname)

        # colData = []
        # for col in range(len(row)):                     #For Each Column in Row
        #     colData.append((colnames[col], row[col]))   #Associate the Column Name to the Data
        
        # user_data = {}
        # for pair in colData:
        #     user_data[pair[0]] = pair[1]                  #Make a map/dictionary for each column name and corresponding data
        
        # return user_data
    
def deposit(username, amount):
    changeBalance(username, amount)

def withdraw(username, amount):
    if(amount > getBalance(username)):
        print("Not Enough Funds to Withdraw this Amount")
        return
    changeBalance(username, -1*amount)

def getBalance(username):
    user_data = getUserData(username)
    print(f"User: '{username}' balance = '{user_data['balance']}'")
    return user_data['balance']

def changeBalance(username, amount):
    user_data = getUserData(username)
    currBalance = user_data['balance']
    cur.execute(""" UPDATE users
                SET balance = %s
                WHERE username = %s
                """,
                (currBalance + amount, username))
    conn.commit()

def buy(username, numShares, stock):
    cost = (numShares * getPrice(stock))
    if(cost > getBalance(username)):
        print("Not Enough Funds to Buy this Amount")
        return
    else:
        changeBalance(username, -1*cost)
        modifyPortfolio(username, "Buy", numShares, stock)

def sell(username, numShares, stock):
    revenue = numShares * getPrice(stock)
    changeBalance(username, revenue)
    modifyPortfolio(username, "Sell", numShares, stock)
    pass

def main():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL, 
                password VARCHAR(255) NOT NULL,
                balance INT NOT NULL
                );
                """)
    conn.commit()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS usersStocks (
                id SERIAL PRIMARY KEY,
                userID INT NOT NULL, 
                ticker VARCHAR(255) NOT NULL,
                numShares INT NOT NULL
                );
                """)
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS usersTransactions (
                id SERIAL PRIMARY KEY,
                userID INT NOT NULL,
                type VARCHAR(255) NOT NULL,
                ticker VARCHAR(255) NOT NULL,
                numShares INT NOT NULL, 
                price INT NOT NULL,
                date VARCHAR(255) NOT NULL
                );
                """)
    conn.commit()

    createUser("Nicholas", "Guerra")        #Create User Successfully
    
    createUser("Nicholas", "NoGuerra")      #User Name Already Exists
    createUser("Kallista-&3", "Bliss")               #User name not alpha numeric
    createUser("KallistaBliss2003RoccosantoTheQueen", "Bliss") #Username too Long

    
    loginUser("Nicholas", "Guerra")         #Login Successfully
    loginUser("Nicholas", "Bliss2003")      #Password Does not Match
    loginUser("Kallista", "Bliss")          #Username Does not Exist
    
    getBalance("Nicholas")
    deposit("Nicholas", 300)
    getBalance("Nicholas")
    withdraw("Nicholas", 5)
    getBalance("Nicholas")

    conn.commit()
  


if __name__ == "__main__":
    # Assuming you have a database connection (cur) already established
    main()
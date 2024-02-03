import datetime
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="GUERRA", user="postgres", password="ferrari11", port=5432)
print("Connected to the database")
cur = conn.cursor()

###ADMIN###
def createUser(username, password):
    if usernameExistsAlready(username):
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
    cur.execute("""INSERT INTO users (username, password) VALUES
                (%s, %s)  
                """,
                (username, password))  
    cur.commit() 
    
    print("User Successfully Created")
    
def removeUser(user):
    #Delete Table and portfolio in database
    pass

def loginUser(username, password):
    if usernameExistsAlready(username):
        verifyUserAndPass(username, password)
    else:
        print("Username Does Not Exist\n")
        return

def usernameExistsAlready(username):
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

def getBalance(user):
    #Return Balance from Database to print or display
    pass

def changeBalance(user, amount):
    #Change balance in database for sepcific user
    #Balance in Database for User += amount
    pass

def buy(user, numShares, stock):
    cost = -1 * (numShares * getPrice(stock))
    changeBalance(user, cost)
    modifyPortfolio(user, "Buy", numShares, stock)
    pass

def sell(user, numShares, stock):
    revenue = numShares * getPrice(stock)
    changeBalance(user, revenue)
    modifyPortfolio(user, "Sell", numShares, stock)
    pass


###PORTFOLIO###
def modifyPortfolio(user, type, numShares, stock):
    if type == "Buy":
        #If Stock exists, then don't append the stock, just add the numShares and price data
        pass
    else:
        #Remove Stock from Stock list, only according to # of shares and if they don't own them
        pass

    price = getPrice(stock)
    date = datetime.datetime.now()
    #Append -> Type, # SHARES, Stock, Price, Date to Portfolio Table for user
    pass

def getStockList(user):
    #Return a list of all the stocks a user owns, and how much money in each
    pass

def getTransactions(user):
    #Return a list of all the transactions a user made
    pass


###STOCKS###
def getPrice(stock):
    #Get from Database
    pass

def getPrices(stock, startDate, endDate):
    #Get list of prices and dates for a specific stock
    pass

def main():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(255), 
                password VARCHAR(255)
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

    conn.commit()
  


if __name__ == "__main__":
    # Assuming you have a database connection (cur) already established
    main()
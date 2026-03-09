import csv
import tkinter as tk
from tkinter import messagebox
import random # used only for username generation [usernames then checked if unique]
import businessAnalytics
import meals
import inbox
import accountSettings
import ordersHistory
import takeOrder


#windows
logInWin= tk.Tk()


# Global Used Variables
READONLY_BG = "#7E8181"
EDIT_BG = "#444343"


# ---------------- HELPER FUNCTIONS ----------------
# Sort a list ascendingly
def SortRecordsAscending(recordList, sortField):
    sortingList = []
    emptyList = []


    # split records
    for record in recordList:
        value = record.__dict__.get(sortField, "")
        if value == "":
            emptyList.append(record)
        else:
            sortingList.append(record)


    # bubble sort non-empty values
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(sortingList) - 1):
            if float(sortingList[i].__dict__[sortField]) > float(sortingList[i + 1].__dict__[sortField]):
                sortingList[i], sortingList[i + 1] = sortingList[i + 1], sortingList[i]
                swapped = True


    # overwrite original list
    recordList[:] = sortingList + emptyList


# Sort a list Decendingly
def SortRecordsDecending(recordList, sortField):
    sortingList = []
    emptyList = []


    # split records
    for record in recordList:
        value = record.__dict__.get(sortField, "")
        if value == "":
            emptyList.append(record)
        else:
            sortingList.append(record)


    # bubble sort non-empty values
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(sortingList) - 1):
            if float(sortingList[i].__dict__[sortField]) < float(sortingList[i + 1].__dict__[sortField]):
                sortingList[i], sortingList[i + 1] = sortingList[i + 1], sortingList[i]
                swapped = True


    # overwrite original list
    recordList[:] = sortingList + emptyList


# Filter a list  
def filterRecords(recordList, fieldName, chosenCategory):
    filteredList = []
    for record in recordList:
        value = record.__dict__.get(fieldName, "")
       
        if value == chosenCategory:
            filteredList.append(record)
    # overwrite original list
    recordList[:] = filteredList


# GENERATE SEQUENTIAL IDs
def getNextID(fileStorage):
    try:
        with open(fileStorage, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))


            if rows and fileStorage == "messagesFile.csv":
                return str(max(int(row["messageID"]) for row in rows) + 1)

            elif rows and fileStorage == "menusFile.csv":
                return str(max(int(row["menuID"]) for row in rows) + 1)

            elif rows and fileStorage == "itemsFile.csv":
                return str(max(int(row["itemID"]) for row in rows) + 1)
           
            elif rows and fileStorage == "ordersFile.csv":
                return str(max(int(row["orderID"]) for row in rows) + 1)
           
            elif rows and fileStorage == "discountsFile.csv":
                return str(max(int(row["discountsID"]) for row in rows) + 1)
           
            elif rows and fileStorage == "transactionsFile.csv":
                return str(max(int(row["transactionID"]) for row in rows) + 1)
    except FileNotFoundError:
            messagebox.showwarning("File Error", "An error occured when trying to store data!")
   
    if fileStorage == "ordersFile.csv":
        return "2000" # starting ID if file empty
    elif fileStorage == "messagesFile.csv" or fileStorage == "transactionsFile.csv":
        return "1000"
    elif fileStorage == "menusFile.csv" or fileStorage == "itemsFile.csv" or fileStorage == "discountsFile.csv":
        return 1


def createUsername(firstname, surname):
    base = firstname + surname
    extra = random.randint(10, 999)
    symbol = random.choice(["", "_", "-", "."])
    return base + symbol + str(extra)


def usernameExists(username):
    try:
        with open("usersFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    return True
    except FileNotFoundError:
        pass
    return False


def saveUser(accountDetails):
    firstname = accountDetails["firstname"]
    surname = accountDetails["surname"]
    baseUsername = firstname + surname
    username = createUsername(firstname, surname)


    counter = 1
    while usernameExists(username):
        username = baseUsername + str(counter)
        counter += 1


    accountDetails["Username"] = username
    firstThreeFields = {"Username": username,
                        "Password": accountDetails["password"],
                        "userType":accountDetails["userType"]}


    # if customer, save to customers file
    if accountDetails["userType"] == "customer":
        #save to users file
        try:
            with open("usersFile.csv", "r") as f:
                usersHasHeader = True
        except FileNotFoundError:
            usersHasHeader = False
       
        with open("usersFile.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not usersHasHeader:
                writer.writerow(firstThreeFields.keys())
            writer.writerow(firstThreeFields.values())
       
        try:
            with open("customersFile.csv", "r") as f:
                custHasHeader = True
        except FileNotFoundError:
            custHasHeader = False
       
        with open("customersFile.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not custHasHeader:
                writer.writerow(accountDetails.keys())
            writer.writerow(accountDetails.values())
       
        messagebox.showinfo("Success", "Account have been created successfully. Customer Access Granted!")
        return True
   
    elif accountDetails["userType"] in( "staff","admin"):
        return addToRequestFile(accountDetails)
         


def addToRequestFile(accountDetails):
    # save to requesters file
    try:
        with open("employeesRequests.csv", "r") as f:
            staffHasHeader = True
    except FileNotFoundError:
        staffHasHeader = False
       
    with open("employeesRequests.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not staffHasHeader:
            writer.writerow(accountDetails.keys())
        writer.writerow(accountDetails.values())
    messagebox.showinfo("Success", "Access request sent! Once approved by an admin the account will be created.")
    return True


def isAlpha(text):
    text = str(text)
    if text == "":
        return False


    for char in text:
        if char == " ":
            continue
        if not ((65 <= ord(char) <= 90) or (97 <= ord(char) <= 122)):
            return False
    return True


def isNumeric(text):
    text = str(text).strip()
    if text == "":
        return False
    for char in text:
        if not (48 <= ord(char) <= 57):
            return False
    return True


def validLength(text, minLen, maxLen):
    return minLen <= len(text) <= maxLen


userDetailsList= ["","","","","","","","","","","","","",
                  "","","","",""]


def validateUser():
    errorMessage= ""
    nonCriticalError= []
    accountDetails = {"firstname":userDetailsList[0],
                      "surname":userDetailsList[1],
                      "password":userDetailsList[2],
                      "Phone Number":userDetailsList[3],
                      "Email":userDetailsList[4],
                      "Location":userDetailsList[5],
                      "Gender":userDetailsList[6],
                      "Age":userDetailsList[7],
                      "Ethnicity":userDetailsList[8],
                      "Favourite Food":userDetailsList[9],
                      "Favourite Colour":userDetailsList[10],
                      "Known For":userDetailsList[11],
                      "userType":userDetailsList[12]}
       
    if accountDetails["firstname"] == "":
        errorMessage = "Firstname cannot be empty, and cannot leave it as 'Firstname'!"
    elif not validLength(accountDetails["firstname"], 5, 20):
        errorMessage = "Firstname must be 5–20 characters"
    elif not isAlpha(accountDetails["firstname"]):
        errorMessage = "Firstname contains invalid characters"
   
    elif accountDetails["surname"] == "":
        errorMessage = "Surname cannot be empty"
    elif not validLength(accountDetails["surname"], 5, 20):
        errorMessage = "Surname must be 5–20 characters"
    elif not isAlpha(accountDetails["surname"]):
        errorMessage = "Surname contains invalid characters"
   
    if errorMessage == "":
        if accountDetails["password"] == "":
            errorMessage = "Password cannot be empty"
        elif not validLength(accountDetails["password"], 8, 25):
            errorMessage = "Password must be 8–25 characters"
        elif " " in accountDetails["password"]:
            errorMessage = "Password cannot contain spaces"
        else:
            hasLetter = False
            hasNumber = False
            for char in accountDetails["password"]:
                if (65 <= ord(char) <= 90) or (97 <= ord(char) <= 122):
                    hasLetter = True
                elif 48 <= ord(char) <= 57:
                    hasNumber = True
            if not hasLetter:
                errorMessage = "Password must contain a letter"
            elif not hasNumber:
                errorMessage = "Password must contain a number"


    if errorMessage == "":
        if accountDetails["Phone Number"] == "":
            errorMessage = "Phone Number can't be left as empty!"
        elif not isNumeric(accountDetails["Phone Number"]):
            errorMessage = "Phone number must be numeric"
        elif len(accountDetails["Phone Number"]) != 11:
            errorMessage = "Phone number must be 11 digits"
       
    # Email
    dot = accountDetails["Email"].count(".")
    at  = accountDetails["Email"].count("@")
    if accountDetails["Email"] != "":
        if dot < 1:
            nonCriticalError= nonCriticalError + ["Email should contain at least one '.'"]
            accountDetails["Email"] = ""
        elif at != 1:
            nonCriticalError = nonCriticalError+ ["Email must contain exactly one '@'"]
            accountDetails["Email"] = ""
        elif accountDetails["Email"].index("@") > accountDetails["Email"].rindex("."):
            nonCriticalError = nonCriticalError + ["'@' must come before '.' in email"]
            accountDetails["Email"] = ""
        elif len(accountDetails["Email"]) >= 50:
                nonCriticalError = nonCriticalError + ["Email must be under 50 characters"]
                accountDetails["Email"] = ""
        accountDetails["Email"] = ""


    # ---------- LOCATION (OPTIONAL) ----------
    # Postcode is either 6 or 7 characters exculding the spaces e.g. CF10 1AA or CF1 1AA
    # not postcode.isalnum() checks for unwanted symbols like "! or ."
    if accountDetails["Location"] != "":
        postcode = accountDetails["Location"].strip().replace(" ", "")
        if not postcode.isalnum():
            nonCriticalError = nonCriticalError + ["Location/ Postcode can't have unwanted symbols (only numbers and letters): Invalid postcode format! E.g. CF10 1AA or CF1 1AA"]
            accountDetails["Location"] = ""
        elif len(postcode) not in (6,7):
            nonCriticalError = nonCriticalError + ["Incorrect length: Invalid postcode format! Postcode must be 6 or 7 characters. E.g. CF10 1AA or CF1 1AA"]
            accountDetails["Location"] = ""
        elif postcode.isdigit() or postcode.isalpha():
            nonCriticalError = nonCriticalError + ["Posatcode can't be all numbers or all letters: Invalid postcode format! Must contain both letters and numbers. E.g. CF10 1AA or CF1 1AA"]
            accountDetails["Location"] = ""
        elif len(accountDetails["Location"]) >= 50: # including spaces here 
                nonCriticalError = nonCriticalError + ["Location must be under 50 characters"]
                accountDetails["Location"] = ""

    # ---------- AGE ----------
    if accountDetails["Age"] != "":
        if not isNumeric(accountDetails["Age"]):
            nonCriticalError = nonCriticalError + ["Age must be numeric"]
            accountDetails["Age"] = ""
        else:
            accountDetails["Age"] = int(accountDetails["Age"])
            if accountDetails["Age"] < 18 or accountDetails["Age"] > 120:
                nonCriticalError = nonCriticalError + ["Age must be between 18 and 120"]
                accountDetails["Age"] = ""
            if len(str(accountDetails["Age"])) >= 50:
                nonCriticalError = nonCriticalError + ["Age must be under 50 characters"]
                accountDetails["Age"] = ""


    #---------- KNOWN FOR ----------
    if accountDetails["Known For"] != "":
        if not isNumeric(accountDetails["Known For"]):
            nonCriticalError = nonCriticalError + ["Known For must be numeric"]
            accountDetails["Known For"] = ""
        else:
            accountDetails["Known For"] = int(accountDetails["Known For"])
            if accountDetails["Known For"] < 0 or accountDetails["Known For"] > 8:
                nonCriticalError = nonCriticalError + ["Known For must be between 0 and 8 years"]
                accountDetails["Known For"] = ""
            if len(str(accountDetails["Known For"])) >= 50:
                nonCriticalError = nonCriticalError + ["Known For must be under 50 characters"]
                accountDetails["Known For"] = ""


   
    #---------- Non-required Fields ----------
    if accountDetails["Gender"] != "":
        if len(accountDetails["Gender"]) >= 50:
            nonCriticalError = nonCriticalError + ["Gender must be under 50 characters"]
            accountDetails["Gender"] = ""
    if accountDetails["Ethnicity"] != "":
        if len(accountDetails["Ethnicity"]) >= 50:
            nonCriticalError = nonCriticalError + ["Ethnicity must be under 50 characters"]
            accountDetails["Ethnicity"] = ""
    if accountDetails["Favourite Food"] != "":
        if len(accountDetails["Favourite Food"]) >= 50:
            nonCriticalError = nonCriticalError + ["Favourite Food must be under 50 characters"]
            accountDetails["Favourite Food"] = ""
    if accountDetails["Favourite Colour"] != "":
        if len(accountDetails["Favourite Colour"]) >= 50:
            nonCriticalError = nonCriticalError + ["Favourite Colour must be under 50 characters"]
            accountDetails["Favourite Colour"] = ""
   
    # ---------- STAFF / ADMIN ONLY ----------
    if accountDetails["userType"] == "staff" or accountDetails["userType"] == "admin":
        accountDetails.update({"Job Title": userDetailsList[13],"Shift": userDetailsList[14],
                               "Date Hired": userDetailsList[15],"DOB": userDetailsList[16],
                               "YOE": userDetailsList[17]})
        if accountDetails["Job Title"] == "":
            errorMessage = "Job title cannot be empty!"
        elif not validLength(accountDetails["Job Title"], 5, 20):
            errorMessage = "Job title must be 5–20 characters!"
        elif not isAlpha(accountDetails["Job Title"]):
            errorMessage = "Job title contains invalid characters!"


        elif accountDetails["Shift"] == "":
            errorMessage = "Shift cannot be empty!"
        elif accountDetails["Shift"].lower() not in ["morning","afternoon","night","anytime","other"]:
            errorMessage = "Shift must be one of the following: 'Morning','Afternoon','Night','Anytime', or 'Other'!"
        elif len(accountDetails["Shift"]) >= 50:
                nonCriticalError = nonCriticalError + ["Shift must be under 50 characters"]
                accountDetails["Shift"] = ""
       
        elif accountDetails["Date Hired"] == "" or accountDetails["DOB"] == "":
            errorMessage = "Dates cannot be empty!"
        elif len(accountDetails["Date Hired"]) >= 50:
                nonCriticalError = nonCriticalError + ["Dates must be under 50 characters"]
                accountDetails["Date Hired"] = ""
        elif len(accountDetails["DOB"]) >= 50:
                nonCriticalError = nonCriticalError + ["Dates must be under 50 characters"]
                accountDetails["DOB"] = ""
       
        else:
            for date in (accountDetails["Date Hired"], accountDetails["DOB"]):
                parts = date.split("/")
                if len(parts) != 3:
                    errorMessage = "Dates must be DD/MM/YYYY !"
                    break
                day = parts[0]
                month = parts[1]
                year = parts[2]
                if not isNumeric(day) or not isNumeric(month) or not isNumeric(year):
                    errorMessage = "Dates must be numeric DD/MM/YYYY !"
                    break
                elif int(year) <1930:
                    errorMessage = "Year can't be before 1930"
                    break
                elif int(month) > 12 or int(month) <1:
                    errorMessage = "Month must be between 1 and 12"
                    break
                elif int(day) >31 or int(day) <1:
                    errorMessage = "Day must be between 1 and 31"
                    break
       
        if len(accountDetails["YOE"]) == 0:
            errorMessage = "Years Of Experience can't be left as empty"
        elif not isNumeric(accountDetails["YOE"]):
            errorMessage = "Years Of Experience must be numeric"
        elif len(accountDetails["YOE"]) >= 50:
                nonCriticalError = nonCriticalError + ["Years Of Experience must be under 50 characters"]
                accountDetails["YOE"] = ""
        else:
            accountDetails["YOE"] = int(accountDetails["YOE"])
            if accountDetails["YOE"] < 0 or accountDetails["YOE"] > 70:
                errorMessage = "Years of experience is not logical. It must be between 0 and 70!"
   
    if errorMessage != "":
        messagebox.showerror("Error", errorMessage)
        errorMessage= ""
        return False


    if len(nonCriticalError) > 0:
        for i in range(len(nonCriticalError)):
            if not messagebox.askokcancel("Optional Information",
                                          nonCriticalError[i] + "\n\nNon-critical error:\nPress OK to ignore or Cancel to fix."):
                nonCriticalError = []
                return False
        nonCriticalError = []
   
    saveUser(accountDetails)
    for i in range (len(userDetailsList)): # empty the list before next entries
        userDetailsList[i] = ""
    return True

def loginValidate(usernameIn,passwordIn): # username exists? and password match?
    username=""
    password=""
    username=usernameIn.get()
    password=passwordIn.get()

    valid= False
    errors = 0
    errorMessage= ""
    accountDetails= {}

    if username.strip() == "":
        errors += 1
        errorMessage += "• Username cannot be empty.\n"

    if password.strip() == "":
        errors += 1
        errorMessage += "• Password cannot be empty.\n"

    # If input validation failed → show errors
    if errors > 0:
        messagebox.showerror("Error!", errorMessage)
        return
   
    try:
        with open("usersFile.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            foundUser = None
            for row in reader:
                if row["Username"] == username:
                    foundUser = row
                    break

    except FileNotFoundError:
        errors += 1
        errorMessage += "• Users file not found.\n"
        messagebox.showerror("Error!", errorMessage)
        return

    # User not found
    if not foundUser:
        errors += 1
        errorMessage += "• Username does not exist.\n"
        messagebox.showerror("Error!", errorMessage)
        return

    # Password incorrect
    if foundUser["Password"] != password:
        errors += 1
        errorMessage += "• Incorrect password.\n"
        messagebox.showerror("Error!", errorMessage)
        return

    # ---------------- AT THIS POINT LOGIN IS VALID ----------------
    if errors == 0:
        valid = True
        errorMessage = "Login successful."
        # Save user details
        accountDetails = dict(foundUser)

    # Show success or failure message
    if valid == False:
        messagebox.showerror("Error!", errorMessage)
        return
    else:
        messagebox.showinfo("Success!", errorMessage)

    # ---------------- LOAD PROFILE (BASED ON USERTYPE) ----------------
    userType = accountDetails["userType"].lower()
    profileFiles = {
        "customer": "customersFile.csv",
        "staff": "staffFile.csv",
        "admin": "adminsFile.csv"}
    profileFile = profileFiles.get(userType)

    if profileFile:
        try:
            with open(profileFile, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("Username", "").strip() == username: # previous: if row["Username"] == username:
                        accountDetails.update(row)
                        break
        except:
            pass
   
    accountDetails["userType"] = foundUser["userType"]


    # Customer_Account
    if accountDetails["userType"]== "customer": # if userType is a customer, give them customer access
        accessLevel= "customer"
     
    # Staff_Account
    elif accountDetails["userType"]== "staff": # if userType is a staff, give them customer access
        accessLevel= "staff"
   
    # Admin_Account
    elif accountDetails["userType"]== "admin": # if userType is a admin, give them customer access
        accessLevel= "admin"
    NavigationMenu(accessLevel,accountDetails)


def contactUs():
    logInWin.withdraw()
    contactWin = tk.Toplevel()
    contactWin.attributes('-fullscreen', True)
    contactWin.bind("<Escape>", lambda event: contactWin.attributes('-fullscreen', False))
    contactWin.title("Contact Us Form")
    contactWin.protocol("WM_DELETE_WINDOW", lambda: onClose(contactWin,logInWin))

    restaurantNumber = "78245678092"
    restaurantEmail = "themediterranean@deeside.co.uk"

    restaurantNumberLabel = tk.Label(contactWin, text= ("Call Our Resturant: " + restaurantNumber), font= ("Arial",30))
    restaurantNumberLabel.pack(pady=20)
   
    restaurantEmailLabel = tk.Label(contactWin, text= ("Email Our Resturant: " + restaurantEmail), font= ("Arial",20))
    restaurantEmailLabel.pack(pady=20)

    close = tk.Button(contactWin, text="Back To Login Screen",command=lambda: onClose(contactWin,logInWin))
    close.pack()


def onClose(closing_win, returning_to_win, canvas=None):  
    if messagebox.askokcancel("Go Back", "Are you sure you want to close this screen?"):
        if canvas is not None:
            canvas.unbind_all("<MouseWheel>")
        closing_win.destroy()
        returning_to_win.deiconify()


def closeApp(logInWin):
    if messagebox.askokcancel("Quit", "Do you want to exit the application?"):
        logInWin.destroy()


def togglePassword(Password):
    if Password.get() == Password.placeholder:
        return
    if Password.cget("show") == "":
        Password.config(show="*")
    else:
        Password.config(show="")


def removePlaceholder(event):
    entry = event.widget
    placeholder = entry.placeholder
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg="black")
        if hasattr(entry, "is_password") and entry.is_password:
            entry.config(show="*")


def addPlaceholder(event):
    entry = event.widget
    placeholder = entry.placeholder
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="grey")
        if hasattr(entry, "is_password") and entry.is_password:
            entry.config(show="")


def NavigationMenu(accessLevel, accountDetails):
    logInWin.withdraw()
    mainMenu = tk.Toplevel()
    mainMenu.title("Navigation Menu")
    mainMenu.attributes('-fullscreen', True)
    mainMenu.bind("<Escape>", lambda event: mainMenu.attributes('-fullscreen', False))
    mainMenu.protocol("WM_DELETE_WINDOW", lambda: onClose(mainMenu,logInWin))


    topFrame= tk.Frame(mainMenu, bg="#000000")
    topFrame.pack(pady=20)


    displayUsernameLabel = tk.Label(topFrame, text= accountDetails["Username"], bg="#7E8181",
                                    fg="white",font=("Arial", 16, "bold"), height=5, width=20)
    displayUsernameLabel.grid(row=0, column=0,padx=10)
    tk.Message(topFrame, bg="#000000").grid(row=0, column=1, padx=20)
    tk.Message(topFrame, bg="#000000").grid(row=0, column=2, padx=20)
    tk.Message(topFrame, bg="#000000").grid(row=0, column=3, padx=20)
    tk.Message(topFrame, bg="#000000").grid(row=0, column=4, padx=20)
   
    restaurantLogo = tk.PhotoImage(file="a2 project restaurant official logo2.png")
    restaurantIcon = tk.Label(topFrame, image=restaurantLogo)
    restaurantIcon.image = restaurantLogo
    restaurantIcon.grid(row=0, column=5,padx=630,pady=0)


    navigationFrame=tk.Frame(mainMenu)
    navigationFrame.pack(fill="x",pady= 10)
    navigationFrame.grid_columnconfigure(0, weight=1)
    for col in range(1, 5):
        navigationFrame.grid_columnconfigure(col, weight=0)
    navigationFrame.grid_columnconfigure(5, weight=1)


    topSpace11 = tk.Message(navigationFrame, width=5)
    topSpace11.grid(row=0, column=0,sticky="w")


    accountSettingslogo = tk.PhotoImage(file="accountSettingsLogo.png")
    accountSettingsIcon = tk.Button(navigationFrame, image=accountSettingslogo, command= lambda: accountSettings.accountSettingsWin(mainMenu,accountDetails))
    accountSettingsIcon.image = accountSettingslogo
    accountSettingsIcon.grid(row=0, column=1, padx=10, pady=5,sticky="w")
    tk.Label(navigationFrame, text="Account Settings").grid(row=1, column=1, padx=10, pady=5)


    inboxlogo = tk.PhotoImage(file="inboxLogo.png")
    inboxIcon = tk.Button(navigationFrame, image=inboxlogo, command= lambda: inbox.inboxWin(mainMenu,accountDetails))
    inboxIcon.image = inboxlogo
    inboxIcon.grid(row=0, column=2, padx=10,pady=5)
    tk.Label(navigationFrame, text="Messages Inbox").grid(row=1, column=2, padx=10, pady=5)


    mealslogo = tk.PhotoImage(file="mealsLogo.png")
    mealsIcon = tk.Button(navigationFrame, image=mealslogo, command= lambda: meals.mealsWin(mainMenu,accountDetails))
    mealsIcon.image = mealslogo
    mealsIcon.grid(row=0, column=3, padx=10,pady=5)
    tk.Label(navigationFrame, text="Meals").grid(row=1, column=3, padx=10, pady=5)


    newOrderlogo = tk.PhotoImage(file="newOrderLogo.png")
    newOrderIcon = tk.Button(navigationFrame, image=newOrderlogo, command= lambda: takeOrder.takingOrderWin(mainMenu))
    newOrderIcon.image = newOrderlogo
    newOrderIcon.grid(row=0, column=4, padx=10,pady=5)
    tk.Label(navigationFrame, text="Take Order").grid(row=1, column=4, padx=10, pady=5)

    tk.Message(navigationFrame).grid(row=0, column=5, padx=5,sticky="e")


    if accessLevel == "customer":
        ordersHistoryLogo = tk.PhotoImage(file="ordersHistoryLogo.png")
        ordersHistoryIcon = tk.Button(navigationFrame, image=ordersHistoryLogo, command= lambda: ordersHistory.ordersHistoryWin(mainMenu,accountDetails))
        ordersHistoryIcon.image = ordersHistoryLogo
        ordersHistoryIcon.grid(row=2, column=1, padx=10,pady=5)
        tk.Label(navigationFrame, text="Orders History").grid(row=3, column=1, padx=10, pady=5)
   
    elif accessLevel == "staff" or accessLevel == "admin":
        businessAnalyticsLogo = tk.PhotoImage(file="businessAnalyticsLogo.png")
        businessAnalyticsIcon = tk.Button(navigationFrame, image=businessAnalyticsLogo, command= lambda: businessAnalytics.bizAnalyticsWin(mainMenu, accountDetails))
        businessAnalyticsIcon.image = businessAnalyticsLogo
        businessAnalyticsIcon.grid(row=2, column=1, padx=10,pady=5)
        tk.Label(navigationFrame, text="Business Analytics").grid(row=3, column=1, padx=10, pady=5)


        ordersHistoryLogo = tk.PhotoImage(file="ordersHistoryLogo.png")
        ordersHistoryIcon = tk.Button(navigationFrame, image=ordersHistoryLogo, command= lambda: ordersHistory.ordersHistoryWin(mainMenu,accountDetails))
        ordersHistoryIcon.image = ordersHistoryLogo
        ordersHistoryIcon.grid(row=2, column=2, padx=10,pady=5)
        tk.Label(navigationFrame, text="Orders History").grid(row=3, column=2, padx=10, pady=5)


import csv
import tkinter as tk
from tkinter import messagebox
import navigationMenu
import signup


class Cust:
    def __init__(self, Firstname, Surname, Password, PhoneNumber, Email, Location, 
                 Gender, Age, Ethnicity, FavouriteFood, FavouriteColour, KnownFor,userType,Username):
        self.Firstname = Firstname
        self.Surname = Surname
        self.PhoneNumber = PhoneNumber
        self.Password = Password
        self.Email = Email
        self.Location = Location
        self.Gender = Gender
        self.Age = Age
        self.Ethnicity = Ethnicity
        self.FavouriteFood = FavouriteFood
        self.FavouriteColour = FavouriteColour
        self.KnownFor = KnownFor
        self.userType = userType
        
        self.Username = Username
    
    def viewCustomer(self,parentWin):
        parentWin.withdraw()
        viewWin = tk.Toplevel()
        viewWin.title("Customer Details")
        viewWin.attributes("-fullscreen", True)
        
        # ---------- SCROLLABLE LIST ----------
        container = tk.Frame(viewWin)
        container.pack(fill="both", expand=True, padx=40, pady=20)
        canvas = tk.Canvas(container, height=550, width=1100, highlightthickness=3, highlightbackground="#696767")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollableFrame = tk.Frame(canvas)
        scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="x", anchor="n")
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        fields = [("First Name", self.Firstname),("Surname", self.Surname),("Password", self.Password),
                  ("Phone Number", self.PhoneNumber),("Email", self.Email),("Location", self.Location),
                  ("Gender", self.Gender),("Age", self.Age),("Ethnicity", self.Ethnicity),
                  ("Favourite Food", self.FavouriteFood),("Favourite Colour", self.FavouriteColour),
                  ("Known For", self.KnownFor),("UserType", self.userType),("Username", self.Username)]
        
        for label, value in fields:
            tk.Label(scrollableFrame, text=label, font=("Arial",14)).pack()
            e = tk.Entry(scrollableFrame, width=100, font=("Arial",14))
            e.insert(0, value)
            e.config(state="readonly")
            e.pack(pady=5)
        
        tk.Button(viewWin, text="Back To Customers Data Page", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(viewWin, parentWin)).pack(pady=200)
        
    def addCustomer(self,parentWin):
        from signup import register 
        register(parentWin)
        
    def editCustomer(self,parentWin,gparentWin):
        parentWin.withdraw()
        editWin = tk.Toplevel()
        editWin.title("Edit Customer")
        editWin.attributes("-fullscreen", True)

        # ---------- SCROLLABLE LIST ----------
        container = tk.Frame(editWin)
        container.pack(fill="both", expand=True, padx=40, pady=20)
        canvas = tk.Canvas(container, height=550, width=1100, highlightthickness=3, highlightbackground="#696767")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollableFrame = tk.Frame(canvas)
        scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="x", anchor="n")
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        entries = {}
        fields = [
            ("Firstname", self.Firstname),
            ("Surname", self.Surname),
            ("Phone Number", self.PhoneNumber),
            ("Password", self.Password),
            ("Email", self.Email),
            ("Location", self.Location),
            ("Gender", self.Gender),
            ("Age", self.Age),
            ("Ethnicity", self.Ethnicity),
            ("Favourite Food", self.FavouriteFood),
            ("Favourite Colour", self.FavouriteColour),
            ("Known For", self.KnownFor),
            ("userType", self.userType)]

        for label, value in fields:
            tk.Label(scrollableFrame, text=label, font=("Arial",14)).pack()
            e = tk.Entry(scrollableFrame, width=100, font=("Arial",14))
            e.insert(0, value)
            e.pack(pady=3)
            entries[label] = e

        def saveChanges():
            rows = []
            with open("customersFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Username"] == self.Username:
                        for key in entries:
                            row[key] = entries[key].get()
                    rows.append(row)

            with open("customersFile.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            messagebox.showinfo("Saved", "Customer updated successfully")
            navigationMenu.onClose(editWin, parentWin)
            parentWin.destroy()
            manageCustomersStatsWin(gparentWin)

        butFrame = tk.Frame(editWin)
        butFrame.pack(pady=200)
        tk.Button(butFrame, text="Back To Customers Data Page", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(editWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Changes", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveChanges).pack(side="right")


    def deleteCustomer(self):
        rows = []
        with open("customersFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] != self.Username:
                    rows.append(row)
        if not rows:
            fieldnames = ["Firstname","Surname","Password","Phone Number","Email","Location",
                          "Gender","Age","Ethnicity","Favourite Food","Favourite Colour","Known For",
                          "userType","Username"] 
        else:
            fieldnames = rows[0].keys()
        with open("customersFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Deleted", f"Account {self.Username} deleted successfully!")


class Staff:
    def __init__(self, Firstname, Surname, Password, PhoneNumber, Email, Location, 
                 Gender, Age, Ethnicity, FavouriteFood, FavouriteColour, KnownFor,userType,
                 JobTitle,Shift,DateHired,DOB,YearsOfExperience,Username):
        self.Firstname = Firstname
        self.Surname = Surname
        self.PhoneNumber = PhoneNumber
        self.Password = Password
        self.Email = Email
        self.Location = Location
        self.Gender = Gender
        self.Age = Age
        self.Ethnicity = Ethnicity
        self.FavouriteFood = FavouriteFood
        self.FavouriteColour = FavouriteColour
        self.KnownFor = KnownFor
        self.userType = userType

        # Employee Details
        self.JobTitle = JobTitle
        self.Shift = Shift
        self.DateHired = DateHired
        self.DOB = DOB
        self.YearsOfExperience = YearsOfExperience
        
        self.Username = Username
    
    def viewStaff(self,parentWin):
        parentWin.withdraw()
        viewWin = tk.Toplevel()
        viewWin.title("Staff Details")
        viewWin.attributes("-fullscreen", True)

        # ---------- SCROLLABLE LIST ----------
        container = tk.Frame(viewWin)
        container.pack(fill="both", expand=True, padx=40, pady=20)
        canvas = tk.Canvas(container, height=550, width=1100, highlightthickness=3, highlightbackground="#696767")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollableFrame = tk.Frame(canvas)
        scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="x", anchor="n")
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        fields = [("First Name", self.Firstname),("Surname", self.Surname),("Password", self.Password),
                  ("Phone Number", self.PhoneNumber),("Email", self.Email),("Location", self.Location),
                  ("Gender", self.Gender),("Age", self.Age),("Ethnicity", self.Ethnicity),
                  ("Favourite Food", self.FavouriteFood),("Favourite Colour", self.FavouriteColour),
                  ("Known For", self.KnownFor),("UserType", self.userType),("Job Title", self.JobTitle),
                  ("Shift", self.Shift),("Date Hired", self.DateHired),("Date Of Birth", self.DOB),
                  ("Years Of Experience", self.YearsOfExperience),("Username", self.Username)]
        
        for label, value in fields:
            tk.Label(scrollableFrame, text=label, font=("Arial",14)).pack()
            e = tk.Entry(scrollableFrame, width=100, font=("Arial",14))
            e.insert(0, value)
            e.config(state="readonly")
            e.pack(pady=5)
        
        tk.Button(viewWin, text="Back To Staff Data Page", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(viewWin, parentWin)).pack(pady=200)
        
    def addStaff(self,parentWin):
        signup.register(parentWin)
        
    def editStaff(self,parentWin,gparentWin):
        parentWin.withdraw()
        editWin = tk.Toplevel()
        editWin.title("Edit Staff")
        editWin.attributes("-fullscreen", True)


        # ---------- SCROLLABLE LIST ----------
        container = tk.Frame(editWin)
        container.pack(fill="both", expand=True, padx=40, pady=20)
        canvas = tk.Canvas(container, height=550, width=1100, highlightthickness=3, highlightbackground="#696767")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollableFrame = tk.Frame(canvas)
        scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="x", anchor="n")
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        entries = {}
        fields = [("Firstname", self.Firstname),("Surname", self.Surname),("Phone Number", self.PhoneNumber),("Password", self.Password),
            ("Email", self.Email),("Location", self.Location),("Gender", self.Gender),("Age", self.Age),
            ("Ethnicity", self.Ethnicity),("Favourite Food", self.FavouriteFood),("Favourite Colour", self.FavouriteColour),
            ("Known For", self.KnownFor),("userType", self.userType),("Job Title", self.JobTitle),
            ("Shift", self.Shift),("Date Hired", self.DateHired),("DOB", self.DOB),("Years Of Experience", self.YearsOfExperience)]

        for label, value in fields:
            tk.Label(scrollableFrame, text=label, font=("Arial",14)).pack()
            e = tk.Entry(scrollableFrame, width=100, font=("Arial",14))
            e.insert(0, value)
            e.pack(pady=3)
            entries[label] = e

        def saveChanges():
            rows = []
            with open("staffFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Username"] == self.Username:
                        for key in entries:
                            row[key] = entries[key].get()
                    rows.append(row)


            with open("staffFile.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            
            messagebox.showinfo("Saved", "Staff updated successfully")
            navigationMenu.onClose(editWin, parentWin)
            parentWin.destroy()
            manageStaffStatsWin(gparentWin)

        butFrame = tk.Frame(editWin)
        butFrame.pack(pady=200)
        tk.Button(butFrame, text="Back To Staff Data Page", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(editWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Changes", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveChanges).pack(side="right")
    
    def deleteStaff(self, request):
        if not request:
            fileStorage = "staffFile.csv"
            fileStorage2= "usersFile.csv"
        else:
            fileStorage = "employeesRequests.csv"
        rows = []
        with open(fileStorage, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] != self.Username:
                    rows.append(row)
        if not rows:
            fieldnames = ["Firstname","Surname","Password","Phone Number","Email","Location",
                          "Gender","Age","Ethnicity","Favourite Food","Favourite Colour","Known For",
                          "userType","Job Title","Shift","Date Hired","Date Of Birth",
                          "Years Of Experience","Username"] 
        else:
            fieldnames = rows[0].keys()
        with open(fileStorage, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        if not request:
            rows = []
            with open(fileStorage, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Username"] != self.Username:
                        rows.append(row)
            if not rows:
                fieldnames2 = ["Username","Password","userType"]
            else:
                fieldnames = rows[0].keys()
            with open(fileStorage, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        
        if request:
            messagebox.showinfo("Deleted", f"Request for {self.Username} deleted successfully!")
        else:
            messagebox.showinfo("Deleted", f"Account {self.Username} deleted successfully!")


class Transaction:
    def __init__(self, transactionID, orderID, status, mainMenuTotal,dessertsTotal,
                 othersTotal,grandTotal,finalPrice,tax,discounts, 
                 date, paymentMethod, location, postcode):
        self.transactionID = transactionID
        self.orderID = orderID
        self.status = status
        self.mainMenuTotal = mainMenuTotal
        self.dessertsTotal = dessertsTotal
        self.othersTotal = othersTotal
        self.grandTotal = grandTotal
        self.finalPrice = finalPrice
        self.tax = tax
        self.discounts = discounts
        self.date = date
        self.paymentMethod = paymentMethod
        self.location = location
        self.postcode = postcode
    
    def viewTransaction(self,parentWin):
        parentWin.withdraw()
        viewWin = tk.Toplevel()
        viewWin.title("Transaction Details")
        viewWin.attributes("-fullscreen", True)
        
        container = tk.Frame(viewWin)
        container.pack(fill="both", expand=True, padx=40, pady=20)
        canvas = tk.Canvas(container, height=550, width=1100, highlightthickness=3, highlightbackground="#696767")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollableFrame = tk.Frame(canvas)
        scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="x", anchor="n")
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        fields = [("Transaction ID", self.transactionID),("Order ID", self.orderID),("Status", self.status),
                  ("Main Menu Total", self.mainMenuTotal),("Desserts Total", self.dessertsTotal),
                  ("Other Menu Categories Total", self.othersTotal),
                  ("Grand Total", self.grandTotal),("Final Price", self.finalPrice),("Tax", self.tax),
                  ("Discount(s)", self.discounts),("Date", self.date),("Payment Method", self.paymentMethod),
                  ("Location", self.location),("Postcode", self.postcode)]
        
        for label, value in fields:
            tk.Label(scrollableFrame, text=label, font=("Arial",14)).pack()
            e = tk.Entry(scrollableFrame, width=100, font=("Arial",14))
            e.insert(0, value)
            e.config(state="readonly")
            e.pack(pady=5)
        
        tk.Button(viewWin, text="Back To Transactions Data Page", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(viewWin, parentWin)).pack(pady=200)


    def editTransaction(self,parentWin,gparentWin):
        parentWin.withdraw()
        editWin = tk.Toplevel()
        editWin.title("Edit Transaction")
        editWin.attributes("-fullscreen", True)
        
        frame = tk.Frame(editWin)
        frame.pack(pady=40)

        statusE = tk.Entry(frame, width=40)
        dateE = tk.Entry(frame, width=40)
        paymentE = tk.Entry(frame, width=40)
        locationE = tk.Entry(frame, width=40)
        postcodeE = tk.Entry(frame, width=40)

        statusE.insert(0, self.status)
        dateE.insert(0, self.date)
        paymentE.insert(0, self.paymentMethod)
        locationE.insert(0, self.location)
        postcodeE.insert(0, self.postcode)

        for w, t in [(statusE,"Status"),(dateE, "Date"),(paymentE, "Payment Method"),(locationE, "Location"),(postcodeE, "Postcode")]:
            tk.Label(frame, text=t).pack()
            w.pack(pady=5)

        def saveChanges():
            if str(statusE.get()).strip().lower() not in ("paid","refunded"):
                messagebox.showerror("Error", "Transaction Status must only be 'Paid' or 'Refunded'")
                return False
            if len(str(statusE.get())) == 0 or len(str(dateE.get())) == 0 or len(str(paymentE.get())) == 0 or len(str(locationE.get())) == 0 or len(str(postcodeE.get())) == 0:
                messagebox.showerror("Error", "Can't leave any fields as empty!")
                return False
            rows = []
            with open("transactionsFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["date"] == self.date and row["postcode"] == self.postcode:
                        row["status"] = statusE.get()
                        row["date"] = dateE.get()
                        row["paymentMethod"] = paymentE.get()
                        row["location"] = locationE.get()
                        row["postcode"] = postcodeE.get()
                    rows.append(row)


            with open("transactionsFile.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            messagebox.showinfo("Saved", "Transaction updated successfully")
            navigationMenu.onClose(editWin, parentWin)
            parentWin.destroy()
            manageSalesStatsWin(gparentWin)
        
        butFrame = tk.Frame(editWin)
        butFrame.pack(pady=40)
        tk.Button(butFrame, text="Back To Transactions Data Page", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(editWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Changes", width=25, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveChanges).pack(side="right")
    
    def deleteTransaction(self):
        rows = []
        with open("transactionsFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            transactionFieldnames = reader.fieldnames

            for row in reader:
                if row["transactionID"] != self.transactionID:
                    rows.append(row)
                else:
                    orderIDToDelete = row["orderID"]  # linked order

        with open("transactionsFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=transactionFieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        remainingOrders = []
        with open("ordersFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            orderFieldnames = reader.fieldnames


            for row in reader:
                if row["orderID"] != orderIDToDelete:
                    remainingOrders.append(row)


        with open("ordersFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=orderFieldnames)
            writer.writeheader()
            writer.writerows(remainingOrders)


        messagebox.showinfo("Deleted",
                            f"Transaction {self.transactionID} and Order {orderIDToDelete} deleted successfully!")




def manageCustomersStatsWin(analyticsNavigationWin):
    analyticsNavigationWin.withdraw()
    custStatsScreen = tk.Toplevel()
    custStatsScreen.title("Customers Records & Statistics Screen")
    custStatsScreen.attributes('-fullscreen', True)
    custStatsScreen.bind("<Escape>", lambda event: custStatsScreen.attributes('-fullscreen', False))
    custStatsScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(custStatsScreen,analyticsNavigationWin))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(custStatsScreen,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    custStatsLogo = tk.PhotoImage(file="custStatsLogo.png")  
    custStatsIcon = tk.Label(logoFrame, image=custStatsLogo,bg="#7E8181")
    custStatsIcon.image = custStatsLogo
    custStatsIcon.pack(side="left")


    tk.Label(logoFrame, text="Customers Records", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="      ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(custStatsScreen)
    container.pack(fill="both", expand=True, padx=40, pady=20)
    canvas = tk.Canvas(container,height=300, width= 1100,highlightthickness=3,highlightbackground="#696767",bg="#4fa5d0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)


    scrollableFrame = tk.Frame(canvas,bg="#ffffff")
    scrollableFrame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="x", anchor="n")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",lambda ev: canvas.yview_scroll(-1*(ev.delta//120), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    # ---------- LOAD customers ----------
    custObjects = []
    try:
        with open("customersFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                custObjects.append(Cust(row["Firstname"], row["Surname"], row["Password"],
                                         row["Phone Number"],row["Email"],row["Location"],
                                         row["Gender"],row["Age"],row["Ethnicity"],row["Favourite Food"],
                                         row["Favourite Colour"],row["Known For"],row["userType"],row["Username"]))
    except FileNotFoundError:
        messagebox.showerror("Error", "Customers file not found")
        return False


    # ---------- ROW SELECTION ----------
    selected = {"object": None, "widgets": []}


    def selectRow(custObj, widgets):
        # Reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")
        # Highlight current
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
        selected["object"] = custObj
        selected["widgets"] = widgets


   # ---------- RENDER ROWS (FIX: extracted rendering logic) ----------
    def displayCustomers(customers):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(customers):
            rowWidgets = []
            values = [obj.Username, obj.Firstname, obj.Surname, obj.PhoneNumber,
                      obj.Age,obj.KnownFor]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=15)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")


                # ---------- FIX: correct lambda capture ----------
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayCustomers(custObjects)
    
    # ---------- SEARCH ----------
    searchFrame = tk.Frame(custStatsScreen)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Customer (Username / Name / Phone):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchCustomer():
        query = searchEntry.get().strip().lower()
        if not query:
            displayCustomers(custObjects)
            return
        results = []
        for c in custObjects:
            if (query in c.Username.lower() or query in c.Firstname.lower() or query in c.Surname.lower()
                or query in c.PhoneNumber.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Customer not found")
            return
        displayCustomers(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchCustomer).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayCustomers(custObjects)).pack(side="left")


    def refreshCustStats():
        custStatsScreen.destroy()
        manageCustomersStatsWin(analyticsNavigationWin)


    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a customer first")
            return
        selected["object"].viewCustomer(custStatsScreen)
    
    def addCustomer():
        Cust("", "", "", "", "", "", "", "", 
              "", "", "", "", "", "").addCustomer(custStatsScreen)
    
    def editCustomer():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a customer first")
            return
        selected["object"].editCustomer(custStatsScreen,analyticsNavigationWin)


    def deleteCustomer():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a customer first")
            return
        selected["object"].deleteCustomer()
        refreshCustStats() # refreshes the page
    
    def sortCustomers():
        sortWin = tk.Toplevel(custStatsScreen)
        sortWin.title("Sort Customers")
        sortWin.geometry("900x300")
        sortWin.grab_set()
        tk.Label(sortWin, text="Sort customers by:", font=("Arial", 12, "bold")).pack(pady=10)


        def sortAndRefresh(field):
            navigationMenu.SortRecordsAscending(custObjects, field)
            displayCustomers(custObjects)
            sortWin.destroy()


        def sortAndRefreshDecending(field):
            navigationMenu.SortRecordsDecending(custObjects, field)
            displayCustomers(custObjects)
            sortWin.destroy()
        
        tk.Button(sortWin,text="Age (Ascending)",width=20,command=lambda: sortAndRefresh("Age")).pack(pady=5)
        tk.Button(sortWin,text="Known For (Ascending)",width=20,command=lambda: sortAndRefresh("KnownFor")).pack(pady=5)


        tk.Button(sortWin,text="Age (Decending)",width=20,command=lambda: sortAndRefreshDecending("Age")).pack(pady=5)
        tk.Button(sortWin,text="Known For (Decending)",width=20,command=lambda: sortAndRefreshDecending("KnownFor")).pack(pady=5)
    
    # ---------- BUTTONS ----------
    butFrame= tk.Frame(custStatsScreen)
    butFrame.pack(pady=40)
    tk.Button(butFrame, text="View Customer Details", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=20)
    tk.Button(butFrame, text="Edit Customer", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=editCustomer).pack(side="left", padx=20)
    tk.Button(butFrame, text="Add Customer", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=addCustomer).pack(side="right", padx=20)
    tk.Button(butFrame, text="Delete Customer", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=deleteCustomer).pack(side="right", padx=20)
    
    butFrame2= tk.Frame(custStatsScreen)
    butFrame2.pack(pady=40)
    tk.Button(butFrame2, text="Back To Analytics Navigation", width=25,height=2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(custStatsScreen,analyticsNavigationWin)).pack(side="left",anchor="w",padx=10)
    tk.Button(butFrame2, text="Sort Customers", width=20,height=2,font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=sortCustomers).pack(side="right", padx=10)


    
def manageRequestsWin(StaffStatsWin, refreshCallback=None):
    StaffStatsWin.withdraw()
    manageRequestsScreen = tk.Toplevel()
    manageRequestsScreen.title("Manage Requests Screen")
    manageRequestsScreen.attributes('-fullscreen', True)
    manageRequestsScreen.bind("<Escape>", lambda event: manageRequestsScreen.attributes('-fullscreen', False))


    def handleClose():
        navigationMenu.onClose(manageRequestsScreen, StaffStatsWin)
        if refreshCallback:
            refreshCallback()  # refresh parent safely


    manageRequestsScreen.protocol("WM_DELETE_WINDOW", handleClose)


    topFrame= tk.Frame(manageRequestsScreen)
    topFrame.pack(fill="x")
    staffStatsLogo = tk.PhotoImage(file="staffStatsLogo.png")
    staffStatsIcon = tk.Label(topFrame, image=staffStatsLogo)
    staffStatsIcon.image = staffStatsLogo 
    staffStatsIcon.pack(anchor="w")


    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(manageRequestsScreen)
    container.pack(fill="both", expand=True, padx=40, pady=20)
    canvas = tk.Canvas(container,height=300, width= 1100,highlightthickness=3,highlightbackground="#696767",bg="#4fa5d0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)


    scrollableFrame = tk.Frame(canvas,bg="#ffffff")
    scrollableFrame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="x", anchor="n")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",lambda ev: canvas.yview_scroll(-1*(ev.delta//120), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    # ---------- LOAD Staff ----------
    staffObjects = []
    staffRawData = []
    try:
        with open("employeesRequests.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                staffObjects.append(Staff(row["Firstname"], row["Surname"], row["Password"],
                                         row["Phone Number"],row["Email"],row["Location"],
                                         row["Gender"],row["Age"],row["Ethnicity"],row["Favourite Food"],
                                         row["Favourite Colour"],row["Known For"],row["userType"],
                                         row["Job Title"],row["Shift"],row["Date Hired"],row["Date Of Birth"],
                                         row["Years Of Experience"],row["Username"]))
                staffRawData.append(row)
                
    except FileNotFoundError:
        messagebox.showerror("Error", "employeesRequests file not found")
        return False


    # ---------- ROW SELECTION ----------
    selected = {"object": None, "widgets": [], "row": None} 
    def selectRow(requesterObj, widgets,row):
        # Reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")
        # Highlight current
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
        selected["object"] = requesterObj
        selected["widgets"] = widgets
        selected["row"] = row


    # ---------- RENDER ROWS (FIX: extracted rendering logic) ----------
    def displayRequest(requester):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(requester):
            rowWidgets = []
            values = [obj.Username, obj.Firstname, obj.Surname, obj.PhoneNumber]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=20)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")


                # ---------- FIX: correct lambda capture ----------
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets, row=staffRawData[r]: selectRow(o, w,row))
                rowWidgets.append(entry)
    displayRequest(staffObjects)


    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Staff first")
            return
        selected["object"].viewStaff(manageRequestsScreen)
    
    def acceptRequester():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Staff first")
            return 
        
        firstThreeFields = {"Username": selected["object"].Username,
                      "Password": selected["object"].Password,
                      "userType":selected["object"].userType}


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
        
        
        # save to staff / admin file
        if selected["object"].userType == "staff":
            fileStorage = "staffFile.csv"
        elif selected["object"].userType == "admin":
            fileStorage = "adminsFile.csv"


        try:
            with open(fileStorage, "r", newline="", encoding="utf-8") as f:
                fileHasHeader = True
        except FileNotFoundError:
            fileHasHeader = False


        with open(fileStorage, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=selected["row"].keys())
            if not fileHasHeader:
                writer.writeheader()
            writer.writerow(selected["row"])
        
        # remove from request file now 
        remainingRows = []


        with open("employeesRequests.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["Username"] != selected["object"].Username:
                    remainingRows.append(row)


        with open("employeesRequests.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(remainingRows)
        
        handleClose()


    def rejectRequester():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Staff first")
            return
        selected["object"].deleteStaff(True)
        handleClose()
    
    butFrame= tk.Frame(manageRequestsScreen)
    butFrame.pack(pady=50)


    # ---------- BUTTON PACK ----------
    closeWin= tk.Button(butFrame, width=25, text="Back To Staff Records", height = 2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command= handleClose)
    closeWin.pack(side="left",padx=5)
    tk.Button(butFrame, text="View Request Details", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=10)
    tk.Button(butFrame, text="Accept Request", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=acceptRequester).pack(side="right", padx=10)
    tk.Button(butFrame, text="Reject Request", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=rejectRequester).pack(side="right", padx=10)




def manageStaffStatsWin(analyticsNavigationWin):
    analyticsNavigationWin.withdraw()
    staffStatsScreen = tk.Toplevel()
    staffStatsScreen.title("Staff Records & Statistics Screen")
    staffStatsScreen.attributes('-fullscreen', True)
    staffStatsScreen.bind("<Escape>", lambda event: staffStatsScreen.attributes('-fullscreen', False))
    staffStatsScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(staffStatsScreen,analyticsNavigationWin))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(staffStatsScreen,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    staffStatsLogo = tk.PhotoImage(file="staffStatsLogo.png")  
    staffStatsIcon = tk.Label(logoFrame, image=staffStatsLogo,bg="#7E8181")
    staffStatsIcon.image = staffStatsLogo
    staffStatsIcon.pack(side="left")


    tk.Label(logoFrame, text="Staff Records", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="      ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(staffStatsScreen)
    container.pack(fill="both", expand=True, padx=40, pady=20)
    canvas = tk.Canvas(container,height=300, width= 1100,highlightthickness=3,highlightbackground="#696767",bg="#4fa5d0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)


    scrollableFrame = tk.Frame(canvas,bg="#ffffff")
    scrollableFrame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="x", anchor="n")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",lambda ev: canvas.yview_scroll(-1*(ev.delta//120), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    # ---------- LOAD Staff ----------
    staffObjects = []
    try:
        with open("staffFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                staffObjects.append(Staff(row["Firstname"], row["Surname"], row["Password"],
                                         row["Phone Number"],row["Email"],row["Location"],
                                         row["Gender"],row["Age"],row["Ethnicity"],row["Favourite Food"],
                                         row["Favourite Colour"],row["Known For"],row["userType"],
                                         row["Job Title"],row["Shift"],row["Date Hired"],row["Date Of Birth"],
                                         row["Years Of Experience"],row["Username"]))
    except FileNotFoundError:
        messagebox.showerror("Error", "Staff file not found")
        return False


    # ---------- ROW SELECTION ----------
    selected = {"object": None, "widgets": []}


    def selectRow(staffObj, widgets):
        # Reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")
        # Highlight current
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
        selected["object"] = staffObj
        selected["widgets"] = widgets


    # ---------- RENDER ROWS (FIX: extracted rendering logic) ----------
    def displayStaff(staff):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(staff):
            rowWidgets = []
            values = [obj.Username, obj.Firstname, obj.Surname, obj.PhoneNumber,
                      obj.Age,obj.KnownFor,obj.YearsOfExperience]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=12)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")


                # ---------- FIX: correct lambda capture ----------
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayStaff(staffObjects)
    
    # ---------- SEARCH ----------
    searchFrame = tk.Frame(staffStatsScreen)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Staff (By Username / Firstname:").pack(side="left")
    tk.Label(searchFrame,text="/ Surname / Phone Number):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchStaff():
        query = searchEntry.get().strip().lower()
        if not query:
            displayStaff(staffObjects)
            return
        results = []
        for c in staffObjects:
            if (query in c.Username.lower() or query in c.Firstname.lower() or query in c.Surname.lower()
                or query in c.PhoneNumber.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Staff not found")
            return
        displayStaff(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchStaff).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayStaff(staffObjects)).pack(side="left")


    def refreshStaffStats():
        staffStatsScreen.destroy()
        manageStaffStatsWin(analyticsNavigationWin)


    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Staff first")
            return
        selected["object"].viewStaff(staffStatsScreen)
    
    
    def addStaff():
        Staff("", "", "", "", "", "", "", "", 
              "", "", "", "", "", "", 
              "", "", "", "", "").addStaff(staffStatsScreen)


    def editStaff():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Staff first")
            return
        selected["object"].editStaff(staffStatsScreen,analyticsNavigationWin)
    
    def deleteStaff():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Staff first")
            return
        selected["object"].deleteStaff(False)
        refreshStaffStats() # refreshes the page 
        
    def manageRequest():
        manageRequestsWin(staffStatsScreen, refreshCallback=refreshStaffStats) # refreshes the page
    
    def sortStaff():
        sortWin = tk.Toplevel(staffStatsScreen)
        sortWin.title("Sort Staff")
        sortWin.geometry("900x300")
        sortWin.grab_set()
        tk.Label(sortWin, text="Sort Staff by:", font=("Arial", 12, "bold")).pack(pady=10)


        def sortAndRefresh(field):
            navigationMenu.SortRecordsAscending(staffObjects, field)
            displayStaff(staffObjects)
            sortWin.destroy()


        def sortAndRefreshDecending(field):
            navigationMenu.SortRecordsDecending(staffObjects, field)
            displayStaff(staffObjects)
            sortWin.destroy()
        tk.Button(sortWin,text="Age (Ascending)",width=20,command=lambda: sortAndRefresh("Age")).pack(pady=5)
        tk.Button(sortWin,text="Known For (Ascending)",width=20,command=lambda: sortAndRefresh("KnownFor")).pack(pady=5)
        tk.Button(sortWin,text="Years Of Experience (Ascending)",width=25,command=lambda: sortAndRefresh("YearsOfExperience")).pack(pady=5)
        
        tk.Button(sortWin,text="Age (Decending)",width=20,command=lambda: sortAndRefreshDecending("Age")).pack(pady=5)
        tk.Button(sortWin,text="Known For (Decending)",width=20,command=lambda: sortAndRefreshDecending("KnownFor")).pack(pady=5)
        tk.Button(sortWin,text="Years Of Experience (Decending)",width=25,command=lambda: sortAndRefreshDecending("YearsOfExperience")).pack(pady=5)


    
    # ---------- BUTTONS ----------
    butFrame= tk.Frame(staffStatsScreen)
    butFrame.pack(pady=40)
    tk.Button(butFrame, text="View Staff Details", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=20)
    tk.Button(butFrame, text="Edit Staff", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=editStaff).pack(side="left", padx=20)
    tk.Button(butFrame, text="Add Staff", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=addStaff).pack(side="right", padx=20)
    tk.Button(butFrame, text="Delete Staff", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=deleteStaff).pack(side="right", padx=20)
    
    butFrame2= tk.Frame(staffStatsScreen)
    butFrame2.pack(pady=40)
    tk.Button(butFrame2, text="Back To Analytics Navigation",width=25,height=2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(staffStatsScreen,analyticsNavigationWin)).pack(side="left",anchor="w",padx=10)
    tk.Button(butFrame2, text="Manage Access Requests",width=25,height=2,font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command= manageRequest).pack(side="left", padx=10)
    tk.Button(butFrame2, text="Sort Staff",width=15,height=2,font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=sortStaff).pack(side="right", padx=10)


def addDiscountWin(SalesStatsWin):
    SalesStatsWin.withdraw()
    discountsCreationScreen = tk.Toplevel()
    discountsCreationScreen.title("Discounts Creation Screen")
    discountsCreationScreen.attributes('-fullscreen', True)
    discountsCreationScreen.bind("<Escape>", lambda event: discountsCreationScreen.attributes('-fullscreen', False))
    discountsCreationScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(discountsCreationScreen, SalesStatsWin))


    def AddDiscount():
        error = False 


        if len(discountCodeEntry.get()) == 0:
            error = True
            errorMessage = "All fields must be filled"
        elif len(discountAmountEntry.get()) == 0:
            error = True
            errorMessage = "All fields must be filled"
        elif len(discountQuantityEntry.get()) == 0:
            error = True
            errorMessage = "All fields must be filled"


        # ---------- FIX: numeric validation ----------
        try:
            discountAmount = float(discountAmountEntry.get())
            discountQuantity = int(discountQuantityEntry.get())
        except ValueError:
            error = True
            errorMessage = "Discount amount and quantity must be numeric!"


        if error == False:
            discountsID = navigationMenu.getNextID("discountsFile.csv")  # FIX: moved after validation


            rows = []


            # ---------- FIX: handle file not existing ----------
            try:
                with open("discountsFile.csv", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    for row in reader:
                        rows.append(row)
            except FileNotFoundError:
                fieldnames = ["discountsID", "discountCode", "discountAmount", "discountQuantity"] 


            # ---------- FIX: record must be a dict ----------
            record = {"discountsID": discountsID,"discountCode": discountCodeEntry.get(),
                "discountAmount": discountAmount,"discountQuantity": discountQuantity}


            rows.append(record)


            # ---------- FIX: write ALL rows, not record ----------
            with open("discountsFile.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)


            messagebox.showinfo("Info", "Discounts have been successfully added!")
            return True
        else:
            messagebox.showerror("Error", errorMessage)

    #, padx=50,pady=20

    mainFrame= tk.Frame(discountsCreationScreen)
    mainFrame.pack(fill="x", padx=400, pady=200)

    tk.Label(mainFrame, text="Discount Code:",font=("Arial", 24,"bold")).grid(row=0, column=0)
    discountCodeEntry = tk.Entry(mainFrame,width=50)
    discountCodeEntry.grid(row=0, column=1, ipady=5)


    tk.Label(mainFrame, text="Discount Amount:",font=("Arial", 24,"bold")).grid(row=1, column=0)
    discountAmountEntry = tk.Entry(mainFrame,width=50)
    discountAmountEntry.grid(row=1, column=1, ipady=5)


    tk.Label(mainFrame, text="Discount Quantity:",font=("Arial", 24,"bold")).grid(row=2, column=0)
    discountQuantityEntry = tk.Entry(mainFrame,width=50)
    discountQuantityEntry.grid(row=2, column=1, ipady=5)


    # ---------- FIX: actually CALL the Function ----------
    tk.Button(mainFrame,text="Add Discount To The System",width=30,height=2,font=("Arial", 12,"bold"),
              command=AddDiscount).grid(row=2, column=2, padx=25)
    
    closeWin= tk.Button(mainFrame,text="Back To Sales Records",width=30,height=2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(discountsCreationScreen, SalesStatsWin))
    closeWin.grid(row=3, column=0, sticky="w", padx=50, pady=40)


    
def manageSalesStatsWin(analyticsNavigationWin):
    analyticsNavigationWin.withdraw()
    salesStatsScreen = tk.Toplevel()
    salesStatsScreen.title("Sales Records & Statistics Screen")
    salesStatsScreen.attributes('-fullscreen', True)
    salesStatsScreen.bind("<Escape>", lambda event: salesStatsScreen.attributes('-fullscreen', False))
    salesStatsScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(salesStatsScreen,analyticsNavigationWin))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(salesStatsScreen,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    salesStatsLogo = tk.PhotoImage(file="salesStatsLogo.png")  
    salesStatsIcon = tk.Label(logoFrame, image=salesStatsLogo,bg="#7E8181")
    salesStatsIcon.image = salesStatsLogo
    salesStatsIcon.pack(side="left")


    tk.Label(logoFrame, text="Sales Records", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="      ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(salesStatsScreen)
    container.pack(fill="both", expand=True, padx=40, pady=20)
    canvas = tk.Canvas(container,height=300, width= 1100,highlightthickness=3,highlightbackground="#696767",bg="#4fa5d0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)


    scrollableFrame = tk.Frame(canvas,bg="#ffffff")
    scrollableFrame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="x", anchor="n")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",lambda ev: canvas.yview_scroll(-1*(ev.delta//120), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    # ---------- LOAD Transactions ----------
    tranObjects = []
    try:
        with open("transactionsFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tranObjects.append(Transaction(row["transactionID"], row["orderID"],row["status"],
                                               row["mainMenuTotal"],row["dessertsTotal"],row["othersTotal"],
                                               row["grandTotal"],row["finalPrice"],row["tax"],row["discounts"],
                                               row["date"],row["paymentMethod"],row["location"],row["postcode"]))
    except FileNotFoundError:
        messagebox.showerror("Error", "Transactions file not found")
        return False


    # ---------- ROW SELECTION ----------
    selected = {"object": None, "widgets": []}


    def selectRow(staffObj, widgets):
        # Reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")
        # Highlight current
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
        selected["object"] = staffObj
        selected["widgets"] = widgets


    # ---------- RENDER ROWS (FIX: extracted rendering logic) ----------
    def displayTransactions(Transactions):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(Transactions):
            rowWidgets = []
            finalPrice= "£" + str(obj.finalPrice)
            values = [obj.transactionID, obj.status, obj.date, finalPrice, obj.paymentMethod, 
                      obj.tax,obj.discounts]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=12)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")


                # ---------- FIX: correct lambda capture ----------
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayTransactions(tranObjects)
    
    # ---------- SEARCH ----------
    searchFrame = tk.Frame(salesStatsScreen)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Transaction (By transactionID / orderID:").pack(side="left")
    tk.Label(searchFrame,text="/ status / date / paymentMethod):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchTransaction():
        query = searchEntry.get().strip().lower()
        if not query:
            displayTransactions(tranObjects)
            return
        results = []
        for c in tranObjects:
            if (query in c.transactionID or query in c.orderID or query in c.status.lower() or query in c.date.lower()
                or query in c.paymentMethod.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Transaction not found")
            return
        displayTransactions(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchTransaction).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayTransactions(tranObjects)).pack(side="left")


    def refreshSalesStats():
        salesStatsScreen.destroy()
        manageSalesStatsWin(analyticsNavigationWin)


    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Transaction first")
            return
        selected["object"].viewTransaction(salesStatsScreen)


    def editTransaction():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Transaction first")
            return
        selected["object"].editTransaction(salesStatsScreen,analyticsNavigationWin)


    def deleteTransaction():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a Transaction first")
            return
        selected["object"].deleteTransaction()
        refreshSalesStats() # refreshes the page 
    
    def sortTransactions():
        sortWin = tk.Toplevel(salesStatsScreen)
        sortWin.title("Sort Transactions")
        sortWin.geometry("1200x600")
        sortWin.grab_set()
        tk.Label(sortWin, text="Sort Transactions by:", font=("Arial", 12, "bold")).pack(pady=10)


        def sortAndRefresh(field):
            navigationMenu.SortRecordsAscending(tranObjects, field)
            displayTransactions(tranObjects)
            sortWin.destroy()


        def sortAndRefreshDecending(field):
            navigationMenu.SortRecordsDecending(tranObjects, field)
            displayTransactions(tranObjects)
            sortWin.destroy()
            
        tk.Button(sortWin,text="Final_Price (Ascending)",width=20,command=lambda: sortAndRefresh("finalPrice")).pack(pady=5)
        tk.Button(sortWin,text="Tax (Ascending)",width=20,command=lambda: sortAndRefresh("tax")).pack(pady=5)
        tk.Button(sortWin,text="Discounts (Ascending)",width=20,command=lambda: sortAndRefresh("discounts")).pack(pady=5)
        tk.Button(sortWin,text="Main_Menu Total (Ascending)",width=25,command=lambda: sortAndRefresh("mainMenuTotal")).pack(pady=5)
        tk.Button(sortWin,text="Desserts Total (Ascending)",width=20,command=lambda: sortAndRefresh("dessertsTotal")).pack(pady=5)
        tk.Button(sortWin,text="Others Total (Ascending)",width=20,command=lambda: sortAndRefresh("othersTotal")).pack(pady=5)
        tk.Button(sortWin,text="Grand Total (Ascending)",width=20,command=lambda: sortAndRefresh("grandTotal")).pack(pady=5)


        tk.Button(sortWin,text="Final_Price (Desending)",width=20,command=lambda: sortAndRefreshDecending("finalPrice")).pack(pady=5)
        tk.Button(sortWin,text="Tax (Desending)",width=20,command=lambda: sortAndRefreshDecending("tax")).pack(pady=5)
        tk.Button(sortWin,text="Discounts (Desending)",width=20,command=lambda: sortAndRefreshDecending("discounts")).pack(pady=5)
        tk.Button(sortWin,text="Main_Menu Total (Desending)",width=25,command=lambda: sortAndRefreshDecending("mainMenuTotal")).pack(pady=5)
        tk.Button(sortWin,text="Desserts Total (Desending)",width=20,command=lambda: sortAndRefreshDecending("dessertsTotal")).pack(pady=5)
        tk.Button(sortWin,text="Others Total (Desending)",width=20,command=lambda: sortAndRefreshDecending("othersTotal")).pack(pady=5)
        tk.Button(sortWin,text="Grand Total (Desending)",width=20,command=lambda: sortAndRefreshDecending("grandTotal")).pack(pady=5)
    
    # ---------- BUTTONS ----------
    butFrame= tk.Frame(salesStatsScreen)
    butFrame.pack(pady=40)
    tk.Button(butFrame, text="View Transaction Details", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=20)
    tk.Button(butFrame, text="Edit Transaction", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=editTransaction).pack(side="left", padx=20)
    tk.Button(butFrame, text="Add A Discount", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command= lambda: addDiscountWin(salesStatsScreen)).pack(side="right", padx=20)
    tk.Button(butFrame, text="Delete Transaction", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=deleteTransaction).pack(side="right", padx=20)
    
    butFrame2= tk.Frame(salesStatsScreen)
    butFrame2.pack(pady=40)
    tk.Button(butFrame2, text="Back To Analytics Navigation",width=25,height=2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(salesStatsScreen,analyticsNavigationWin)).pack(side= "left",anchor="w",padx=10)
    tk.Button(butFrame2, text="Sort Transactions", width=25,height=2,font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=sortTransactions).pack(side="right", padx=10)




def viewGeneralStatsWin(analyticsNavigationWin, accounDetails):
    analyticsNavigationWin.withdraw()
    generalStatsScreen = tk.Toplevel()
    generalStatsScreen.title("General Statistics Screen")
    generalStatsScreen.attributes('-fullscreen', True)
    generalStatsScreen.bind("<Escape>", lambda event: generalStatsScreen.attributes('-fullscreen', False))
    generalStatsScreen.protocol("WM_DELETE_WINDOW",lambda: navigationMenu.onClose(generalStatsScreen, analyticsNavigationWin))


    # ---------------- TOP BAR ---------------- 
    topFrame = tk.Frame(generalStatsScreen,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    generalStatsLogo = tk.PhotoImage(file="salesStatsLogo.png")  
    generalStatsIcon = tk.Label(logoFrame, image=generalStatsLogo,bg="#7E8181")
    generalStatsIcon.image = generalStatsLogo
    generalStatsIcon.pack(side="left")


    tk.Label(logoFrame, text="General Statistics & Reports", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)
    
    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(generalStatsScreen)
    container.pack(fill="both", expand=True, padx=40, pady=10)
    canvas = tk.Canvas(container, height=500, width=1100, highlightthickness=3, highlightbackground="#696767")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollableFrame = tk.Frame(canvas)
    scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="x", anchor="n")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    
    # ---------- STATS FRAME ----------
    statsFrame = tk.Frame(scrollableFrame)
    statsFrame.pack()


    def safeInt(v):
        try:
            return int(v)
        except:
            return 0


    # =====================================================
    # CUSTOMER STATS
    # =====================================================
    customerCount = 0
    totalCustomerAge = 0
    genderCount = {}
    locationCount = {}


    try:
        with open("customersFile.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                customerCount += 1
                age = safeInt(row["Age"])
                totalCustomerAge += age


                gender = row["Gender"]
                location = row["Location"]


                genderCount[gender] = genderCount.get(gender, 0) + 1
                locationCount[location] = locationCount.get(location, 0) + 1
    except FileNotFoundError:
        messagebox.showerror("Error", "customersFile.csv not found")


    avgCustomerAge = round(totalCustomerAge / customerCount, 1) if customerCount else 0
    mostCommonLocation = max(locationCount, key=locationCount.get) if locationCount else "N/A"


    # =====================================================
    # STAFF STATS
    # =====================================================
    staffCount = 0
    totalStaffAge = 0
    totalExperience = 0
    jobTitles = {}


    try:
        with open("staffFile.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                staffCount += 1
                totalStaffAge += safeInt(row["Age"])
                totalExperience += safeInt(row["Years Of Experience"])


                job = row["Job Title"]
                jobTitles[job] = jobTitles.get(job, 0) + 1
    except FileNotFoundError:
        messagebox.showerror("Error", "staffFile.csv not found")


    avgStaffAge = round(totalStaffAge / staffCount, 1) if staffCount else 0
    avgExperience = round(totalExperience / staffCount, 1) if staffCount else 0


    adminsCount= 0 
    AdminsTotalExperience= 0
    AdminsJobTitles = {}
    try:
        with open("adminsFile.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                adminsCount += 1
                AdminsTotalExperience += safeInt(row["Years Of Experience"])


                job = row["Job Title"]
                AdminsJobTitles[job] = AdminsJobTitles.get(job, 0) + 1
    except FileNotFoundError:
        messagebox.showerror("Error", "adminsFile.csv not found")
    
    AdminAvgExperience = round(AdminsTotalExperience / staffCount, 1) if staffCount else 0


    # =====================================================
    # TRANSACTION STATS
    # =====================================================
    transactionCount = 0
    totalRevenue = 0.0
    paymentMethods = {}
    itemCounts = {}
    top3PopularItems = []
    hoursCount= {}
    peakHours= []
    
    try:
        with open("transactionsFile.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactionCount += 1
                if row["status"] == "Paid":
                    totalRevenue += float(row["finalPrice"]) 


                method = row["paymentMethod"]
                paymentMethods[method] = paymentMethods.get(method, 0) + 1


                # ---------- PEAK HOURS ----------
                
                dateTime = row["date"]           # Example: "03/10/2025 10:45"
                timePart = dateTime.split(" ")[1]  # "10:45"
                hour = timePart.split(":")[0]      # "10"
                hoursCount[hour] = hoursCount.get(hour, 0) + 1


                
    except FileNotFoundError:
        messagebox.showerror("Error", "transactionsFile.csv not found")




    try:
        with open("ordersFile.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # ---------- ITEMS ----------
                rawItems = row["items"]


                # clean + split (handles: "item1, item2" or "['item1','item2']")
                rawItems = rawItems.strip("[]")
                items = [i.strip().strip("'").strip('"') for i in rawItems.split(",") if i.strip()]


                for item in items:
                    itemCounts[item] = itemCounts.get(item, 0) + 1
    except FileNotFoundError:
        messagebox.showerror("Error", "ordersFile.csv not found")


    avgOrderValue = round(totalRevenue / transactionCount, 2) if transactionCount else 0
    mostUsedPayment = max(paymentMethods, key=paymentMethods.get) if paymentMethods else "N/A"
    #mostPopularItem = max(itemCounts, key=itemCounts.get) if itemCounts else "N/A"
    
    tempItemCounts = itemCounts.copy()  # IMPORTANT: don't destroy original data
    for _ in range(3):
        if not tempItemCounts:
            break
        
        maxItem = None
        maxCount = -1
        for item, count in tempItemCounts.items():
            if count > maxCount:
                maxCount = count
                maxItem = item
        
        top3PopularItems.append((maxItem, maxCount))
        del tempItemCounts[maxItem]  # remove so next max is different
    
    tempHours = hoursCount.copy()
    for _ in range(3):
        if not tempHours:
            break
        
        maxHour = None
        maxCount = -1
        for hour, count in tempHours.items():
            if count > maxCount:
                maxCount = count
                maxHour = hour
        
        peakHours.append((maxHour, maxCount))
        del tempHours[maxHour]
    
    # =====================================================
    # DISPLAY RESULTS
    # =====================================================
    def section(title):
        tk.Label(statsFrame, text=title, font=("Arial", 18, "bold"), width=70,anchor="center",bg="black",fg="white").pack(pady=(10, 5))


    def stat(text):
        tk.Label(statsFrame, text=text, font=("Arial", 14), width=70,anchor="center",bg="grey",fg="white").pack()


    section("Customer Statistics")
    stat(f"Total Customers: {customerCount}")
    stat(f"Average Customer Age: {avgCustomerAge}")
    stat(f"Most Common Location: {mostCommonLocation}")
    for g, c in genderCount.items():
        if g == "":
            g = "Not Provided"
        g = "Gender-" + str(g)
        stat(f"{g}: {c}")


    section("Staff Statistics")
    stat(f"Total Staff Members: {staffCount}")
    stat(f"Average Staff Age: {avgStaffAge}")
    stat(f"Average Years of Experience: {avgExperience}")
    stat("Most common Staff roles:")
    for job, c in jobTitles.items():
        stat(f"{job}: {c}")
    
    if accounDetails["userType"] == "admin":
        stat("Admins Statistics")
        stat(f"Total Admins Count: {adminsCount}")
        stat(f"Admins' Average Years of Experience: {AdminAvgExperience}")
        stat("Most common Admins roles:")
        for job, c in AdminsJobTitles.items():
            stat(f"{job}: {c}")
    
    section("Transaction Statistics")
    # only admins can see sensitive data like revenue and total transactions 
    if accounDetails["userType"] == "admin": 
        stat(f"Total Transactions: {transactionCount}")
        stat(f"Total Revenue: £{totalRevenue:.2f}")
        
        if top3PopularItems:
            stat("Most Popular Items:")
            for Item, count in top3PopularItems:
                stat(f"{Item} -- {count} items")
        else:
            stat("Most Popular Items: N/A")
        
        if peakHours:
            stat("Peak Transaction Hours:")
            for hour, count in peakHours:
                stat(f"{hour}:00 – {hour}:59 → {count} transactions")
        else:
            stat("Peak Transaction Hours: N/A")
    # other transactions data is accessible to all staff and admins 
    stat(f"Average Order Value: £{avgOrderValue}")
    stat(f"Most Used Payment Method: {mostUsedPayment}")


    butFrame= tk.Frame(generalStatsScreen)
    butFrame.pack(pady=10, fill="x")
    closeWin= tk.Button(butFrame, width=25, text="Back To Analytics Navigation", height = 2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(generalStatsScreen,analyticsNavigationWin))
    closeWin.pack(anchor="w",padx=5)




def bizAnalyticsWin(mainMenu, accountDetails):
    mainMenu.withdraw()
    bizAnalyticsScreen = tk.Toplevel()
    bizAnalyticsScreen.title("Business Analytics Screen")
    bizAnalyticsScreen.attributes('-fullscreen', True)
    bizAnalyticsScreen.bind("<Escape>", lambda event: bizAnalyticsScreen.attributes('-fullscreen', False))
    bizAnalyticsScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(bizAnalyticsScreen,mainMenu))


    AccessType = accountDetails["userType"]


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(bizAnalyticsScreen,bg="#000000")
    topFrame.pack(fill="x",pady=10)
    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    businessAnalyticsLogo = tk.PhotoImage(file="businessAnalyticsLogo2.png")
    businessAnalyticsIcon = tk.Label(logoFrame, image=businessAnalyticsLogo,bg="#7E8181")
    businessAnalyticsIcon.image = businessAnalyticsLogo
    businessAnalyticsIcon.pack(side="left")


    tk.Label(logoFrame, text="Business Statistics & Reports", font=("Arial", 24, "bold"),
             bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    manageCustomersStatsFrame= tk.Frame(bizAnalyticsScreen, bg="lightblue")
    manageCustomersStatsFrame.pack(pady=10)
    manageCustStats = tk.Button(manageCustomersStatsFrame, width=43, text="Customers Statistics", height = 3, command= lambda: manageCustomersStatsWin(bizAnalyticsScreen))
    manageCustStats.grid(row=0,column=0,padx=15,pady=5)


    custStatsLogo = tk.PhotoImage(file="custStatsLogo.png")
    custStatsIcon = tk.Label(manageCustomersStatsFrame,image=custStatsLogo)
    custStatsIcon.image = custStatsLogo
    custStatsIcon.grid(row=0, column=1, padx=5,pady=5)


    if AccessType == "admin":
        manageStaffStatsFrame= tk.Frame(bizAnalyticsScreen, bg="lightgreen")
        manageStaffStatsFrame.pack(pady=10)
        manageStaffStats = tk.Button(manageStaffStatsFrame, width=43, text="Staff Statistics", height = 3, command= lambda: manageStaffStatsWin(bizAnalyticsScreen))
        manageStaffStats.grid(row=0,column=0,padx=15,pady=5)
        
        staffStatsLogo = tk.PhotoImage(file="staffStatsLogo.png")
        staffStatsIcon = tk.Label(manageStaffStatsFrame,image=staffStatsLogo)
        staffStatsIcon.image = staffStatsLogo
        staffStatsIcon.grid(row=0, column=1, padx=5,pady=5)
        
        manageSalesStatsFrame= tk.Frame(bizAnalyticsScreen, bg="yellow")
        manageSalesStatsFrame.pack(pady=10)
        manageSalesStats = tk.Button(manageSalesStatsFrame, width=43, text="Sales Statistics", height = 3, command= lambda: manageSalesStatsWin(bizAnalyticsScreen))
        manageSalesStats.grid(row=0,column=0,padx=15,pady=5)
        
        salesStatsLogo = tk.PhotoImage(file="salesStatsLogo.png")
        salesStatsIcon = tk.Label(manageSalesStatsFrame,image=salesStatsLogo)
        salesStatsIcon.image = salesStatsLogo
        salesStatsIcon.grid(row=0, column=1, padx=5,pady=5)
    
    viewGeneralStatsFrame= tk.Frame(bizAnalyticsScreen, bg="red")
    viewGeneralStatsFrame.pack(pady=10)
    viewGeneralStats = tk.Button(viewGeneralStatsFrame, width=43, text="General Statistics", height = 3, command= lambda: viewGeneralStatsWin(bizAnalyticsScreen, accountDetails))
    viewGeneralStats.grid(row=0,column=0,padx=15,pady=5)


    generalStatsLogo = tk.PhotoImage(file="generalStatsLogo.png")
    generalStatsIcon = tk.Label(viewGeneralStatsFrame,image=generalStatsLogo)
    generalStatsIcon.image = generalStatsLogo
    generalStatsIcon.grid(row=0, column=1, padx=5,pady=5)
   
    butFrame= tk.Frame(bizAnalyticsScreen)
    butFrame.pack(pady=30, fill="x")
    closeWin= tk.Button(butFrame, width=25, text="Go Back To Navigation Menu", height = 2,
                        font=("Arial", 12,"bold"),bg="#171717", fg="white",
                        command=lambda: navigationMenu.onClose(bizAnalyticsScreen,mainMenu))
    closeWin.pack(anchor="w",padx=5)


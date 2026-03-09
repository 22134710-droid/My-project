import csv
import tkinter as tk
from tkinter import messagebox
import navigationMenu


def enableEdit(entries, cancelBtn):
    for field in entries:
        if field != "Username":
            entries[field].config(state="normal", bg=navigationMenu.EDIT_BG)
    cancelBtn.grid()


def cancelEdit(entries, originalValues, cancelBtn):
    for field in entries:
        #entries[field].config(state="normal")
        entries[field].delete(0, "end")
        entries[field].insert(0, originalValues[field])
        entries[field].config(state="readonly", readonlybackground=navigationMenu.READONLY_BG)
    cancelBtn.grid_remove()


def saveChanges(entries, cancelBtn, accountDetails):
    for field in entries:
        if field in accountDetails:
            accountDetails[field] = entries[field].get()
   
    for field in entries:
        entries[field].config(state="readonly", readonlybackground=navigationMenu.READONLY_BG)
    cancelBtn.grid_remove()


    userType = accountDetails["userType"]
    username = accountDetails["Username"]


    if userType == "admin":
        fileStorage = "adminsFile.csv"
    elif userType == "staff":
        fileStorage = "staffFile.csv"
    elif userType == "customer":
        fileStorage = "customersFile.csv"
    else:
        messagebox.showerror("Error", "Invalid user type")
        return


    rows = []
    updated = False


    try:
        with open(fileStorage, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames


            if not fieldnames:
                messagebox.showerror("Error","Your account could not be found in memory.")
                return


            for row in reader:
                if row.get("Username") == username:
                    for field in entries:
                        if field in row:
                            row[field] = entries[field].get()
                    updated = True
                rows.append(row)


    except FileNotFoundError:
        messagebox.showerror("Error","Account storage file not found.")
        return


    if not updated:
        messagebox.showerror("Error","Your account could not be found in memory.")
        return


    with open(fileStorage, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)
    messagebox.showinfo("Saved","Account details updated successfully.")




def deleteAccountAction(accountSettingsWin, mainMenu, accountDetails):
    if messagebox.askyesno("Confirm", "Are you sure you want to delete your account??"):


        # ---------- USERS FILE ----------
        fileStorage = "usersFile.csv"
        remainingUsers = []


        with open(fileStorage, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["Username"] != accountDetails["Username"]:
                    remainingUsers.append(row)


        with open(fileStorage, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()                              
            writer.writerows(remainingUsers)


        # ---------- ROLE-SPECIFIC FILE ----------
        if accountDetails["userType"] == "customer":
            fileStorage = "customersFile.csv"
        elif accountDetails["userType"] == "staff":
            fileStorage = "staffFile.csv"
        elif accountDetails["userType"] == "admin":
            fileStorage = "adminsFile.csv"


        remainingUsers = []


        with open(fileStorage, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["Username"] != accountDetails["Username"]:
                    remainingUsers.append(row)


        with open(fileStorage, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(remainingUsers)
       
        accountSettingsWin.destroy()
        mainMenu.destroy()
        navigationMenu.logInWin.deiconify()




def accountSettingsWin(mainMenu, accountDetails):
    mainMenu.withdraw()
    settingsScreen = tk.Toplevel()
    settingsScreen.title("Account Settings Menu")
    settingsScreen.attributes('-fullscreen', True)
    settingsScreen.bind("<Escape>", lambda event: settingsScreen.attributes('-fullscreen', False))
    settingsScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(settingsScreen,mainMenu,canvas))
   
    topFrame= tk.Frame(settingsScreen,bg="#000000")
    topFrame.pack(fill="x")
    topFrame.grid_columnconfigure(1, weight=1)


    accountLabelFrame= tk.Frame(topFrame, bg="#7E8181")
    accountLabelFrame.grid(row=0,column=0,pady=10)


    tk.Message(topFrame,bg="#000000").grid(row=0,column=1,padx=200)


    accountSettingsLogo = tk.PhotoImage(file="accountSettingsLogo2.png") # is 75% size of 1st 
    accountSettingsIcon = tk.Label(accountLabelFrame, image=accountSettingsLogo, bg="#7E8181")
    accountSettingsIcon.image = accountSettingsLogo
    accountSettingsIcon.grid(row=0, column=0, sticky="w")


    tk.Label(accountLabelFrame,text="Account Settings",font=("Arial", 22, "bold"), bg="#7E8181",
             fg="white").grid(row=0,column=1, padx=20,sticky="w")
   
    canvas = tk.Canvas(settingsScreen)
    scrollbar = tk.Scrollbar(settingsScreen, orient="vertical", command=canvas.yview)
   
    scrollableFrame = tk.Frame(canvas)
    scrollableFrame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    def onMousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    settingsScreen.bind_all("<MouseWheel>", onMousewheel)


    fieldsFrame = tk.Frame(scrollableFrame)
    fieldsFrame.pack(pady=20)


    entries = {}
    row = 0
    for field, value in accountDetails.items():
        label = tk.Label(fieldsFrame, text=field, font=("Arial", 12))
        label.grid(row=row, column=0, padx=20, pady=8, sticky="e")
       
        if field == "Password":
            PassEntry = tk.Entry(fieldsFrame, font=("Arial", 12), show="*",width=90)
            PassEntry.placeholder = "Password"
            PassEntry.is_password = True
            PassEntry.insert(0, value)
            PassEntry.bind("<FocusIn>", navigationMenu.removePlaceholder)
            PassEntry.bind("<FocusOut>", navigationMenu.addPlaceholder)
            PassEntry.config(state="readonly",readonlybackground=navigationMenu.READONLY_BG)
            PassEntry.grid(row=row, column=1, padx=20, pady=8, ipady=4,sticky="w")
           
            showBtn = tk.Button(fieldsFrame,text="Show Password",width=15,
                                command=lambda: navigationMenu.togglePassword(PassEntry)) # btn
            showBtn.grid(row=row, column=2, padx=10)
            entries[field] = PassEntry


        else:
            entry = tk.Entry(fieldsFrame, font=("Arial", 12),width=90)
            entry.insert(0, value)
            entry.config(state="readonly",readonlybackground=navigationMenu.READONLY_BG)
            entry.grid(row=row, column=1, padx=20, pady=8, ipady=4,sticky="w")
            entries[field] = entry
       
        row += 1


    butFrame= tk.Frame(scrollableFrame)
    butFrame.pack(pady=20)
    editBut = tk.Button(butFrame,text="Edit Details",width=25,height=2,
                        font=("Arial", 12,"bold"),bg="#171717", fg="white",command=lambda: enableEdit(entries,cancelBtn))
    editBut.grid(row=0, column=0, padx=20)
    saveBut = tk.Button(butFrame,text="Save Changes",width=25,height=2,
                        font=("Arial", 12,"bold"),bg="#171717", fg="white",command=lambda: saveChanges(entries,cancelBtn, accountDetails))
    saveBut.grid(row=0, column=1)


    cancelBtn = tk.Button(butFrame,text="Cancel",width=20,height=2,
                          font=("Arial", 12,"bold"),bg="#171717", fg="white",command=lambda: cancelEdit(entries, originalValues, cancelBtn))
    cancelBtn.grid(row=0, column=2, padx=15)
    cancelBtn.grid_remove()
   
    originalValues = {}
    for field in entries:
        originalValues[field] = entries[field].get()
   
    closeWin= tk.Button(butFrame, width=25, text="Go Back To Navigation Menu", height = 2,
                        font=("Arial", 12,"bold"),bg="#171717", fg="white",command=lambda: navigationMenu.onClose(settingsScreen,mainMenu,canvas))
    closeWin.grid(row=2, column=0, pady=25, padx=5)


    if accountDetails["userType"] != "staff":
        deleteAccount = tk.Button(butFrame, width=25, text="Delete Account", height = 2,
                                  font=("Arial", 12,"bold"),bg="#171717", fg="white",command=lambda: deleteAccountAction(settingsScreen,mainMenu,accountDetails))
        deleteAccount.grid(row=2, column=2, pady=25)


    logOut = tk.Button(butFrame, width=25, text="Log Out", height = 2,
                       font=("Arial", 12,"bold"),bg="#171717", fg="white",command=lambda: navigationMenu.onClose(settingsScreen,navigationMenu.logInWin,canvas))
    logOut.grid(row=2, column=1, pady=25, padx=15)


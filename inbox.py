import csv
import tkinter as tk
from tkinter import messagebox
import datetime
import navigationMenu


# ---------------- INBOX WINDOW ----------------
def inboxWin(mainMenu, accountDetails):
    mainMenu.withdraw()
    inbox = tk.Toplevel()
    inbox.title("Inbox")
    inbox.attributes('-fullscreen', True)
    inbox.bind("<Escape>", lambda e: inbox.attributes('-fullscreen', False))
    inbox.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(inbox, mainMenu))
   
    username = accountDetails["Username"]
    accessLevel = accountDetails["userType"]
   
    topFrame = tk.Frame(inbox,bg="#000000")
    topFrame.pack(fill="x")
    accountLabelFrame= tk.Frame(topFrame, bg="#7E8181")
    accountLabelFrame.grid(row=0,column=0,pady=10)
    tk.Message(topFrame,bg="#000000").grid(row=0,column=1,padx=200)


    inboxlogo = tk.PhotoImage(file="inboxLogo2.png") # 75% of the 1st
    inboxIcon = tk.Label(accountLabelFrame, image=inboxlogo,bg="#000000")
    inboxIcon.image = inboxlogo
    inboxIcon.grid(row=0, column=0, padx=10,pady=5)


    tk.Label(accountLabelFrame,text="Inbox",font=("Arial", 22, "bold"), bg="#7E8181",
             fg="white").grid(row=0,column=1, padx=20,sticky="w")
    tk.Label(accountLabelFrame,text="                     ",font=("Arial", 22, "bold"), bg="#7E8181",
             fg="white").grid(row=0,column=2, padx=20,sticky="w")


    # ---------------- BUTTONS ----------------
    btnFrame = tk.Frame(inbox)
    btnFrame.pack(fill="x", pady=10)
   
    tk.Button(btnFrame, text="Go Back To Navigation Menu", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(inbox, mainMenu),width=25).pack(side="left", padx=5)
    tk.Button(btnFrame, text="View Message", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: viewMessage()).pack(side="left", padx=5)
    tk.Button(btnFrame, text="Delete Message", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: deleteMessage(accessLevel)).pack(side="left", padx=5)
    tk.Button(btnFrame, text="Reply", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: replyMessage(accessLevel)).pack(side="left", padx=5)
    tk.Button(btnFrame, text="Send a Message", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: openSendMessage(inbox,username,accessLevel)).pack(side="left", padx=5)


    # ---------------- LIST ----------------
    listFrame = tk.Frame(inbox)
    listFrame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(listFrame)
    scrollbar.pack(side="right", fill="y")


    messagesList = tk.Listbox(listFrame,font=("Arial",25))
    messagesList.pack(side="left", fill="both", expand=True)
    messagesList.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=messagesList.yview)


    messagesData = []


    # ---------------- LOAD MESSAGES ----------------
    def loadMessages():
        messagesList.delete(0, tk.END)
        messagesData.clear()
        try:
            with open("messagesFile.csv", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["receiverID"] == username:
                        messagesData.append(row)


            messagesData.reverse()
            for row in messagesData:
                messagesList.insert(tk.END,f"FROM: {row['senderID']} | {row['dateTime']}")
        except FileNotFoundError:
            messagesList.insert(tk.END, "messagesFile.csv NOT FOUND")
       
    loadMessages()


    # ---------------- HELPERS ----------------
    def getSelectedMessage():
        if not messagesList.curselection():
            return None
        return messagesData[messagesList.curselection()[0]]


    # ---------------- VIEW ----------------
    def viewMessage():
        msg = getSelectedMessage()
        if not msg:
            messagebox.showerror("Error", "No message selected!")
            return


        inbox.withdraw()
        win = tk.Toplevel()
        win.title("View Message")
        win.attributes('-fullscreen', True)
        win.bind("<Escape>", lambda e: win.attributes('-fullscreen', False))
        win.protocol("WM_DELETE_WINDOW", lambda: (win.destroy(), inbox.deiconify()))


        tk.Button(win, text="Back", command=lambda: (win.destroy(), inbox.deiconify())).pack(anchor="w", padx=10, pady=5)
        tk.Label(win, text=f"From: {msg['senderID']}").pack(anchor="w", padx=10)
        tk.Label(win, text=f"Date: {msg['dateTime']}").pack(anchor="w", padx=10)
        textBox = tk.Text(win, wrap="word")
        textBox.pack(fill="both", expand=True, padx=10, pady=10)
        textBox.insert("1.0", msg["content"])
        textBox.config(state="disabled")


    # ---------------- DELETE ----------------
    def deleteMessage(UserAccessLevel):
        msg = getSelectedMessage()
        if not msg:
            messagebox.showerror("Error", "No message selected!")
            return
       
        senderType = None
        try:
            with open("usersFile.csv", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Username"] == msg["senderID"]:
                        senderType = row["userType"]
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "usersFile.csv not found")
            return
       
        if UserAccessLevel == "staff" and senderType == "admin":
            messagebox.showerror("Access Denied",
                                 "You are not allowed to delete messages sent by admins!")
            return


        if not messagebox.askyesno("Confirm", "Delete this message?"):
            return
        with open("messagesFile.csv", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        rows = [r for r in rows if r["messageID"] != msg["messageID"]]
        with open("messagesFile.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys(), quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows)
        loadMessages()


    # ---------------- REPLY ----------------
    def replyMessage(UserAccessLevel):
        msg = getSelectedMessage()
        if not msg:
            messagebox.showerror("Error", "No message selected!")
            return
        
        senderType = None
        try:
            with open("usersFile.csv", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Username"] == msg["senderID"]:
                        senderType = row["userType"]
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "usersFile.csv not found")
            return
       
        if UserAccessLevel == "staff" and senderType == "admin":
            messagebox.showerror("Access Denied",
                                 "You cannot reply to an admin's message!")
            return
        
        receiver = msg["senderID"]
        inbox.withdraw()
        openComposeWindow(inbox, username, receiver,reply=True)


# ---------------- SEND A MESSAGE ----------------
def openSendMessage(parent, senderUsername, SenderAccessLevel):
    parent.withdraw()
    sendWin = tk.Toplevel()
    sendWin.title("Send a Message")
    sendWin.attributes('-fullscreen', True)
    sendWin.bind("<Escape>", lambda e: sendWin.attributes('-fullscreen', False))
    sendWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(sendWin, parent))


    topFrame = tk.Frame(sendWin,bg="#000000")
    topFrame.pack(fill="x")
    accountLabelFrame= tk.Frame(topFrame, bg="#7E8181")
    accountLabelFrame.grid(row=0,column=0,pady=10)


    tk.Message(topFrame,bg="#000000").grid(row=0,column=1,padx=200)
    inboxlogo = tk.PhotoImage(file="inboxLogo2.png") # 75% of the 1st
    inboxIcon = tk.Label(accountLabelFrame, image=inboxlogo,bg="#000000")
    inboxIcon.image = inboxlogo
    inboxIcon.grid(row=0, column=0, padx=10,pady=5)


    tk.Label(accountLabelFrame,text="Sending A Message",font=("Arial", 22, "bold"), bg="#7E8181",
             fg="white").grid(row=0,column=1, padx=20,sticky="w")
    tk.Label(accountLabelFrame,text="            ",font=("Arial", 22, "bold"), bg="#7E8181",
             fg="white").grid(row=0,column=2, padx=20,sticky="w")


    tk.Button(sendWin,text="Back",font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: (sendWin.destroy(), parent.deiconify())).pack(anchor="w", padx=10, pady=5)


    tk.Label(sendWin, text="Select a staff or admin user:").pack(anchor="w", padx=10)


    listFrame = tk.Frame(sendWin)
    listFrame.pack(fill="both", expand=True, padx=10, pady=5)


    scrollbar = tk.Scrollbar(listFrame)
    scrollbar.pack(side="right", fill="y")


    usersList = tk.Listbox(listFrame)
    usersList.pack(side="left", fill="both", expand=True)
    usersList.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=usersList.yview)


    usersData = []          # staff/admin
    customerData = []       # customers (for search fallback)


    # ---------- LOAD USERS ----------
    def setList():
        usersList.delete(0, tk.END)
        usersData.clear()
        customerData.clear()
        try:
            with open("usersFile.csv", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["userType"] in ("staff", "admin"):
                        usersData.append(row)
                        usersList.insert(tk.END, row["Username"])
                    elif row["userType"] == "customer":
                        customerData.append(row)
        except FileNotFoundError:
            usersList.insert(tk.END, "usersFile.csv NOT FOUND")


    setList()


    # ---------- SELECT USER ----------
    def selectUser():
        accessType= "Allowed"
        if not usersList.curselection():
            messagebox.showwarning("Select User", "Please select a user!")
            return False
        receiverAL = ""
        receiver = usersList.get(usersList.curselection()[0])
        with open("usersFile.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == receiver:
                    receiverAL = row["userType"]

        if senderUsername== receiver:
            messagebox.showwarning("Select User", "You cannot send a message to yourself!")
            return False

        elif SenderAccessLevel== "customer" and receiverAL == "customer":
            messagebox.showwarning("Select User", "You're not allowed to send messages to other customers!")
            return False
        
        else:
            sendWin.withdraw()
            openComposeWindow(sendWin, senderUsername, receiver)


    tk.Button(sendWin, text="Select User", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=selectUser).pack(pady=10)


    # ---------- SEARCH ----------
    searchFrame = tk.Frame(sendWin)
    searchFrame.pack(pady=10)


    tk.Label(searchFrame, text="Search a username:").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchUser():
        query = searchEntry.get().strip().lower()
        if not query:
            setList()
            return


        usersList.delete(0, tk.END)
        found = False


        # search staff/admin first
        for user in usersData:
            if query == user["Username"].lower():
                usersList.insert(tk.END, user["Username"])
                found = True


        # fallback: search customers
        if not found:
            for user in customerData:
                if query == user["Username"].lower():
                    usersList.insert(tk.END, user["Username"])
                    found = True
                    break


        if not found:
            messagebox.showerror("Error", "Username not found!")
            setList()


    tk.Button(searchFrame,text="Search A User",width=12,font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=searchUser).pack(side="left", padx=5)




# ---------------- COMPOSE / REPLY WINDOW ----------------
def openComposeWindow(parent, sender, receiver,reply=False):
    composeWin = tk.Toplevel()
    composeWin.title("Compose Message")
    composeWin.attributes('-fullscreen', True)
    composeWin.bind("<Escape>", lambda e: composeWin.attributes('-fullscreen', False))
    composeWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(composeWin, parent))


    tk.Button(composeWin, text="Cancel Message", font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(composeWin, parent)).pack(anchor="w", padx=10, pady=5)
   
    LabelFrame= tk.Frame(composeWin,bg="#171717")
    LabelFrame.pack(pady=5)
    LabelBackgroundFrame= tk.Frame(LabelFrame,bg="#FFFFFF")
    LabelBackgroundFrame.pack(padx=10,pady=5)
    tk.Label(LabelBackgroundFrame, text="Message Body",bg="#FFFFFF",fg="grey",
             font=("Arial",12,"bold")).pack(anchor="w", padx=265, pady=5)
   
    BodyFrame= tk.Frame(composeWin,bg="#171717")
    BodyFrame.pack(pady=5)
    tk.Label(BodyFrame, text=f"To: {receiver}").pack(anchor="w", padx=10, pady=5)


    textBox = tk.Text(BodyFrame, wrap="word")
    textBox.pack(fill="both", expand=True, padx=10, pady=10)


    if reply:
        textBox.insert("1.0", "Responding:\n")
        textBox.tag_add("bold", "1.0", "1.11")
        textBox.tag_config("bold", font=("TkDefaultFont", 10, "bold"), background="yellow")
        textBox.mark_set("insert", "2.0")


    def sendMessage():
        content = textBox.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty Message", "Message content cannot be empty.")
            return


        rows = []
        try:
            with open("messagesFile.csv", newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
        except FileNotFoundError:
            messagebox.showwarning("File Error", "An error has occured!")
            return


        messageID = navigationMenu.getNextID("messagesFile.csv")
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")


        newMessage = {"messageID": messageID,"senderID": sender,"receiverID": receiver,
            "messageStatus": "Sent","dateTime": now,"content": content}


        with open("messagesFile.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file,
                fieldnames=["messageID","senderID","receiverID","messageStatus","dateTime","content"],
                quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows + [newMessage])


        messagebox.showinfo("Success", "Message sent successfully.")
        composeWin.destroy()
        parent.deiconify()


    tk.Button(composeWin, text="Send Response" if reply else "Send & Confirm", font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=sendMessage).pack(pady=10)


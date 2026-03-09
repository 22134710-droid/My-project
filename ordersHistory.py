import csv
import tkinter as tk
from tkinter import messagebox
import navigationMenu


class Order:        
    def __init__(self, orderID, Username, items, status,
                 totalPrice, phoneNumber, tax, discount):


        self.orderID = orderID
        self.Username = Username
        self.items = items
        self.status = status
        self.phoneNumber = phoneNumber or "not provided"
        self.totalPrice = float(totalPrice)
        self.discount = float(discount)
        self.tax = float(tax)
       
        self.baseTotal = (float(totalPrice) + float(discount) - float(tax))
        self._recalculateTotal()


   
    # ---------- VIEW ----------
    def viewOrder(self, parentWin):
        win = tk.Toplevel(parentWin)
        win.title(f"Order {self.orderID}")
        win.geometry("600x400")


        details = [f"Order ID: {self.orderID}",f"Username: {self.Username}",
            f"Items: {self.items}",f"Status: {self.status}",f"Phone Number: {self.phoneNumber}",
            f"Total Price: £{self.totalPrice}",f"Discount: £{self.discount}",f"Tax: £{self.tax}"]


        for d in details:
            tk.Label(win, text=d, font=("Arial", 11)).pack(anchor="w", padx=20, pady=4)


        tk.Button(win, text="Close", width=15, command=win.destroy).pack(pady=15)


    # ---------- EDIT ----------
    def editOrder(self, parentWin):
        win = tk.Toplevel(parentWin)
        win.title(f"Edit Order {self.orderID}")
        win.geometry("500x350")


        phoneVar = tk.StringVar(value=self.phoneNumber)
        discountVar = tk.DoubleVar(value=self.discount)
        taxVar = tk.DoubleVar(value=self.tax)
       
        tk.Label(win, text="Phone Number").pack(anchor="w", padx=10)
        tk.Entry(win, textvariable=phoneVar).pack(fill="x", padx=10)


        tk.Label(win, text="Discount").pack(anchor="w", padx=10)
        tk.Entry(win, textvariable=discountVar).pack(fill="x", padx=10)


        tk.Label(win, text="Tax").pack(anchor="w", padx=10)
        tk.Entry(win, textvariable=taxVar).pack(fill="x", padx=10)


        saved = {"ok": False}


        def save():
            self.phoneNumber = phoneVar.get()  or "not provided"
            self.discount = round(float(discountVar.get() or 0),2)
            self.tax = round(float(taxVar.get() or 0),2)
            self._recalculateTotal()


            saved["ok"] = True
            win.destroy()


        tk.Button(win, text="Save", width=15, command=save).pack(pady=15)


        parentWin.wait_window(win)
        return saved["ok"]


    # ---------- FILE SAVE (SAFE UPDATE) ----------
    def saveToOrdersFile(self):
        rows = []
        updated = False


        with open("ordersFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["orderID"] == self.orderID:
                    row["items"] = self.items
                    row["status"] = self.status
                    row["totalPrice"] = self.totalPrice
                    row["phoneNumber"] = self.phoneNumber
                    row["discount"] = self.discount
                    row["tax"] = self.tax
                    updated = True
                rows.append(row)


        if not updated:
            return


        with open("ordersFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


    # ---------- CANCEL ----------
    def cancelOrder(self):
        self.status = "Cancelled"
        self.saveToOrdersFile()
        self._updateTransactionFile("Refunded")


    # ---------- DELETE ----------
    def deleteOrder(self):
        with open("ordersFile.csv", "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            fieldnames = rows[0].keys() if rows else []


        rows = [r for r in rows if r["orderID"] != self.orderID]


        with open("ordersFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


        self._deleteTransactions()


    # ---------- TRANSACTIONS ----------
    def _updateTransactionFile(self, newStatus):
        rows = []


        try:
            with open("transactionsFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                fieldnames = list(reader.fieldnames or [])


                if "finalPrice" not in fieldnames:
                    fieldnames.append("finalPrice")
                if "tax" not in fieldnames:
                    fieldnames.append("tax")
                if "discounts" not in fieldnames:
                    fieldnames.append("discounts")
                if "status" not in fieldnames:
                    fieldnames.append("status")
               
                for row in reader:
                    if row["orderID"] == self.orderID:
                        row["finalPrice"] = f"{self.totalPrice:.2f}"
                        row["tax"] = f"{self.tax:.2f}"
                        row["discounts"] = f"{self.discount:.2f}"
                        if newStatus != "":
                            row["status"] = newStatus
                    rows.append(row)


            with open("transactionsFile.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)


        except FileNotFoundError:
            pass


    def _deleteTransactions(self):
        with open("transactionsFile.csv", "r", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            fieldnames = rows[0].keys() if rows else ["orderID","Username","items","status","totalPrice","phoneNumber","discount","tax"]


        rows = [r for r in rows if r.get("orderID") != self.orderID]


        with open("transactionsFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
   
    def _recalculateTotal(self):
        self.totalPrice = round(max(0.0,self.baseTotal + self.tax - self.discount),2)




def ordersHistoryWin(mainMenu, userDetails):
    mainMenu.withdraw()
    ordersHistoryScreen = tk.Toplevel()
    ordersHistoryScreen.title("Orders History Screen")
    ordersHistoryScreen.attributes('-fullscreen', True)
    ordersHistoryScreen.bind("<Escape>", lambda e: ordersHistoryScreen.attributes('-fullscreen', False))
    ordersHistoryScreen.protocol("WM_DELETE_WINDOW",lambda: navigationMenu.onClose(ordersHistoryScreen, mainMenu))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(ordersHistoryScreen,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    newOrdersLogo = tk.PhotoImage(file="ordersHistoryLogo2.png") #50% from 1st
    newOrdersIcon = tk.Label(logoFrame, image=newOrdersLogo,bg="#7E8181")
    newOrdersIcon.image = newOrdersLogo
    newOrdersIcon.pack(side="left")


    tk.Label(logoFrame, text="Manage Orders History", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="   ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(ordersHistoryScreen)
    container.pack(fill="both", expand=True, padx=40, pady=20)
    canvas = tk.Canvas(container, height=300, width=1100, highlightthickness=3, highlightbackground="#696767",bg="#4fa5d0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)


    scrollableFrame = tk.Frame(canvas,bg="#ffffff")
    scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="x", anchor="n")
    scrollbar.pack(side="right", fill="y")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), "units")))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    # ---------- LOAD MENUS ----------
    allOrders = []
    orderObjects = []
    try:
        with open("ordersFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                contentList = row["items"].split("|") if row["items"] else []
                allOrders.append(Order(row["orderID"],row["Username"],contentList,row["status"],row["totalPrice"],row["phoneNumber"],row["tax"],row["discount"]))
    except FileNotFoundError:
        messagebox.showerror("Error", "Orders File not found")
        return False
   
    orderObjects[:] = allOrders[:]


    # ---------- ROW SELECTION ----------
    selected = {"object": None, "widgets": []}
   
    def selectRow(orderObj, widgets):
        # Reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey",fg="black",relief="sunken") # bg="white", fg="black", relief="sunken")
        # Highlight current
        for w in widgets:
            w.config(readonlybackground="#4da6ff",fg="white",relief="raised") # bg="#4da6ff", fg="grey", relief="raised")#
        selected["object"] = orderObj
        selected["widgets"] = widgets
       
    # ---------- RENDER ROWS (FIX: extracted rendering logic) ----------
    def displayOrders(order):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(order):
            rowWidgets = []
            values = [obj.orderID, obj.status, obj.Username, obj.totalPrice]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=22)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey",fg="white")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")


                # ---------- FIX: correct lambda capture ----------
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayOrders(orderObjects)


    # ---------------- HELPERS ----------------
    # ----------- ACTIONS ------------
    def viewSelectedOrder():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select an order first")
            return
        selected["object"].viewOrder(ordersHistoryScreen)


    def editSelectedOrder():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select an order first")
            return
        saved = selected["object"].editOrder(ordersHistoryScreen)
        if saved:
            selected["object"].saveToOrdersFile()
            selected["object"]._updateTransactionFile("")
        ordersHistoryScreen.destroy()
        ordersHistoryWin(mainMenu, userDetails)


    def cancelSelectedOrder():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a order first")
            return


        if messagebox.askyesno("Confirm", f"Cancel order #{selected['object'].orderID}?"):
            selected["object"].cancelOrder()
            ordersHistoryScreen.destroy()
            ordersHistoryWin(mainMenu, userDetails)


    def deleteSelectedOrder():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a order first")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete order #{selected['object'].orderID}?"):
            selected["object"].deleteOrder()
            ordersHistoryScreen.destroy()
            ordersHistoryWin(mainMenu, userDetails)


    # ---------------- BUTTON BAR (UNCHANGED STYLE) ----------------
    bottomFrame = tk.Frame(ordersHistoryScreen)
    bottomFrame.pack(fill="x", pady=10)


    tk.Button(bottomFrame, width=25, height=2,text="View Selected Order",font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelectedOrder).grid(row=0, column=0, padx=10)


    tk.Button(bottomFrame, width=25, height=2,text="Edit Selected Order", font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=editSelectedOrder).grid(row=0, column=1, padx=10)


    tk.Button(bottomFrame, width=25, height=2,text="Cancel Selected Order",font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=cancelSelectedOrder).grid(row=0, column=2, padx=10)


    tk.Button(bottomFrame, width=25, height=2,text="Delete Selected Order",font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=deleteSelectedOrder).grid(row=0, column=3, padx=10)
   
    tk.Button(bottomFrame, width=25, height=2,text="Go Back to Navigation Menu",font=("Arial", 12,"bold"),
              bg="#171717", fg="white",
              command=lambda: navigationMenu.onClose(ordersHistoryScreen, mainMenu)).grid(row=1, column=0, padx=10,pady=10)

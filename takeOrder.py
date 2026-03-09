import csv
import tkinter as tk
from tkinter import messagebox
import datetime
import navigationMenu


def paymentWin(newOrderScreen, Discount, discountCode, deliveryService, mainMenu):
    newOrderScreen.withdraw()
    paymentScreen = tk.Toplevel()
    paymentScreen.title("Payment Screen")
    paymentScreen.attributes('-fullscreen', True)
    paymentScreen.bind("<Escape>", lambda e: paymentScreen.attributes('-fullscreen', False))
    paymentScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(paymentScreen, newOrderScreen))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(paymentScreen,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    newOrdersLogo = tk.PhotoImage(file="newOrderLogo2.png")
    newOrdersIcon = tk.Label(logoFrame, image=newOrdersLogo,bg="#7E8181")
    newOrdersIcon.image = newOrdersLogo
    newOrdersIcon.pack(side="left")


    tk.Label(logoFrame, text="Payment Screen", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Label(logoFrame, text="     ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    # ---------------- MAIN CONTENT ----------------
    contentFrame = tk.Frame(paymentScreen)
    contentFrame.pack(expand=True, fill="both", padx=30, pady=10)
    contentFrame.columnconfigure(0, weight=2)
    contentFrame.columnconfigure(1, weight=1)


    # =====================================================
    # LEFT SIDE — ORDER SUMMARY
    # =====================================================
    orderFrame = tk.Frame(contentFrame)
    orderFrame.grid(row=0, column=0, padx=5)


    tk.Label(orderFrame, text="Order Summary", font=("Arial", 18, "bold")).pack(anchor="w")
    orderListFrame = tk.Frame(orderFrame, bd=2, relief="groove", height=380, width=530)
    orderListFrame.pack(pady=5,padx=10)
    orderListFrame.pack_propagate(False)
    orderCanvas = tk.Canvas(orderListFrame, bg="#4fa5d0", highlightthickness=0)
    orderScrollbar = tk.Scrollbar(orderListFrame, orient="vertical", command=orderCanvas.yview)
    orderCanvas.configure(yscrollcommand=orderScrollbar.set)


    orderCanvas.pack(side="left", fill="both", expand=True)
    orderScrollbar.pack(side="right", fill="y")


    #orderScrollFrame = tk.Frame(orderCanvas)
    #orderCanvas.create_window((0, 0), window=orderScrollFrame, anchor="nw")


    orderScrollContainer = tk.Frame(orderCanvas, bg="#4fa5d0")
    orderCanvas.create_window((0, 0), window=orderScrollContainer, anchor="nw")
    orderScrollFrame = tk.Frame(orderScrollContainer)
    orderScrollFrame.pack(padx=15, pady=10)  # <-- THIS creates the visible blue border


    orderScrollFrame.bind(
        "<Configure>",lambda e: orderCanvas.configure(scrollregion=orderCanvas.bbox("all")))


    # =====================================================
    # ORDER DATA
    # =====================================================
    orderItems = newOrderScreen.orderItems if hasattr(newOrderScreen, "orderItems") else []


    # Main Meals Total
    MainMealsTotal = 0
    for MenuItem in orderItems:
        if MenuItem["menuCategory"] == "Main Meals":
            MainMealsTotal += float(MenuItem["price"]) * int(MenuItem["qty"])
    tk.Label(orderScrollFrame,text=f"Main Meals Total: £{MainMealsTotal:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)
   
    # Desserts Total
    DessertsTotal = 0
    for MenuItem in orderItems:
        if MenuItem["menuCategory"] == "Desserts":
            DessertsTotal += float(MenuItem["price"]) * int(MenuItem["qty"])
    tk.Label(orderScrollFrame,text=f"Desserts Total: £{DessertsTotal:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)
   
    grandTotal = 0
    for item in orderItems:
        grandTotal += float(item["price"]) * int(item["qty"])
   
    # Others Total
    OthersTotal = grandTotal - (MainMealsTotal + DessertsTotal)
    tk.Label(orderScrollFrame,text=f"Other Items Total: £{OthersTotal:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)


    # Grand Total
    tk.Label(orderScrollFrame,text=f"Grand Total: £{grandTotal:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)
   
    Tax = float(0)
    n=0
    # Tax
    if deliveryService["value"]: # charge for delivery service
        Tax= Tax + 4.99
        tk.Label(contentFrame, text="Taxed £4.99 for delivery", fg= "green", font=("Arial",10)).grid(row=(n+1), column=0, sticky="w")
        n= n+1
   
    if grandTotal < 10: # charge for small orders
        Tax= Tax + 0.99
        tk.Label(contentFrame, text="Taxed £0.99 for Under_10_Order", fg= "green", font=("Arial",10)).grid(row=(n+1), column=0, sticky="w")
   
    tk.Label(orderScrollFrame,text=f"Tax: £{Tax:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)
   
    # Discounts
    if Discount > grandTotal:
        Discount = grandTotal
    tk.Label(orderScrollFrame,text=f"Discounts: £{Discount:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)
   
    finalPrice = grandTotal + Tax - Discount


    # Final Price
    tk.Label(orderScrollFrame,text=f"Final Price: £{finalPrice:.2f}",font=("Arial", 12, "bold"),
             bg="white", width= 45, height=2,bd=3,relief="groove").pack(fill="x", padx=10, pady=2)


    # =====================================================
    # RIGHT SIDE — DETAILS
    # =====================================================
    rightFrame = tk.Frame(contentFrame)
    rightFrame.grid(row=0, column=1, sticky="nsew", padx=10)


    # ---------------- CUSTOMER DETAILS (OPTIONAL) ----------------
    customerFrame = tk.LabelFrame(rightFrame, text="Customer Details (Optional)",
        font=("Arial", 18, "bold"), padx=10, pady=10)
    customerFrame.pack(fill="x", pady=10)


    tk.Label(customerFrame, text="Username").grid(row=0, column=0, sticky="w")
    usernameEntry = tk.Entry(customerFrame, width=35)
    usernameEntry.grid(row=0, column=1)


    tk.Label(customerFrame, text="Phone Number").grid(row=1, column=0, sticky="w")
    phoneEntry = tk.Entry(customerFrame, width=35)
    phoneEntry.grid(row=1, column=1)


    # ---------------- TRANSACTION DETAILS (REQUIRED) ----------------
    transactionFrame = tk.LabelFrame(
        rightFrame, text="Transaction Details (Required)",font=("Arial", 18, "bold"), padx=10)
    transactionFrame.pack(fill="x", pady=50)


    tk.Label(transactionFrame, text="Payment Method").grid(row=0, column=0, sticky="w")
    paymentMethodEntry = tk.Entry(transactionFrame, width=35)
    paymentMethodEntry.grid(row=0, column=1)


    tk.Label(transactionFrame, text="Location").grid(row=1, column=0, sticky="w")
    locationEntry = tk.Entry(transactionFrame, width=35)
    locationEntry.grid(row=1, column=1)
    tk.Label(transactionFrame,text="For example: 14, High Street, Deeside",font=("Arial", 9),fg="grey").grid(row=2, column=1, sticky="w")


    tk.Label(transactionFrame, text="Postcode").grid(row=3, column=0, sticky="w")
    postcodeEntry = tk.Entry(transactionFrame, width=35)
    postcodeEntry.grid(row=3, column=1)
    tk.Label(transactionFrame,text="For example: CE21AA",font=("Arial", 9),fg="grey").grid(row=4, column=1, sticky="w")
   
    # =====================================================
    # CONFIRM PAYMENT
    # =====================================================
    def confirmPayment():
        username = usernameEntry.get().strip()
        phone = phoneEntry.get().strip()


        # ---- Username validation (optional) ----
        if username:
            found = False
            with open("customersFile.csv", newline="") as f:
                for row in csv.DictReader(f):
                    if row["Username"] == username:
                        found = True
                        break
            if not found:
                messagebox.showwarning("Error", "Username does not exist!")
                return


        # ---- Phone validation (optional) ----
        if phone:
            if not phone.isdigit():
                messagebox.showwarning("Error", "Phone number must be numeric!")
                return
            elif len(phone) != 11:
                messagebox.showwarning("Error", "Phone number must be 11 digits!")
                return

        # ---- Transaction validation ----
        paymentMethod = paymentMethodEntry.get().strip().lower()
        if paymentMethod== "":
            messagebox.showwarning("Error","Payment method is required!")
            return
        elif paymentMethod not in ["cash", "card", "other"]:
            messagebox.showwarning("Error","Payment method must be Cash, Card, or Other!")
            return


        if not locationEntry.get().strip():
            messagebox.showwarning("Error", "Location is required!")
            return


        postcode = postcodeEntry.get().strip().replace(" ", "")
        # Postcode is either 6 or 7 characters exculding the spaces e.g. CF10 1AA or CF1 1AA
        # not postcode.isalnum() checks for unwanted symbols like "! or ."
        if postcode== "":
            messagebox.showwarning("Error", "Postcode is required!")
            return
        elif not postcode.isalnum():
            messagebox.showwarning("Error", "Postcode can't have unwanted symbols (only numbers and letters): Invalid postcode format! E.g. CF10 1AA or CF1 1AA")
            return
        elif len(postcode) not in (6,7):
            messagebox.showwarning("Error", "Incorrect length: Invalid postcode format! Postcode must be 6 or 7 characters. E.g. CF10 1AA or CF1 1AA")
            return
        elif postcode.isdigit() or postcode.isalpha():
            messagebox.showwarning("Error","Posatcode can't be all numbers or all letters: Invalid postcode format! Must contain both letters and numbers. E.g. CF10 1AA or CF1 1AA")
            return
       
        # Generating IDs
        orderID = navigationMenu.getNextID("ordersFile.csv")
        transactionID = navigationMenu.getNextID("transactionsFile.csv")
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        # ---- Save transaction ----
        with open("transactionsFile.csv", "a", newline="") as f:
            csv.writer(f).writerow([
                transactionID, orderID,"Paid",
                f"{MainMealsTotal:.2f}", f"{DessertsTotal:.2f}", f"{OthersTotal:.2f}",
                f"{grandTotal:.2f}", f"{finalPrice:.2f}", f"{Tax}", f"{Discount}",
                date,
                paymentMethod,locationEntry.get(),postcode])
       
        # ---- Save order ----
        itemsStr = str([item["name"] for item in orderItems])


        with open("ordersFile.csv", "a", newline="") as f:
            csv.writer(f).writerow([
                orderID,username if username else "not provided",
                itemsStr,"Successful",
                f"{finalPrice:.2f}",
                phone if phone else "not provided",
                f"{Tax}",f"{Discount}"])
       
        def removeUsedDiscount(code):
            found = 0
            if not code:
                return False
           
            code = code.strip().lower()
            try:
                rows = []
                updated = False
                with open("discountsFile.csv", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames


                    for row in reader:
                        if row["discountCode"].strip().lower() == code:
                            discountQuantity = int(row["discountQuantity"])
                            found = found + 1
                           
                            if discountQuantity > 1:
                                row["discountQuantity"]= str(discountQuantity - 1)
                                rows.append(row)
                                # else it won't be added to rows. so technically be deleted as quantitiy becomes 0
                            updated = True
                        else:
                            rows.append(row)
               
                if updated:
                    with open("discountsFile.csv", "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)
               
                return updated
            except FileNotFoundError:
                messagebox.showwarning("Discount Error", "Error Occured! Please Tell a staff member!")
   
        if discountCode != "":
            removeUsedDiscount(discountCode)
        messagebox.showinfo("Payment", "Payment Confirmed!")
        paymentScreen.destroy()
        newOrderScreen.deiconify()
   
    def cancelOrder():
        if messagebox.askyesno("Confirm","Are you sure you want to cancel your order?"):
            paymentScreen.destroy()
            newOrderScreen.destroy()
            mainMenu.deiconify()
   
    # ---------------- BUTTONS ----------------
    bottomFrame = tk.Frame(paymentScreen)
    bottomFrame.pack(fill="x", pady=15)
    tk.Button(bottomFrame, text="Go Back To Order",width=25, height=2,font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(paymentScreen, newOrderScreen)).pack(side="left", padx=20)
    tk.Button(bottomFrame, text="Cancel Order",width=25, height=2,font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=cancelOrder).pack(side="left", padx=20)
    tk.Button(bottomFrame, text="Confirm Payment",width=25, height=2,font=("Arial", 12,"bold"),bg="#2A79A4",
              fg="white",command=confirmPayment).pack(side="left", padx=20)

def takingOrderWin(mainMenu):
    mainMenu.withdraw()
    newOrderScreen = tk.Toplevel()
    newOrderScreen.title("New Order Screen")
    newOrderScreen.attributes('-fullscreen', True)
    newOrderScreen.bind("<Escape>", lambda event: newOrderScreen.attributes('-fullscreen', False))
    newOrderScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(newOrderScreen, mainMenu))

    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(newOrderScreen,bg="#000000")
    topFrame.pack(fill="x")

    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)

    newOrdersLogo = tk.PhotoImage(file="newOrderLogo2.png")
    newOrdersIcon = tk.Label(logoFrame, image=newOrdersLogo,bg="#7E8181")
    newOrdersIcon.image = newOrdersLogo
    newOrdersIcon.pack(side="left")

    tk.Label(logoFrame, text="Take Order", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="     ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)

    # ---------------- MAIN CONTENT ----------------
    contentFrame = tk.Frame(newOrderScreen)
    contentFrame.pack(expand=True, fill="both", padx=30, pady=10)
    contentFrame.columnconfigure(0, weight=1)
    contentFrame.columnconfigure(1, weight=1)


    # =====================================================
    # LEFT SIDE — ORDER ITEMS
    # =====================================================
    orderFrame = tk.Frame(contentFrame)
    orderFrame.grid(row=0, column=0, sticky="nsew", padx=10)


    tk.Label(orderFrame, text="Order Items", font=("Arial", 18, "bold")).pack(anchor="w")


    orderListFrame = tk.Frame(orderFrame, bd=2, relief="groove", height=300, width=530)
    orderListFrame.pack(pady=(0, 5))
    orderListFrame.pack_propagate(False)


    orderCanvas = tk.Canvas(orderListFrame, bg="#4fa5d0", highlightthickness=0)
    orderScrollbar = tk.Scrollbar(orderListFrame, orient="vertical", command=orderCanvas.yview)
    orderCanvas.configure(yscrollcommand=orderScrollbar.set)
    orderCanvas.pack(side="left", fill="both", expand=True)
    orderScrollbar.pack(side="right", fill="y")


    orderScrollFrame = tk.Frame(orderCanvas, bg="#4fa5d0")
    orderCanvas.create_window((0, 0), window=orderScrollFrame, anchor="nw")
    orderScrollFrame.bind("<Configure>", lambda e: orderCanvas.configure(scrollregion=orderCanvas.bbox("all")))
   
    def onMousewheelLeft(event):
        orderCanvas.yview_scroll(-1 * (event.delta // 120), "units")
    orderCanvas.bind("<Enter>", lambda e: orderCanvas.bind_all("<MouseWheel>", onMousewheelLeft))
    orderCanvas.bind("<Leave>", lambda e: orderCanvas.unbind_all("<MouseWheel>"))


    # ---------------- TOTAL PRICE ----------------
    totalVar = tk.StringVar(value="Total: £0.00")
    totalFrame = tk.Frame(orderFrame)
    totalFrame.pack(fill="x", pady=(0, 10))


    tk.Label(totalFrame,textvariable=totalVar,font=("Arial", 16, "bold"),anchor="e").pack(fill="x", padx=10)


    # ---------------- ORDER DATA ----------------
    orderItems = []
    selectedOrderRow = {"widgets": [], "index": None}


    def updateTotalPrice():
        total = 0
        for item in orderItems:
            total += float(item["price"]) * int(item["qty"])
       
        if takeDelivery["value"]:
            total= total + 4.99
        totalVar.set(f"Total: £{total:.2f}")


    def refreshOrderItems():
        for w in orderScrollFrame.winfo_children():
            w.destroy()


        for idx, item in enumerate(orderItems):
            row = tk.Frame(orderScrollFrame, bg="white", bd=1, relief="solid")
            row.pack(fill="x", padx=10, pady=2)


            lbl = tk.Label(row,text=f"{item['id']}   {item['name']}   x{item['qty']}   £{item['price']}",
                font=("Arial", 14),bg="white",anchor="w")
            lbl.pack(fill="x", padx=5, pady=3)


            widgets = [row]
            row.bind("<Button-1>", lambda e, i=idx, w=widgets: selectOrderRow(i, w))
            lbl.bind("<Button-1>", lambda e, i=idx, w=widgets: selectOrderRow(i, w))


    def selectOrderRow(idx, widgets):
        for w in selectedOrderRow["widgets"]:
            w.config(bg="white")
            for c in w.winfo_children():
                c.config(bg="white", fg="black")


        for w in widgets:
            w.config(bg="#797979")
            for c in w.winfo_children():
                c.config(bg="#797979", fg="white")


        selectedOrderRow["widgets"] = widgets
        selectedOrderRow["index"] = idx


    def chooseQuantity():
        win = tk.Toplevel(newOrderScreen)
        win.title("Quantity")
        win.geometry("250x150")
        win.grab_set()


        tk.Label(win, text="Quantity", font=("Arial", 14)).pack(pady=10)
        qtyVar = tk.IntVar(value=1)
        tk.Spinbox(win, from_=1, to=20, textvariable=qtyVar).pack()


        def confirm():
            win.qty = qtyVar.get()
            win.destroy()


        tk.Button(win, text="Confirm", command=confirm).pack(pady=10)
        newOrderScreen.wait_window(win)
        return getattr(win, "qty", None)


    # ---------------- ADD / REMOVE / CANCEL ----------------
    selectedMenuRow = {"widgets": [], "item": None}


    def addToOrder():
        if not selectedMenuRow["item"]:
            messagebox.showwarning("Warning", "Select an item first")
            return
       
        qty = chooseQuantity()
        if qty is None:
            return
       
        item = selectedMenuRow["item"]


        for orderItem in orderItems:
            if (orderItem["id"] == item["itemID"] and orderItem["menuCategory"] == item["MenuCategoryLink"]):
                orderItem["qty"] += qty
                refreshOrderItems()
                updateTotalPrice()
                return
       
        orderItems.append({"id": item["itemID"],"name": item["itemName"],"price": item["itemPrice"],
        "qty": qty,"menuCategory": item["MenuCategoryLink"]})


        refreshOrderItems()
        updateTotalPrice()


    def removeFromOrder():
        if selectedOrderRow["index"] is None:
            messagebox.showerror("Error","Please select an item from order items to remove!")
            return
        del orderItems[selectedOrderRow["index"]]
        selectedOrderRow["index"] = None
        selectedOrderRow["widgets"] = []
        refreshOrderItems()
        updateTotalPrice()


    def cancelCurrentOrder():
        orderItems.clear()
        selectedOrderRow["index"] = None
        selectedOrderRow["widgets"] = []
        refreshOrderItems()
        updateTotalPrice()


    tk.Button(orderFrame, text="Add Item", width=20, font=("Arial", 12,"bold"),bg="#2A79A4",
              fg="white",command=addToOrder).pack(pady=2)
    tk.Button(orderFrame, width=25, height=2, text="Go Back To Navigation Menu",font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(newOrderScreen, mainMenu)).pack(pady=4)
    tk.Label(orderFrame, text= "Enter A Discount Code Below: (6 Characters Code)").pack(pady=4)
    discountCodeEntry = tk.Entry(orderFrame)
    discountCodeEntry.pack(pady=4)


    # =====================================================
    # RIGHT SIDE — MENU ITEMS
    # =====================================================
    itemsFrame = tk.Frame(contentFrame)
    itemsFrame.grid(row=0, column=1, sticky="nsew", padx=10)


    tk.Label(itemsFrame, text="All Items", font=("Arial", 18, "bold")).pack(anchor="w")


    canvasFrame = tk.Frame(itemsFrame, height=300, width=570, bd=2, relief="groove")
    canvasFrame.pack(fill="both")
    canvasFrame.pack_propagate(False)


    canvas = tk.Canvas(canvasFrame, bg="#4fa5d0", highlightthickness=0)
    scrollbar = tk.Scrollbar(canvasFrame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    scrollFrame = tk.Frame(canvas, bg="#4fa5d0")
    canvas.create_window((0, 0), window=scrollFrame, anchor="nw")
    scrollFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    def onMousewheelRight(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", onMousewheelRight))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    itemsLookup = {}
    with open("itemsFile.csv", newline="") as f:
        for row in csv.DictReader(f):
            itemsLookup[row["itemID"]] = row


    def selectMenuRow(widgets, item):
        for w in selectedMenuRow["widgets"]:
            w.config(bg="white")
            for c in w.winfo_children():
                c.config(bg="white", fg="black")


        for w in widgets:
            w.config(bg="#797979")
            for c in w.winfo_children():
                c.config(bg="#797979", fg="white")


        selectedMenuRow["widgets"] = widgets
        selectedMenuRow["item"] = item
   
    with open("menusFile.csv", newline="") as f:
        for menu in csv.DictReader(f):
            tk.Label(scrollFrame, text=menu["menuName"], font=("Arial", 16, "bold")).pack(anchor="w", padx=10)
            for itemID in menu["menuContent"].split("|"):
                if itemID in itemsLookup:
                    item = itemsLookup[itemID].copy()
                    item["MenuCategoryLink"] = menu["menuCategory"]
                    row = tk.Frame(scrollFrame, bg="white", bd=1, relief="solid")
                    row.pack(fill="x", padx=20, pady=2)
                    lbl = tk.Label(row, text=f"{itemID}   {item['itemName']}   £{item['itemPrice']}",
                                   font=("Arial", 16), bg="white", anchor="w")
                    lbl.pack(fill="x")
                    widgets = [row]
                    row.bind("<Button-1>", lambda e, w=widgets, i=item: selectMenuRow(w, i))
                    lbl.bind("<Button-1>", lambda e, w=widgets, i=item: selectMenuRow(w, i))
   
    def proceedToPayment():
        if not orderItems:
            messagebox.showwarning("Empty Order", "Add at least one item before proceeding.")
            return
       
        discountCode = discountCodeEntry.get().strip().upper()
        newOrderScreen.orderItems = orderItems
        discountFound = False
        Discount = 0


        if discountCode != "":
            enteredCode = discountCode.strip().lower()
            try:
                with open("discountsFile.csv", newline="", encoding="utf-8") as f:
                    reader= csv.DictReader(f)
                    for row in reader:
                        if row["discountCode"].strip().lower() == enteredCode:
                            Discount = float(row["discountAmount"])
                            discountFound = True
                            break
                if not discountFound and len(enteredCode) !=0:
                    messagebox.showwarning("Discount", "Invalid discount code.")


            except FileNotFoundError:
                messagebox.showerror("Discount Error", "An Error occured. Can't apply a discount!")
       
        if discountFound or discountCode == "":
            paymentWin(newOrderScreen,Discount, discountCode, takeDelivery, mainMenu)
   
    takeDelivery = {"value": False}
    def activateDelivery():
        takeDelivery["value"] = True
        deliveryServiceButton.config(state=tk.DISABLED)
        updateTotalPrice()
   
    tk.Button(itemsFrame, text="Remove Item", width=20, font=("Arial", 12,"bold"),bg="#2A79A4",
              fg="white",command=removeFromOrder).pack(pady=2)
    tk.Button(itemsFrame, text="Cancel Order", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=cancelCurrentOrder).pack(pady=4)
    deliveryServiceButton = tk.Button(itemsFrame, text="Activate Delivery Service (+£4.99)",font=("Arial", 12,"bold"),bg="#2A79A4",
              fg="white",width=25, height=2,command=activateDelivery)
    deliveryServiceButton.pack(pady=2)
    tk.Button(itemsFrame, width=25, height=2, text="Confirm and Proceed",font=("Arial", 12,"bold"),bg="#2A79A4",
              fg="white",command=proceedToPayment).pack(pady=2)


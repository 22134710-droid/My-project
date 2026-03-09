import csv
import tkinter as tk
from tkinter import messagebox
import navigationMenu


class Menu:
    def __init__(self, menuID, menuName, menuCategory, menuContent):
        self.menuID = menuID
        self.menuName = menuName
        self.menuCategory = menuCategory
        self.menuContent = menuContent  # list of itemIDs

    # ---------------- ADD MENU ----------------
    def addMenu(self, parentWin,mWin):
        parentWin.withdraw()
        addWin = tk.Toplevel()
        addWin.title("Add Menu")
        addWin.attributes("-fullscreen", True)

        frame = tk.Frame(addWin)
        frame.pack(pady=40)
        nameE = tk.Entry(frame, width=40)
        catE = tk.Entry(frame, width=40)
        contentE = tk.Entry(frame, width=40)
        contentE.config(state="readonly")  # lock field

        for w, t in [(nameE, "Menu Name"),(catE, "Menu Category"),(contentE, "Menu Content (itemID|itemID)")]:
            tk.Label(frame, text=t).pack()
            w.pack(pady=5)

        # ---------- ITEM SELECTION LIST ----------
        listFrame = tk.Frame(addWin)
        listFrame.pack(pady=10, fill="both", expand=True)
        scrollbar = tk.Scrollbar(listFrame)
        scrollbar.pack(side="right", fill="y")

        itemsList = tk.Listbox(listFrame, yscrollcommand=scrollbar.set, selectmode="multiple", width=80, height=12)
        itemsList.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=itemsList.yview)

        itemsData = []

        # Load items from itemsFile.csv
        try:
            with open("itemsFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    itemsData.append(row)
                    itemsList.insert(tk.END, f"{row['itemID']} | {row['itemName']} | £{row['itemPrice']}")
        except FileNotFoundError:
            messagebox.showerror("Error", "itemsFile.csv not found")
            return

        # ---------- ITEM SELECTION HANDLER ----------
        def addSelectedItems():
            selectedIndices = itemsList.curselection()
            if not selectedIndices:
                messagebox.showwarning("Warning", "Select items to add")
                return
            selectedIDs = [itemsData[i]["itemID"] for i in selectedIndices]
            currentContent = contentE.get().split("|") if contentE.get() else []
            # Avoid duplicates
            newContent = list(dict.fromkeys(currentContent + selectedIDs))
            contentE.config(state="normal")
            contentE.delete(0, tk.END)
            contentE.insert(0, "|".join(newContent))
            contentE.config(state="readonly")

        tk.Button(addWin, text="Add Selected Items", width=20, command=addSelectedItems).pack(pady=5)

        # ---------- SEARCH BAR ----------
        searchFrame = tk.Frame(addWin)
        searchFrame.pack(pady=10)
        tk.Label(searchFrame, text="Search Item by ID or Name:").pack(side="left")
        searchEntry = tk.Entry(searchFrame, width=30)
        searchEntry.pack(side="left", padx=5)


        def searchItem():
            query = searchEntry.get().strip().lower()
            itemsList.delete(0, tk.END)
            found = False
            for item in itemsData:
                if query == item["itemID"].lower() or query in item["itemName"].lower():
                    itemsList.insert(tk.END, f"{item['itemID']} | {item['itemName']} | £{item['itemPrice']}")
                    found = True
            if not found:
                messagebox.showerror("Error", "Item not found!")
        
        tk.Button(searchFrame, text="Search", width=12, command=searchItem).pack(side="left", padx=5)
        
        # ---------- SAVE MENU ----------
        
        def saveMenu():
            menuID= navigationMenu.getNextID("menusFile.csv")
            if not nameE.get() or not catE.get() or not contentE.get():
                messagebox.showwarning("Warning", "All fields must be filled")
                return
            try:
                with open("menusFile.csv", "r", newline="", encoding="utf-8") as f:
                    hasHeader = True
            except FileNotFoundError:
                hasHeader = False

            with open("menusFile.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not hasHeader:
                    writer.writerow(["menuID", "menuName", "menuCategory", "menuContent"])
                writer.writerow([menuID, nameE.get(), catE.get(), contentE.get()])
            messagebox.showinfo("Success", "Menu added successfully")
            addWin.destroy()
            parentWin.destroy()
            manageMenusScreen(mWin)

        # ---------- BACK TO MEALS BUTTON ----------
        butFrame = tk.Frame(addWin)
        butFrame.pack(pady=40)
        tk.Button(butFrame, text="Back To Menus List", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(addWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Menu", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveMenu).pack(side="right")

    # ---------------- VIEW MENU ----------------
    def viewMenu(self, parentWin):
        parentWin.withdraw()
        viewWin = tk.Toplevel()
        viewWin.title("Menu Details")
        viewWin.attributes("-fullscreen", True)

        frame = tk.Frame(viewWin)
        frame.pack(pady=40)

        fields = [("Menu ID", self.menuID),("Menu Name", self.menuName),("Category", self.menuCategory),("Content", "|".join(self.menuContent))]

        for label, value in fields:
            tk.Label(frame, text=label).pack()
            e = tk.Entry(frame, width=50)
            e.insert(0, value)
            e.config(state="readonly")
            e.pack(pady=5)

        tk.Button(frame, text="Back To Menus List", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(viewWin, parentWin)).pack(pady=20)

    # ---------------- EDIT MENU ----------------
    def editMenu(self, parentWin,mWin):
        parentWin.withdraw()
        editWin = tk.Toplevel()
        editWin.title("Edit Menu")
        editWin.attributes("-fullscreen", True)

        frame = tk.Frame(editWin)
        frame.pack(pady=30)

        nameE = tk.Entry(frame, width=40)
        catE = tk.Entry(frame, width=40)
        contentE = tk.Entry(frame, width=40)
        contentE.config(state="readonly")

        nameE.insert(0, self.menuName)
        catE.insert(0, self.menuCategory)
        contentE.config(state="normal")
        contentE.insert(0, "|".join(self.menuContent))
        contentE.config(state="readonly")

        for w, t in [(nameE, "Menu Name"),(catE, "Menu Category"),(contentE, "Menu Content")]:
            tk.Label(frame, text=t).pack()
            w.pack(pady=5)


        # ---------- ITEM SELECTION ----------
        listFrame = tk.Frame(editWin)
        listFrame.pack(pady=10, fill="both", expand=True)
        scrollbar = tk.Scrollbar(listFrame)
        scrollbar.pack(side="right", fill="y")


        itemsList = tk.Listbox(listFrame, yscrollcommand=scrollbar.set, selectmode="multiple", width=80, height=12)
        itemsList.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=itemsList.yview)


        itemsData = []
        try:
            with open("itemsFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    itemsData.append(row)
                    itemsList.insert(tk.END, f"{row['itemID']} | {row['itemName']} | £{row['itemPrice']}")
        except FileNotFoundError:
            messagebox.showerror("Error", "itemsFile.csv not found")
            return


        def addSelectedItems():
            selectedIndices = itemsList.curselection()
            if not selectedIndices:
                messagebox.showwarning("Warning", "Select items to add")
                return
            selectedIDs = [itemsData[i]["itemID"] for i in selectedIndices]
            currentContent = contentE.get().split("|") if contentE.get() else []
            newContent = list(dict.fromkeys(currentContent + selectedIDs))
            contentE.config(state="normal")
            contentE.delete(0, tk.END)
            contentE.insert(0, "|".join(newContent))
            contentE.config(state="readonly")


        tk.Button(editWin, text="Add Selected Items", width=20, command=addSelectedItems).pack(pady=5)

        # ---------- SEARCH BAR ----------
        searchFrame = tk.Frame(editWin)
        searchFrame.pack(pady=10)
        tk.Label(searchFrame, text="Search Item by ID or Name:").pack(side="left")
        searchEntry = tk.Entry(searchFrame, width=30)
        searchEntry.pack(side="left", padx=5)

        def searchItem():
            query = searchEntry.get().strip().lower()
            itemsList.delete(0, tk.END)
            found = False
            for item in itemsData:
                if query == item["itemID"].lower() or query in item["itemName"].lower():
                    itemsList.insert(tk.END, f"{item['itemID']} | {item['itemName']} | £{item['itemPrice']}")
                    found = True
            if not found:
                messagebox.showerror("Error", "Item not found!")


        tk.Button(searchFrame, text="Search", width=12, command=searchItem).pack(side="left", padx=5)
        # ---------- SAVE CHANGES ----------
        def saveChanges():
            rows = []
            with open("menusFile.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["menuID"] == self.menuID:
                        row["menuName"] = nameE.get()
                        row["menuCategory"] = catE.get()
                        row["menuContent"] = contentE.get()
                    rows.append(row)
            with open("menusFile.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            messagebox.showinfo("Saved", "Menu updated")
            editWin.destroy()
            parentWin.destroy()
            manageMenusScreen(mWin)

        butFrame = tk.Frame(editWin)
        butFrame.pack(pady=40)
        tk.Button(butFrame, text="Back To Meals List", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(editWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Changes", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveChanges).pack(side="right")

    # ---------------- DELETE MENU ----------------
    def deleteMenu(self):
        rows = []
        with open("menusFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["menuID"] != self.menuID:
                    rows.append(row)
        if not rows:
            fieldnames = ["menuID", "menuName", "menuCategory", "menuContent"]
        else:
            fieldnames = rows[0].keys()
        with open("menusFile.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Deleted", f"Menu {self.menuName} deleted successfully!")


class Item:
    def __init__(self, itemID, itemName, itemPrice, itemIngredients):
        self.itemID = itemID
        self.itemName = itemName
        self.itemPrice = itemPrice
        self.itemIngredients = itemIngredients  # list

    # ---------------- ADD ITEM ----------------
    def addItem(self, parentWin,mWin):
        parentWin.withdraw()
        addWin = tk.Toplevel()
        addWin.title("Add Item")
        addWin.attributes("-fullscreen", True)

        frame = tk.Frame(addWin)
        frame.pack(pady=40)
        
        nameE = tk.Entry(frame, width=40)
        priceE = tk.Entry(frame, width=40)
        ingE = tk.Entry(frame, width=40)

        for w, t in [(nameE, "Item Name"),(priceE, "Item Price"),(ingE, "Ingredients (| separated)")]:
            tk.Label(frame, text=t).pack()
            w.pack(pady=5)

        def saveItem():
            itemID= navigationMenu.getNextID("itemsFile.csv")
            if not nameE.get() or not priceE.get() or not ingE.get():
                messagebox.showwarning("Warning", "All fields must be filled")
                return
            try:
                with open("itemsFile.csv", "r"):
                    hasHeader = True
            except FileNotFoundError:
                hasHeader = False

            with open("itemsFile.csv", "a", newline="") as f:
                writer = csv.writer(f)
                if not hasHeader:
                    writer.writerow(["itemID", "itemName", "itemPrice", "itemIngredients"])
                writer.writerow([itemID,nameE.get(),priceE.get(),ingE.get()])

            messagebox.showinfo("Success", "Item added")
            addWin.destroy()
            parentWin.destroy()
            manageItemsScreen(mWin)

        butFrame= tk.Frame(addWin)
        butFrame.pack(pady=40)
        tk.Button(butFrame,text="Back To Items List",width=20,font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(addWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Item", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveItem).pack(side="right")
        
    # ---------------- VIEW ITEM ----------------
    def viewItem(self, parentWin):
        parentWin.withdraw()
        viewWin = tk.Toplevel()
        viewWin.title("Item Profile")
        viewWin.attributes("-fullscreen", True)

        frame = tk.Frame(viewWin)
        frame.pack(pady=40)

        fields = [("Item ID", self.itemID),("Name", self.itemName),
            ("Price", self.itemPrice),("Ingredients", ", ".join(self.itemIngredients))]

        for label, value in fields:
            tk.Label(frame, text=label).pack()
            e = tk.Entry(frame, width=50, state="readonly")
            e.pack(pady=5)
            e.config(state="normal")
            e.insert(0, value)
            e.config(state="readonly")

        tk.Button(frame,text="Back To Items List",width=20,font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(viewWin, parentWin)).pack(pady=20)

    # ---------------- EDIT ITEM ----------------
    def editItem(self, parentWin,mWin):
        parentWin.withdraw()
        editWin = tk.Toplevel()
        editWin.title("Edit Item")
        editWin.attributes("-fullscreen", True)

        frame = tk.Frame(editWin)
        frame.pack(pady=40)

        nameE = tk.Entry(frame, width=40)
        priceE = tk.Entry(frame, width=40)
        ingE = tk.Entry(frame, width=40)

        nameE.insert(0, self.itemName)
        priceE.insert(0, self.itemPrice)
        ingE.insert(0, "|".join(self.itemIngredients))

        for w, t in [(nameE, "Item Name"),(priceE, "Item Price"),(ingE, "Ingredients")]:
            tk.Label(frame, text=t).pack()
            w.pack(pady=5)

        def saveChanges():
            rows = []
            with open("itemsFile.csv", "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["itemID"] == self.itemID:
                        row["itemName"] = nameE.get()
                        row["itemPrice"] = priceE.get()
                        row["itemIngredients"] = ingE.get()
                    rows.append(row)

            with open("itemsFile.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            messagebox.showinfo("Saved", "Item updated")
            editWin.destroy()
            parentWin.destroy()
            manageItemsScreen(mWin)

        butFrame= tk.Frame(editWin)
        butFrame.pack(pady=40)
        tk.Button(butFrame,text="Back To Items List",width=20,font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=lambda: navigationMenu.onClose(editWin, parentWin)).pack(side="left",padx=10)
        tk.Button(butFrame, text="Save Changes", width=20, font=("Arial", 12,"bold"),bg="#171717",
              fg="white",command=saveChanges).pack(side="right")
        

    # ---------------- DELETE ITEM ----------------
    def deleteItem(self):
        rows = []
        with open("itemsFile.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["itemID"] != self.itemID:
                    rows.append(row)
        
        with open("itemsFile.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Deleted", f"Item {self.itemName} deleted successfully!")

def mealsWin(mainMenu,accountDetails):
    mainMenu.withdraw()
    mealsScreen = tk.Toplevel()
    mealsScreen.title("Meals Screen")
    mealsScreen.attributes('-fullscreen', True)
    mealsScreen.bind("<Escape>", lambda event: mealsScreen.attributes('-fullscreen', False))
    mealsScreen.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(mealsScreen,mainMenu))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(mealsScreen,bg="#000000")
    topFrame.pack(fill="x",pady=20)


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    mealsLogo = tk.PhotoImage(file="mealsLogo2.png")
    mealsIcon = tk.Label(logoFrame, image=mealsLogo,bg="#7E8181")
    mealsIcon.image = mealsLogo
    mealsIcon.pack(side="left")


    tk.Label(logoFrame, text="Meals", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="        ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    viewMenusFrame= tk.Frame(mealsScreen, bg="lightblue")
    viewMenusFrame.pack()
    viewMenus = tk.Button(viewMenusFrame, width=42, text="View Menus", height = 3, command= lambda: viewMenusScreen(mealsScreen))
    viewMenus.grid(row=0,column=0,padx=15,pady=5)


    viewMenusLogo = tk.PhotoImage(file="MenusLogo.png")
    viewMenusIcon = tk.Label(viewMenusFrame,image=viewMenusLogo)
    viewMenusIcon.image = viewMenusLogo
    viewMenusIcon.grid(row=0, column=1, padx=5,pady=5)
   
    viewItemsFrame= tk.Frame(mealsScreen, bg="lightgreen")
    viewItemsFrame.pack(pady=20)
    viewItems = tk.Button(viewItemsFrame, width=40, text="View Items", height = 3, command= lambda: viewItemsScreen(mealsScreen))
    viewItems.grid(row=0,column=0,padx=15,pady=5)


    viewItemsLogo = tk.PhotoImage(file="ItemsLogo.png")
    viewItemsIcon = tk.Label(viewItemsFrame,image=viewItemsLogo)
    viewItemsIcon.image = viewItemsLogo
    viewItemsIcon.grid(row=0, column=1, padx=5,pady=5)


    if accountDetails["userType"] == "admin":
        manageMenusFrame= tk.Frame(mealsScreen, bg="red")
        manageMenusFrame.pack(pady=10)
        manageMenus = tk.Button(manageMenusFrame, width=43, text="Manage Menus", height = 3, command= lambda: manageMenusScreen(mealsScreen))
        manageMenus.grid(row=0,column=0,padx=15,pady=5)
        
        manageMenusLogo = tk.PhotoImage(file="manageMenusLogo.png")
        manageMenusIcon = tk.Label(manageMenusFrame,image=manageMenusLogo)
        manageMenusIcon.image = manageMenusLogo
        manageMenusIcon.grid(row=0, column=1, padx=5,pady=5)
        
        manageItemsFrame= tk.Frame(mealsScreen, bg="darkblue")
        manageItemsFrame.pack(pady=10)
        manageItems = tk.Button(manageItemsFrame, width=45, text="Manage Items", height = 3, command= lambda: manageItemsScreen(mealsScreen))
        manageItems.grid(row=0,column=0,padx=15,pady=5)
        
        manageItemsLogo = tk.PhotoImage(file="manageItemsLogo.png")
        manageItemsIcon = tk.Label(manageItemsFrame,image=manageItemsLogo)
        manageItemsIcon.image = manageItemsLogo
        manageItemsIcon.grid(row=0, column=1, padx=5,pady=5)
    
    butFrame= tk.Frame(mealsScreen)
    butFrame.pack(pady=50, fill="x")
    closeWin= tk.Button(butFrame, width=25, text="Go Back To Navigation Menu", height = 2,font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(mealsScreen,mainMenu))
    closeWin.pack(anchor="w",padx=5)




def viewMenusScreen(mWin):
    mWin.withdraw()
    viewMenusWin = tk.Toplevel()
    viewMenusWin.title("Menus Screen")
    viewMenusWin.attributes('-fullscreen', True)
    viewMenusWin.bind("<Escape>", lambda event: viewMenusWin.attributes('-fullscreen', False))
    viewMenusWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(viewMenusWin, mWin))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(viewMenusWin,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    viewMenusLogo = tk.PhotoImage(file="MenusLogo.png") 
    viewMenusIcon = tk.Label(logoFrame, image=viewMenusLogo,bg="#7E8181")
    viewMenusIcon.image = viewMenusLogo
    viewMenusIcon.pack(side="left")


    tk.Label(logoFrame, text="Menus List", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="       ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    container = tk.Frame(viewMenusWin)
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


    allMenus = []
    menuObjects = []
    try:
        with open("menusFile.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                contentList = row["menuContent"].split("|")
                allMenus.append(
                    Menu(row["menuID"],row["menuName"],row["menuCategory"],contentList))
    except FileNotFoundError:
        messagebox.showerror("Error", "menusFile.csv not found")
        return False
    menuObjects[:] = allMenus[:]


    # ---------- ROW SELECTION ----------
    selected = {"object": None,"widgets": []}
    def selectRow(menuObj, widgets):# reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")# highlight current selection
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised") 
       
        selected["object"] = menuObj
        selected["widgets"] = widgets
    
    # ---------- RENDER ROWS ----------
    def displayMenus(menu):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(menu):
            rowWidgets = []
            values = [obj.menuID, obj.menuName, obj.menuCategory]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=30)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayMenus(menuObjects)


    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a menu first")
            return
        selected["object"].viewMenu(viewMenusWin)

    # ---------- SEARCH ----------
    searchFrame = tk.Frame(viewMenusWin)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Menu (menuID / menuName):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchMenu():
        query = searchEntry.get().strip().lower()
        if not query:
            displayCustomers(menuObjects)
            return
        results = []
        for c in menuObjects:
            if (query in c.menuID or query in c.menuName.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Menu not found")
            return
        displayMenus(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchMenu).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayMenus(menuObjects)).pack(side="left")
    
    def filterMenus():
        filterWin = tk.Toplevel(viewMenusWin)
        filterWin.title("Filter Menus")
        filterWin.geometry("900x300")
        filterWin.grab_set()
        tk.Label(filterWin, text="Enter the category you want to filter by below:", font=("Arial", 12, "bold")).pack(pady=10)
        categoryPickEntry= tk.Entry(filterWin)
        categoryPickEntry.pack(pady=10)


        def sortAndRefresh():
            categoryPick=categoryPickEntry.get()
            field = "menuCategory"


            menuObjects[:] = allMenus[:]
            navigationMenu.filterRecords(menuObjects,field,categoryPick)
            displayMenus(menuObjects)
            filterWin.destroy()
        tk.Button(filterWin,text="Confirm Filtering",width=20,command= sortAndRefresh).pack(pady=5)
    
    def resetMenus():
        menuObjects[:] = allMenus[:]
        displayMenus(menuObjects)
    
    btnFrame = tk.Frame(viewMenusWin)
    btnFrame.pack(pady=15)
    tk.Button(btnFrame, text="Back To Meals", width=20, font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command= lambda: navigationMenu.onClose(viewMenusWin, mWin)).pack(side="left", padx=20)
    tk.Button(btnFrame, text="View Menu Details", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=20)
    tk.Button(btnFrame, text="Filter Menus By Category", width=25, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=filterMenus).pack(side="right", padx=20)
    tk.Button(btnFrame,text="Reset Filters",width=20,font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=resetMenus).pack(side="right", padx=20)




def viewItemsScreen(mWin):
    mWin.withdraw()
    viewItemsWin = tk.Toplevel()
    viewItemsWin.title("Items Screen")
    viewItemsWin.attributes('-fullscreen', True)
    viewItemsWin.bind("<Escape>", lambda event: viewItemsWin.attributes('-fullscreen', False))
    viewItemsWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(viewItemsWin, mWin))


    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(viewItemsWin,bg="#000000")
    topFrame.pack(fill="x")


    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)


    viewItemsLogo = tk.PhotoImage(file="ItemsLogo.png")  
    viewItemsIcon = tk.Label(logoFrame, image=viewItemsLogo,bg="#7E8181")
    viewItemsIcon.image = viewItemsLogo
    viewItemsIcon.pack(side="left")


    tk.Label(logoFrame, text="Items List", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="       ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)


    container = tk.Frame(viewItemsWin)
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


    allItems = [] 
    itemObjects = []
    try:
        with open("itemsFile.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                    ingredientsList = row["itemIngredients"].split("|")
                    allItems.append(
                        Item(row["itemID"],row["itemName"],row["itemPrice"],ingredientsList))
    except FileNotFoundError:
        messagebox.showerror("Error", "itemsFile.csv not found")
        return False
    
    itemObjects[:] = allItems[:]


    selected = {"object": None,"widgets": []}
    def selectRow(itemObj, widgets):# reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")# highlight current selection
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
       
        selected["object"] = itemObj
        selected["widgets"] = widgets
    
    # ---------- RENDER ROWS ---------- 
    def displayItems(item):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []


        for r, obj in enumerate(item):
            rowWidgets = []
            values = [obj.itemID, obj.itemName, obj.itemPrice]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=30)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayItems(itemObjects)

    

    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select an item first")
            return
        selected["object"].viewItem(viewItemsWin)

    # ---------- SEARCH ----------
    searchFrame = tk.Frame(viewItemsWin)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Item (itemID / itemName):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchItem():
        query = searchEntry.get().strip().lower()
        if not query:
            displayCustomers(itemObjects)
            return
        results = []
        for c in itemObjects:
            if (query in c.itemID or query in c.itemName.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Item not found")
            return
        displayItems(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchItem).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayItems(itemObjects)).pack(side="left")

    btnFrame = tk.Frame(viewItemsWin)
    btnFrame.pack(pady=15)
     
    def sortItemsByPrice():
        sortWin = tk.Toplevel(viewItemsWin)
        sortWin.title("Sort Items By Price")
        sortWin.geometry("900x300")
        sortWin.grab_set()


        def sortAndRefresh(field):
            navigationMenu.SortRecordsAscending(itemObjects, field)
            displayItems(itemObjects)
            sortWin.destroy()


        def sortAndRefreshDecending(field):
            navigationMenu.SortRecordsDecending(itemObjects, field)
            displayItems(itemObjects)
            sortWin.destroy()
        
        tk.Button(sortWin,text="Sort By Price (Ascending)",width=20,command=lambda: sortAndRefresh("itemPrice")).pack(pady=5)
        tk.Button(sortWin,text="Sort By Price (Decending)",width=20,command=lambda: sortAndRefreshDecending("itemPrice")).pack(pady=5)
    
    def resetItems():
        itemObjects[:] = allItems[:]
        displayItems(itemObjects)

    tk.Button(btnFrame, text="Back To Meals", width=20, font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command= lambda: navigationMenu.onClose(viewItemsWin, mWin)).pack(side="left", padx=20)
    tk.Button(btnFrame, text="View Item Details", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=20)
    tk.Button(btnFrame, text="Sort Items By Price", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=sortItemsByPrice).pack(side="right", padx=20)
    tk.Button(btnFrame, text="Reset Items Order", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=resetItems).pack(side="right", padx=20)


def manageMenusScreen(mWin):
    mWin.withdraw()
    manageMenusWin = tk.Toplevel()
    manageMenusWin.title("Menus Screen")
    manageMenusWin.attributes('-fullscreen', True)
    manageMenusWin.bind("<Escape>", lambda event: manageMenusWin.attributes('-fullscreen', False))
    manageMenusWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(manageMenusWin, mWin))

    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(manageMenusWin,bg="#000000")
    topFrame.pack(fill="x")
    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)

    manageMenusLogo = tk.PhotoImage(file="manageMenusLogo.png")
    manageMenusIcon = tk.Label(logoFrame, image=manageMenusLogo,bg="#7E8181")
    manageMenusIcon.image = manageMenusLogo
    manageMenusIcon.pack(side="left")

    tk.Label(logoFrame, text="Manage Menus", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="       ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)

    # ---------- SCROLLABLE LIST ----------
    container = tk.Frame(manageMenusWin)
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

    # ---------- LOAD MENUS ----------
    allMenus = []
    menuObjects = []
    try:
        with open("menusFile.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                contentList = row["menuContent"].split("|") if row["menuContent"] else []
                allMenus.append(Menu(row["menuID"], row["menuName"], row["menuCategory"], contentList))
    except FileNotFoundError:
        messagebox.showerror("Error", "menusFile.csv not found")
        return False
    
    menuObjects[:] = allMenus[:]

    # ---------- ROW SELECTION ----------
    selected = {"object": None, "widgets": []}

    def selectRow(menuObj, widgets):
        # Reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")
        # Highlight current
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
        selected["object"] = menuObj
        selected["widgets"] = widgets
        
    # ---------- RENDER ROWS (FIX: extracted rendering logic) ----------
    def displayMenus(menu):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []

        for r, obj in enumerate(menu):
            rowWidgets = []
            values = [obj.menuID, obj.menuName, obj.menuCategory]


            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=30)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")


                # ---------- FIX: correct lambda capture ----------
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayMenus(menuObjects)

    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a menu first")
            return
        selected["object"].viewMenu(manageMenusWin)

    # ---------- SEARCH ----------
    searchFrame = tk.Frame(manageMenusWin)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Menu (menuID / menuName):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchMenu():
        query = searchEntry.get().strip().lower()
        if not query:
            displayCustomers(menuObjects)
            return
        results = []
        for c in menuObjects:
            if (query in c.menuID or query in c.menuName.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Menu not found")
            return
        displayMenus(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchMenu).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayMenus(menuObjects)).pack(side="left")
    
    def filterMenus():
        filterWin = tk.Toplevel(manageMenusWin)
        filterWin.title("Filter Menus")
        filterWin.geometry("900x300")
        filterWin.grab_set()
        tk.Label(filterWin, text="Enter the category you want to filter by below:", font=("Arial", 12, "bold")).pack(pady=10)
        categoryPickEntry= tk.Entry(filterWin)
        categoryPickEntry.pack(pady=10)

        def sortAndRefresh():
            categoryPick=categoryPickEntry.get()
            field = "menuCategory"

            menuObjects[:] = allMenus[:]
            navigationMenu.filterRecords(menuObjects,field,categoryPick)
            displayMenus(menuObjects)
            filterWin.destroy()
        tk.Button(filterWin,text="Confirm Filtering",width=20,command= sortAndRefresh).pack(pady=5)
    
    def resetMenus():
        menuObjects[:] = allMenus[:]
        displayMenus(menuObjects)

    def addMenu():
        Menu(None, "", "", []).addMenu(manageMenusWin,mWin)
    
    def editMenu():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a menu first")
            return
        selected["object"].editMenu(manageMenusWin,mWin)

    def deleteMenu():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select a menu first")
            return
        selected["object"].deleteMenu()
        manageMenusWin.destroy()
        manageMenusScreen(mWin)

    # ---------- BUTTONS ----------
    btnFrame = tk.Frame(manageMenusWin)
    btnFrame.pack(pady=15)
    tk.Button(btnFrame, text="Back To Meals", width=15, font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command=lambda: navigationMenu.onClose(manageMenusWin, mWin)).pack(side="left", padx=20)
    tk.Button(btnFrame, text="View Menu Details", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left", padx=20)
    tk.Button(btnFrame, text="Edit Menu", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=editMenu).pack(side="left", padx=20)
    tk.Button(btnFrame, text="Add Menu", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=addMenu).pack(side="right", padx=20)
    tk.Button(btnFrame, text="Delete Menu", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=deleteMenu).pack(side="right", padx=20)

    # ---------- BUTTONS ----------
    btnFrame2 = tk.Frame(manageMenusWin)
    btnFrame2.pack(pady=15)
    tk.Button(btnFrame2,text="Reset Filters",width=20,font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=resetMenus).pack(side="left",padx=10)
    tk.Button(btnFrame2, text="Filter Menus By Category", width=25, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=filterMenus).pack(side="right",padx=10)


def manageItemsScreen(mWin):
    mWin.withdraw()
    manageItemsWin = tk.Toplevel()
    manageItemsWin.title("Items Screen")
    manageItemsWin.attributes('-fullscreen', True)
    manageItemsWin.bind("<Escape>", lambda event: manageItemsWin.attributes('-fullscreen', False))
    manageItemsWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(manageItemsWin, mWin))

    # ---------------- TOP BAR ----------------
    topFrame = tk.Frame(manageItemsWin,bg="#000000")
    topFrame.pack(fill="x")
    logoFrame = tk.Frame(topFrame,bg="#7E8181")
    logoFrame.pack(side="left",fill="x",pady=5,padx=10)

    viewItemsLogo = tk.PhotoImage(file="manageItemsLogo.png")
    viewItemsIcon = tk.Label(logoFrame, image=viewItemsLogo,bg="#7E8181")
    viewItemsIcon.image = viewItemsLogo
    viewItemsIcon.pack(side="left")

    tk.Label(logoFrame, text="Manage Items", font=("Arial", 24, "bold"),bg="#7E8181",fg="white").pack(side="left", padx=30)
    tk.Label(logoFrame, text="       ", font=("Arial", 24, "bold"),bg="#7E8181").pack(side="left", padx=30)
    tk.Message(topFrame,bg="#000000").pack(side="right",padx=40)

    container = tk.Frame(manageItemsWin)
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

    allItems = []
    itemObjects = []
    try:
        with open("itemsFile.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                    ingredientsList = row["itemIngredients"].split("|")
                    allItems.append(
                        Item(row["itemID"],row["itemName"],row["itemPrice"],ingredientsList))
    except FileNotFoundError:
        messagebox.showerror("Error", "itemsFile.csv not found")
        return False
    itemObjects[:] = allItems[:]

    selected = {"object": None,"widgets": []}
    def selectRow(itemObj, widgets):# reset previous selection
        for w in selected["widgets"]:
            w.config(readonlybackground="grey", fg="black", relief="sunken")# highlight current selection
        for w in widgets:
            w.config(readonlybackground="#4da6ff", fg="white", relief="raised")
       
        selected["object"] = itemObj
        selected["widgets"] = widgets
   
    # ---------- RENDER ROWS ---------- 
    def displayItems(item):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()
        selected["object"] = None
        selected["widgets"] = []

        for r, obj in enumerate(item):
            rowWidgets = []
            values = [obj.itemID, obj.itemName, obj.itemPrice]

            for c, val in enumerate(values):
                entry = tk.Entry(scrollableFrame, font=("Arial", 14), width=30)
                entry.insert(0, val)
                entry.config(state="readonly",readonlybackground="grey", fg="black")
                entry.grid(row=r, column=c, padx=6, pady=4, sticky="w")
                entry.bind("<Button-1>",lambda e, o=obj, w=rowWidgets: selectRow(o, w))
                rowWidgets.append(entry)
    displayItems(itemObjects)

    def viewSelected():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select an item first")
            return
        selected["object"].viewItem(manageItemsWin)

    # ---------- SEARCH ----------
    searchFrame = tk.Frame(manageItemsWin)
    searchFrame.pack(pady=10)
    tk.Label(searchFrame,text="Search Item (itemID / itemName):").pack(side="left")
    searchEntry = tk.Entry(searchFrame, width=30)
    searchEntry.pack(side="left", padx=5)


    def searchItem():
        query = searchEntry.get().strip().lower()
        if not query:
            displayCustomers(itemObjects)
            return
        results = []
        for c in itemObjects:
            if (query in c.itemID or query in c.itemName.lower()):
                results.append(c)
        if not results:
            messagebox.showerror("Error", "Item not found")
            return
        displayItems(results)


    tk.Button(searchFrame, text="Search", width=12, command=searchItem).pack(side="left", padx=5)
    tk.Button(searchFrame, text="Reset", width=12, command=lambda: displayItems(itemObjects)).pack(side="left")
     
    def sortItemsByPrice():
        sortWin = tk.Toplevel(manageItemsWin)
        sortWin.title("Sort Items By Price")
        sortWin.geometry("900x300")
        sortWin.grab_set()


        def sortAndRefresh(field):
            navigationMenu.SortRecordsAscending(itemObjects, field)
            displayItems(itemObjects)
            sortWin.destroy()


        def sortAndRefreshDecending(field):
            navigationMenu.SortRecordsDecending(itemObjects, field)
            displayItems(itemObjects)
            sortWin.destroy()
        
        tk.Button(sortWin,text="Sort By Price (Ascending)",width=20,command=lambda: sortAndRefresh("itemPrice")).pack(pady=5)
        tk.Button(sortWin,text="Sort By Price (Decending)",width=20,command=lambda: sortAndRefreshDecending("itemPrice")).pack(pady=5)
    
    def resetItems():
        itemObjects[:] = allItems[:]
        displayItems(itemObjects)
    
    def addItem():
        Item(None, "", "", []).addItem(manageItemsWin,mWin)


    def editItem():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select an item first")
            return
        selected["object"].editItem(manageItemsWin,mWin)


    def deleteItem():
        if selected["object"] is None:
            messagebox.showwarning("Warning", "Select an item first")
            return
        selected["object"].deleteItem()
        manageItemsWin.destroy()
        manageItemsScreen(mWin)
    
    btnFrame = tk.Frame(manageItemsWin)
    btnFrame.pack(pady=15)
    tk.Button(btnFrame, text="Back To Meals", width=15, font=("Arial", 12,"bold"),
              bg="#171717", fg="white",command= lambda: navigationMenu.onClose(manageItemsWin, mWin)).pack(side="left",padx=20)
    tk.Button(btnFrame, text="View Item Details", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=viewSelected).pack(side="left",padx=20)
    tk.Button(btnFrame, text="Edit Item", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command= editItem).pack(side="left",padx=20)
    tk.Button(btnFrame, text="Add Item", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command= addItem).pack(side="right",padx=20)
    tk.Button(btnFrame, text="Delete Item", width=15, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command= deleteItem).pack(side="right",padx=20)


    btnFrame2 = tk.Frame(manageItemsWin)
    btnFrame2.pack(pady=15)
    tk.Button(btnFrame2, text="Reset Items Order", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=resetItems).pack(side="left", padx=10)
    tk.Button(btnFrame2, text="Sort Items By Price", width=20, font=("Arial", 12,"bold"),
              bg="#2A79A4", fg="white",command=sortItemsByPrice).pack(side="right", padx=10)

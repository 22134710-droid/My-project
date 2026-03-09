import tkinter as tk
import navigationMenu


def register(previousWin):
    navigationMenu.logInWin.withdraw()
    registerWin = tk.Toplevel()
    registerWin.attributes('-fullscreen', True)
    registerWin.bind("<Escape>", lambda event: registerWin.attributes('-fullscreen', False))
    registerWin.title("Sign up Form")
    registerWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.onClose(registerWin,previousWin))
   
    def onMousewheel(event): # mouse action for the scrollbar
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
   
    #dimensions measures
    fieldsWidth=120
    fieldsHeight=12
    fieldsBorder= 2
    horizontalBorder= 5
    fontSize= 10
    labelsFontSize=15
    iconPadding=765
    buttonsHeight= 2
    buttonsWidth= 15
    buttonsPadding=50


    topFrame =tk.Frame(registerWin, bg="#000000")
    topFrame.pack(fill="x")
   
    userDetails= tk.Label(topFrame, text= "Account Details", width=20,height=3,
                          font=("Arial", 24, "bold"), bg="#7E8181",fg="white")
    userDetails.grid(row=0,column=0,sticky="w",padx=5,pady=5)


    restaurantLogo = tk.PhotoImage(file="a2 project restaurant official logo.png")
    restaurantIcon = tk.Label(topFrame, image=restaurantLogo)
    restaurantIcon.image = restaurantLogo  
    restaurantIcon.grid(row=0,column=1,padx=iconPadding)


    # scollbar
    container = tk.Frame(registerWin)
    container.pack(fill="both", expand=True)
    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, width=24)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)


    scrollableFrame = tk.Frame(canvas)
    scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.bind_all("<MouseWheel>", onMousewheel)


    userDet = tk.Frame(scrollableFrame)  
    userDet.pack(fill="x")


    userDetails= tk.Label(userDet, text= "User Details", width=20, font=("Arial", labelsFontSize, "bold"))
    userDetails.grid(row=0,column=0,sticky="w",ipady=10)


    firstname= tk.Entry(userDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    firstname.placeholder = "Firstname"
    firstname.insert(0, firstname.placeholder)
    firstname.bind("<FocusIn>", navigationMenu.removePlaceholder)
    firstname.bind("<FocusOut>", navigationMenu.addPlaceholder)
    firstname.grid(row=1,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    surname= tk.Entry(userDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    surname.placeholder = "Surname"
    surname.insert(0, surname.placeholder)
    surname.bind("<FocusIn>", navigationMenu.removePlaceholder)
    surname.bind("<FocusOut>", navigationMenu.addPlaceholder)
    surname.grid(row=2,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    setPassword= tk.Entry(userDet,width=fieldsWidth, fg="grey",border=fieldsBorder, font=("Arial", fontSize), justify="center")
    setPassword.placeholder = "Set Password"
    setPassword.insert(0, setPassword.placeholder)
    setPassword.bind("<FocusIn>", navigationMenu.removePlaceholder)
    setPassword.bind("<FocusOut>", navigationMenu.addPlaceholder)
    setPassword.grid(row=3,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    phoneNum= tk.Entry(userDet,width=fieldsWidth, fg="grey",border=fieldsBorder, font=("Arial", fontSize), justify="center")
    phoneNum.placeholder = "Phone Number"
    phoneNum.insert(0, phoneNum.placeholder)
    phoneNum.bind("<FocusIn>", navigationMenu.removePlaceholder)
    phoneNum.bind("<FocusOut>", navigationMenu.addPlaceholder)
    phoneNum.grid(row=4,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    Email= tk.Entry(userDet,width=fieldsWidth, fg="grey",border=fieldsBorder, font=("Arial", fontSize), justify="center")
    Email.placeholder = "Email"
    Email.insert(0, Email.placeholder)
    Email.bind("<FocusIn>", navigationMenu.removePlaceholder)
    Email.bind("<FocusOut>", navigationMenu.addPlaceholder)
    Email.grid(row=5,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    Location= tk.Entry(userDet,width=fieldsWidth, fg="grey",border=fieldsBorder, font=("Arial", fontSize), justify="center")
    Location.placeholder = "Location"
    Location.insert(0, Location.placeholder)
    Location.bind("<FocusIn>", navigationMenu.removePlaceholder)
    Location.bind("<FocusOut>", navigationMenu.addPlaceholder)
    Location.grid(row=6,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)
    LocationExample= tk.Label(userDet,text="Example: CF10 1AA",font=("Arial", 9),fg="grey")
    LocationExample.grid(row=7, column=0, sticky="w")


    personDet = tk.Frame(scrollableFrame)
    personDet.pack(fill="x")
    personalDetails= tk.Label(personDet, text= "Personal Details", width=20, font=("Arial", labelsFontSize, "bold"))
    personalDetails.grid(row=0,column=0,sticky="w",ipady=10)


    gender= tk.Entry(personDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    gender.placeholder = "Gender"
    gender.insert(0, gender.placeholder)
    gender.bind("<FocusIn>", navigationMenu.removePlaceholder)
    gender.bind("<FocusOut>", navigationMenu.addPlaceholder)
    gender.grid(row=1,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    age= tk.Entry(personDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    age.placeholder = "Age"
    age.insert(0, age.placeholder)
    age.bind("<FocusIn>", navigationMenu.removePlaceholder)
    age.bind("<FocusOut>", navigationMenu.addPlaceholder)
    age.grid(row=2,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    ethnicity= tk.Entry(personDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    ethnicity.placeholder = "Ethnicity"
    ethnicity.insert(0, ethnicity.placeholder)
    ethnicity.bind("<FocusIn>", navigationMenu.removePlaceholder)
    ethnicity.bind("<FocusOut>", navigationMenu.addPlaceholder)
    ethnicity.grid(row=3,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    favMeal= tk.Entry(personDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    favMeal.placeholder = "Favourite Meal"
    favMeal.insert(0, favMeal.placeholder)
    favMeal.bind("<FocusIn>", navigationMenu.removePlaceholder)
    favMeal.bind("<FocusOut>", navigationMenu.addPlaceholder)
    favMeal.grid(row=4,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    favColor= tk.Entry(personDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    favColor.placeholder = "Favourite Colour"
    favColor.insert(0, favColor.placeholder)
    favColor.bind("<FocusIn>", navigationMenu.removePlaceholder)
    favColor.bind("<FocusOut>", navigationMenu.addPlaceholder)
    favColor.grid(row=5,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    knownFor= tk.Entry(personDet,width=fieldsWidth, fg="grey", border=fieldsBorder, font=("Arial", fontSize), justify="center")
    knownFor.placeholder = "How long you've known our resturant for?"
    knownFor.insert(0, knownFor.placeholder)
    knownFor.bind("<FocusIn>", navigationMenu.removePlaceholder)
    knownFor.bind("<FocusOut>", navigationMenu.addPlaceholder)
    knownFor.grid(row=6,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    close = tk.Button(personDet, width=25, text="Back To Login/ Previous Screen", height = buttonsHeight,
                      font=("Arial",10,"bold"), bg="#7E8181",fg="white",command=lambda: navigationMenu.onClose(registerWin,previousWin,canvas))
    close.grid(row=0, column=1, sticky="w", pady=5)


    userIdentification = tk.Frame(scrollableFrame)
    userIdentification.pack(fill="x")


    userTypeLabel= tk.Label(userIdentification, text= "Who are you?", width=20, font=("Arial", labelsFontSize, "bold"))
    userTypeLabel.grid(row=0,column=0,sticky="w",ipady=10)


    employeeFrame = tk.Frame(userIdentification)
    employeeDetails= tk.Label(employeeFrame, text="Employee Details", width= 20,
                              font=("Arial", labelsFontSize,"bold"))
    employeeDetails.grid(row=2,column=0,sticky="w",ipady=10)


    jobTitle = tk.Entry(employeeFrame, width=fieldsWidth, fg="grey",
                border=fieldsBorder, font=("Arial", fontSize), justify="center")
    jobTitle.placeholder = "Job Title"
    jobTitle.insert(0, jobTitle.placeholder)
    jobTitle.bind("<FocusIn>", navigationMenu.removePlaceholder)
    jobTitle.bind("<FocusOut>", navigationMenu.addPlaceholder)
    jobTitle.grid(row=3,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)
   
    shift = tk.Entry(employeeFrame, width=fieldsWidth, fg="grey",
                border=fieldsBorder, font=("Arial", fontSize), justify="center")
    shift.placeholder = "Shift"
    shift.insert(0, shift.placeholder)
    shift.bind("<FocusIn>", navigationMenu.removePlaceholder)
    shift.bind("<FocusOut>", navigationMenu.addPlaceholder)
    shift.grid(row=4,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)
   
    dateHired = tk.Entry(employeeFrame, width=fieldsWidth, fg="grey",
                border=fieldsBorder, font=("Arial", fontSize), justify="center")
    dateHired.placeholder = "Date Hired"
    dateHired.insert(0, dateHired.placeholder)
    dateHired.bind("<FocusIn>", navigationMenu.removePlaceholder)
    dateHired.bind("<FocusOut>", navigationMenu.addPlaceholder)
    dateHired.grid(row=5,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)
   
    DOB = tk.Entry(employeeFrame, width=fieldsWidth, fg="grey",
                border=fieldsBorder, font=("Arial", fontSize), justify="center")
    DOB.placeholder = "Date Of Birth"
    DOB.insert(0, DOB.placeholder)
    DOB.bind("<FocusIn>", navigationMenu.removePlaceholder)
    DOB.bind("<FocusOut>", navigationMenu.addPlaceholder)
    DOB.grid(row=6,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)
   
    YOE = tk.Entry(employeeFrame, width=fieldsWidth, fg="grey",
               border=fieldsBorder, font=("Arial", fontSize), justify="center")
    YOE.placeholder = "Years Of Experience"
    YOE.insert(0, YOE.placeholder)
    YOE.bind("<FocusIn>", navigationMenu.removePlaceholder)
    YOE.bind("<FocusOut>", navigationMenu.addPlaceholder)
    YOE.grid(row=7,column=0,ipady=fieldsHeight,sticky="w", padx=horizontalBorder)


    dynamicFrame = tk.Frame(userIdentification)
    dynamicFrame.grid(row=3, column=0, columnspan=3, sticky="w")
   
    def storeDetails():
        # all users fields
        fields= [firstname.get(),surname.get(),setPassword.get(),phoneNum.get(),
                 Email.get(),Location.get(),gender.get(),age.get(),ethnicity.get(),
                 favMeal.get(),favColor.get(),knownFor.get()]
        placeholders = ["Firstname","Surname","Set Password","Phone Number",
                        "Email","Location (Postcode)","Gender","Age","Ethnicity",
                        "Favourite Meal","Favourite Colour","How long you've known our resturant for?"]
        # admins and staff only fields
        fields2= [jobTitle.get(),shift.get(),dateHired.get(),DOB.get(),YOE.get()]
        placeholders2= ["Job Title","Shift","Date Hired",
                           "Date Of Birth","Years Of Experience"]
        navigationMenu.userDetailsList
        # storing user and personal details
        for i in range(len(fields)):
            if str(fields[i]) == placeholders[i]:
                navigationMenu.userDetailsList[i] = ""
            else:
                navigationMenu.userDetailsList[i] = fields[i]
       
        # storing employee details if user is staff or admin
        if navigationMenu.userDetailsList[12] == "staff" or navigationMenu.userDetailsList[12] == "admin":
            for i in range(5):
                if fields2[i] == placeholders2[i]:
                    navigationMenu.userDetailsList[i+13] = ""
                else:
                    navigationMenu.userDetailsList[i+13] = fields2[i]
        elif navigationMenu.userDetailsList[12] == "customer":
            for i in range(5):
                navigationMenu.userDetailsList[i+13] =  ""
        return True
   
    def resetUserType():
        employeeFrame.grid_remove()
        for widget in dynamicFrame.winfo_children():
            widget.destroy()
        customerType.config(state="normal")
        staffType.config(state="normal")
        adminType.config(state="normal")
   
    def customerAction(): # entry1 is the window registerWin, entry2 is the frame userIdentification
        customerType.config(state="disabled")
        staffType.config(state="disabled")
        adminType.config(state="disabled")
        employeeFrame.grid_remove()


        SelectedUserType = ""
        SelectedUserType = "customer"
        close2 = tk.Button(dynamicFrame, width=30, text="Go Back To Login/ Previous Screen", height = 2,
                           font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: navigationMenu.onClose(registerWin,previousWin))
        close2.grid(row=2, column=0, pady=25, padx=60)
 
        createAccount = tk.Button(dynamicFrame, width=30, text="Create Account", height = 2,
                                  font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: requestAccess(SelectedUserType))
        createAccount.grid(row=2, column=1, pady=25, padx=120)
        changeTypeBtn = tk.Button(dynamicFrame,text="Change User Type",width=30,height=2,
                                  font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=resetUserType)
        changeTypeBtn.grid(row=3, column=0, pady=25)
        return True
   
    def staffAction():
        customerType.config(state="disabled")
        staffType.config(state="disabled")
        adminType.config(state="disabled")
        employeeFrame.grid(row=2, column=0, columnspan=2, sticky="w")
       
        SelectedUserType = ""
        SelectedUserType = "staff"
       
        close2 = tk.Button(dynamicFrame, width=30, text="Go Back To Login/ Previous Screen", height = 2,
                           font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: navigationMenu.onClose(registerWin,previousWin))
        close2.grid(row=8, column=0, pady=25, padx=60)
       
        Submit = tk.Button(dynamicFrame, width=30, text="Submit", height = 2,
                           font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: requestAccess(SelectedUserType))
        Submit.grid(row=8, column=1, pady=25, padx=120)


        changeTypeBtn = tk.Button(dynamicFrame,text="Change User Type",width=30,height=2,
                                  font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=resetUserType)
        changeTypeBtn.grid(row=9, column=0, pady=25)
        return True


    def adminAction():
        customerType.config(state="disabled")
        staffType.config(state="disabled")
        adminType.config(state="disabled")
        employeeFrame.grid(row=2, column=0, columnspan=2, sticky="w")
       
        SelectedUserType = ""
        SelectedUserType = "admin"
       
        close2 = tk.Button(dynamicFrame, width=30, text="Go Back To Login/ Previous Screen", height = 2,
                           font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: navigationMenu.onClose(registerWin,previousWin))
        close2.grid(row=8, column=0, pady=25, padx=60)
       
        Submit = tk.Button(dynamicFrame, width=30, text="Submit", height = 2,
                           font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: requestAccess(SelectedUserType))
        Submit.grid(row=8, column=1, pady=25, padx=120)


        changeTypeBtn = tk.Button(dynamicFrame,text="Change User Type",width=30,height=2,
                                  font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=resetUserType)
        changeTypeBtn.grid(row=9, column=0, pady=25)
        return True
   
    def requestAccess(SelectedUserType):
        if SelectedUserType == "customer":
            navigationMenu.userDetailsList[12] = "customer"
            storeDetails()
            if navigationMenu.validateUser():
                return True
            else:
                return False
            
        elif SelectedUserType == "staff":
            navigationMenu.userDetailsList[12] = "staff"
            storeDetails()
            if navigationMenu.validateUser():
                return True
            else:
                return False
            
        elif SelectedUserType == "admin":
            navigationMenu.userDetailsList[12] = "admin"
            storeDetails()
            if navigationMenu.validateUser():
                return True
            else:
                return False
        else:
            return False
   
    customerType = tk.Button(userIdentification, width=buttonsWidth, text="Customer", height = buttonsHeight,
                             font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: customerAction())
    customerType.grid(row=1, column=0,pady=10)
    staffType = tk.Button(userIdentification, width=buttonsWidth, text="Staff", height = buttonsHeight,
                          font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: staffAction())
    staffType.grid(row=1, column=1,pady=10)
    adminType = tk.Button(userIdentification, width=buttonsWidth, text="Admin", height = buttonsHeight,
                          font=("Arial",10,"bold"),bg="#7E8181",fg="white",command=lambda: adminAction())
    adminType.grid(row=1, column=2,padx=buttonsPadding,pady=10)

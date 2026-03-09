import tkinter as tk
import signup
import navigationMenu


navigationMenu.logInWin.attributes('-fullscreen', True)
navigationMenu.logInWin.bind("<Escape>", lambda event: navigationMenu.logInWin.attributes('-fullscreen', False))
navigationMenu.logInWin.title("Log-In Form")
navigationMenu.logInWin.protocol("WM_DELETE_WINDOW", lambda: navigationMenu.closeApp(navigationMenu.logInWin))
navigationMenu.logInWin.configure(bg="#0B0B0B")

topFrame= tk.Frame(navigationMenu.logInWin, bg="#000000")
topFrame.pack(fill="x")

fieldsWidth=53
fieldsHeight=10
fieldsBorder= 2
logoFrameHeight= 25
iconPadding =372

restaurantLogo = tk.PhotoImage(file="a2 project restaurant official logo.png")
restaurantIcon = tk.Label(topFrame, image=restaurantLogo)
restaurantIcon.image = restaurantLogo   # keep reference
restaurantIcon.pack(anchor="e")

mainFrame= tk.Frame(navigationMenu.logInWin, bg="#0B0B0B")
mainFrame.pack(pady=40)

Username= tk.Entry(mainFrame,width=fieldsWidth, fg="grey",border=fieldsBorder, font=("Arial", 16), justify="center")
Username.placeholder = "Username"
Username.insert(0, Username.placeholder)
Username.bind("<FocusIn>", navigationMenu.removePlaceholder)
Username.bind("<FocusOut>", navigationMenu.addPlaceholder)
Username.grid(row=0,column=0,ipady=fieldsHeight)

Password= tk.Entry(mainFrame,width=fieldsWidth, fg="grey",border=fieldsBorder,font=("Arial", 16), justify="center")
Password.placeholder = "Password"
Password.is_password = True
Password.insert(0, Password.placeholder)
Password.bind("<FocusIn>", navigationMenu.removePlaceholder)
Password.bind("<FocusOut>", navigationMenu.addPlaceholder)
Password.grid(row=1,column=0,ipady=fieldsHeight)


def togglePassword(Password):
    if Password.get() == Password.placeholder:
        return
    if Password.cget("show") == "":
        Password.config(show="*")
        toggleButton.config(text="Show")
    else:
        Password.config(show="")
        toggleButton.config(text="Hide")

toggleButton = tk.Button(mainFrame, text="Show", command= lambda: togglePassword(Password))
toggleButton.grid(padx=5,column=1,row=1)

buttonsWidth= 64
buttonsHeight=2

logInOption = tk.Button(mainFrame,text="Log in", width=buttonsWidth,height=buttonsHeight,
                        font=("Arial", 12,"bold"),command= lambda: navigationMenu.loginValidate(Username,Password), bg="#7E8181", fg="white")
logInOption.grid(pady=10,row=2,column=0)

emptySpace = tk.Message(mainFrame,border=25, bg="#0B0B0B")
emptySpace.grid(row=3,column=0)

signUpOption = tk.Button(mainFrame,text="Don't have an account? Sign up here", width=buttonsWidth,
                         height=buttonsHeight,font=("Arial", 12,"bold"),command= lambda: signup.register(navigationMenu.logInWin), bg="#7E8181", fg="white")
signUpOption.grid(row=4,column=0)
contactOption = tk.Button(mainFrame,text="Contact Us", width=buttonsWidth,height=buttonsHeight,
                          font=("Arial", 12,"bold"),command= lambda: navigationMenu.contactUs(), bg="#7E8181", fg="white")
contactOption.grid(row=5,column=0)


bottomFrame = tk.Frame(navigationMenu.logInWin, bg="#0B0B0B")
bottomFrame.pack(pady=40, anchor="w")
closeAppOption = tk.Button(bottomFrame, width=25, text="Close App", height=2, command=lambda: navigationMenu.closeApp(navigationMenu.logInWin))
closeAppOption.pack(pady=10,padx=5)


navigationMenu.logInWin.mainloop()

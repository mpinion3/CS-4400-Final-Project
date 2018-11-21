from tkinter import *
from tkinter import messagebox
import pymysql
import time
from datetime import *
import calendar

class CS4400:
    def __init__(self,rootWin):
        self.longWin = 
        self.Login(rootWin)
        self.departsFromList = []
        self.arrivesAtList = []
        self.isFirstClassList = []
        self.tripPriceList = []
        self.resTrainNumberList = []
        self.tripDurationList = []
        self.numBagsList = []
        self.pNameList = []
        self.dateList = []

    def Connect(self):
        try:
            self.db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", db = "cs4400_Team_52", user = "cs4400_Team_52", passwd = "hriZUPo_")
            return(self.db)
        except:
            messagebox.showerror("Did not connect", "Error: cannot connect")
            return

    def Login(self,rootWin):
        self.loginWin=rootWin          #creates the parameter window
        self.loginWin.title('Login')#names Login Window

        self.isStudent = "NO"

        f2=Frame(self.loginWin)     #creates a frame for the entry boxes and labels

        userL=Label(f2, text='Username').grid(row=0,column=0,sticky=E)  #username labels and entry boxes aligned East
        self.CustUsername=Entry(f2,width=30)
        self.CustUsername.grid(row=0, column=1)

        passL=Label(f2, text='Password').grid(row=1,column=0,sticky=E)  #password labels and entry boxes aligned East
        self.CustPassword=Entry(f2,width=30,show="*")
        self.CustPassword.grid(row=1, column=1)

        f2.pack(padx=50,pady=50)   #puts the frame in the gui and anchors it West


        f3=Frame(self.loginWin)     #creates a frame for the buttons

        b1=Button(f3, text='Login',width=10,command=self.CheckLogin)   #creates a registration button
        b1.grid(row = 0, column = 0,padx=30)


        b2=Button(f3, text='Register', bd=0, command=self.New_User)   #creates login button
        ##
        ##Should this delete the login window? It just minimizes it
        ##
        b2.grid(row=0,column=2)

        f3.pack(side=BOTTOM,anchor=E)   #puts the frame in the gui and anchors it to the right



    def New_User(self):

        self.loginWin.iconify()

        self.nuWin=Toplevel()
        self.nuWin.title("New User Registration")

        f2=Frame(self.nuWin)

        userL=Label(f2, text='Username:').grid(row=0,column=0,sticky=W,padx=5)  #username labels and entry boxes aligned East
        self.NUuser=Entry(f2,width=30)
        self.NUuser.grid(row=0, column=1,pady=2)

        email=Label(f2, text='Email Address:').grid(row=1,column=0,sticky=W,padx=5)  #email labels and entry boxes aligned East
        self.NUemail=Entry(f2,width=30)
        self.NUemail.grid(row=1,column=1,pady=2)

        passL=Label(f2, text='Password:').grid(row=2,column=0,sticky=W,padx=5)  #password labels and entry boxes aligned East
        self.NUpassword=Entry(f2,width=30,show="*")
        self.NUpassword.grid(row=2,column=1,pady=2)

        con_passL=Label(f2, text='Confirm Password:').grid(row=3,column=0,sticky=W,padx=5)  #password labels and entry boxes aligned East
        self.NUconfirm=Entry(f2,width=30,show="*")
        self.NUconfirm.grid(row=3,column=1,pady=2)

        f2.pack(padx=30, pady=20)

        f3=Frame(self.nuWin)     #creates a frame for the buttons

        b1=Button(f3, text='Create',width=10, command=self.RegisterNew)   #creates a registration button
        b1.grid(row = 0, column = 0,padx=30,pady=10)
        f3.pack(side=BOTTOM,anchor=E)

    def RegisterNew(self):
        self.UserName=self.NUuser.get()
        self.Email=self.NUemail.get()
        self.Password=self.NUpassword.get()
        confirm=self.NUconfirm.get()

        if self.UserName=="":            #if there is nothing in the username entry box...
            messagebox.showerror('Input Error','Must have a Username')      #show an error message and end register new
            return
        elif len(self.UserName)>50:      #if there the username is longer than 20 characters...
            messagebox.showerror('Input Error','Your Username is too long!')  #show an error message and end register new
            return
        elif self.Password != confirm:          #if the two passwords do not match...
            messagebox.showerror('Input Error','Passwords do not match')    #show an error message and end register new
            return

        db=self.Connect()   #runs method for connecting
        if db==None:        #if self.Connect returns nothing then end register new
            return

        cursor=db.cursor()  #creates a cursor


        sql = '''INE Username FROM Users WHERE Username = %s'''
        cursor.execute(sql, self.UserName)    #searches through database to find any usernames that are the same as what the user has entered
        fetch = cursor.fetchall()
        LocalnameList = fetch
        
        if len(LocalnameList)!= 0:   #if the list of things found is not empty...
            messagebox.showerror("Input Error",'This Username already exists!') #show an error message and end register new
            return
        else:
            sql2 = '''INSERT INTO Users(Username, Password) VALUES (%s, %s)'''
            cursor.execute(sql2,(self.UserName, self.Password))
            sql3 = '''INSERT INTO Customer(Username, Email) VALUES (%s, %s)'''
            cursor.execute(sql3,(self.UserName, self.Email))
            db.commit() ##not sure if this is necessary/what its supposed to do
            cursor.close()  #adds the entry info into the database without a first name, commits it to the database and then closes the cursor
            self.nuWin.withdraw()
            self.Functionality()
            ## self.Prop_Res()


    def CheckLogin(self):
        self.UserName=self.CustUsername.get()
        self.Password=self.CustPassword.get()

        db=self.Connect()   #runs method for connecting
        if db==None:        #if self.Connect returns nothing then end register new
            return
        cursor=db.cursor()
        sql = '''SELECT A.Username, A.Password FROM Users AS A NATURAL JOIN Customer AS B WHERE A.Username = %s AND A.Password = %s'''
        cursor.execute(sql, (self.UserName,self.Password))    #searches through database to find any usernames that are the same as what the user has entered
        fetch = cursor.fetchall()
        LocalnameList = fetch
        
        if len(LocalnameList) == 0:
            sql = '''SELECT A.Username, A.Password FROM Users AS A NATURAL JOIN Manager AS B WHERE A.Username = %s AND A.Password = %s'''
            cursor.execute(sql, (self.UserName, self.Password))
            fetch2 = cursor.fetchall()
            ManagerNames = fetch2
            
            if len(ManagerNames) == 0:
                messagebox.showerror("you have entered in an incorrect username/password combination","you are dumb. you have entered in an incorrect username/password combination.")

            else:
                self.ManagerFunctionality()
                return

        else:
                    
            self.loginWin.withdraw()
            self.Functionality()
            
        db.commit()
        cursor.close()



    def Functionality(self):


        self.nueWind=Toplevel()
        self.nueWind.title("Choose Functionality")

        f22=Frame(self.nueWind)

        TrainS=Button(f22, text='View Train Schedule', fg='blue', command=self.TrainSchedule).grid(row=0,column=0,sticky=EW,padx=5)  #View Train Schedule Button and entry boxes aligned Middle

        Make=Button(f22, text='Make A Reservation', command=self.MakeReservation).grid(row=1,column=0,sticky=EW,padx=5)  #Make a Reservation Button and entry boxes aligned Middle

        Update=Button(f22, text='Update A Reservation', command = self.UpdateReservation).grid(row=2,column=0,sticky=EW,padx=5)  #Update a Reservation Button and entry boxes aligned Middle

        Cancel=Button(f22, text='Cancel A Reservation', command=self.CancelReservation).grid(row=3,column=0,sticky=EW,padx=5)  #Cancel a Reservation Button and entry boxes aligned Middle

        ViewReview=Button(f22, text='View Review', command = self.Review).grid(row=4,column=0,sticky=EW,padx=5)  #View Review Button and entry boxes aligned Middle

        GiveReview = Button(f22, text="Give Review",command=self.GiveReview).grid(row=5, column=0, sticky=EW, padx=5)

        Confirm=Button(f22, text='Add School Information (Student Discount)', command=self.AddSchoolInfo).grid(row=6,column=0,sticky=EW,padx=5)  #Add School Information button and entry boxes aligned Middle


        bp=Button(f22, text='Log Out',width=10, command=self.LogOut)   #creates a Log Out button
        bp.grid(row = 7, column = 1,padx=30,pady=10)
        f22.pack(side=BOTTOM,anchor=E,padx=30, pady=20)

    def LogOut(self):

        self.loginWin.deiconify()
        self.nueWind.withdraw()

    def ManagerLogOut(self):
        self.loginWin.deiconify()
        self.managerWin.withdraw()


    def AddSchoolInfo(self):

        self.nueWind.withdraw()


        self.schoolwin=Toplevel()
        self.schoolwin.title("Add School Info")

        f23=Frame(self.schoolwin)

        L=Label(f23, text='School Email Address').grid(row=0,column=0,sticky=E)  #School Email Address labels and entry boxes aligned East
        self.schoolemail=Entry(f23,width=30)
        self.schoolemail.grid(row=0, column=1, sticky = E)
        L2=Label(f23, text='Your Email Address Ends with .edu').grid(row=1,sticky=EW)

        b=Button(f23, text="Back", width=10, command=self.Back) #adds Back button
        b.grid(row=2, column = 0, padx=30)
        b1=Button(f23, text="Submit", width=10, command=self.CheckSchoolInfo) #adds Submit button
        b1.grid(row=2, column = 1, padx = 30)

        f23.pack(side = BOTTOM, anchor = E, padx=30, pady=20)

    def Back(self):
        self.schoolwin.withdraw()
        self.nueWind.deiconify()

    def CheckSchoolInfo(self):

        db=self.Connect()   #runs method for connecting
        if db==None:        #if self.Connect returns nothing then end register new
            return
        cursor=db.cursor()  #creates a cursor

        email = self.schoolemail.get()
        if email[-4:] == '.edu':
            self.isStudent = "YES"
            sql = '''UPDATE Customer SET Is_Student = '1' WHERE Username = %s'''
            cursor.execute(sql, self.UserName)    #insert "yes" boolean as school email into customer
            fetch = cursor.fetchall()
            self.schoolwin.withdraw()
            self.nueWind.deiconify()
        else:
            self.isStudent = "NO"
            messagebox.showerror('Input Error','This is not a student email.')

        db.commit() ##not sure if this is necessary/what its supposed to do
        cursor.close()  #adds the entry info into the database without a first name, commits it to the database and then closes the cursor


    def TrainSchedule(self):

        ##        self.loginWin.iconify()
        ##      does it need that line of code? ^^

        self.trainS=Toplevel()
        self.trainS.title("View Train Schedule")

        f=Frame(self.trainS)

        L=Label(f, text='Train Number').grid(row=0,column=0,sticky=E)  #Train Number label & entry boxes aligned East
        self.trainNum=Entry(f,width=30)
        self.trainNum.grid(row=0, column=1, sticky = E)

        b=Button(f, text="Search", width=10, command=self.PullTrainSchedule) #adds Search button
        b.grid(row=2, column = 0, padx=30)

        f.pack(side = BOTTOM, anchor = E, padx=30, pady=20)

    def PullTrainSchedule(self):
        self.trainSchedWin = Toplevel()
        self.trainSchedWin.title("View Train Schedule")

        searchTrain = self.trainNum.get()

        db=self.Connect()   #runs method for connecting
        if db==None:        #if self.Connect returns nothing then end register new
            return
        cursor=db.cursor()  #creates a cursor
        sql = '''SELECT Arrival_Time, Departure_Time, Name FROM Stops WHERE Train_Number = %s ORDER BY Arrival_Time'''

        cursor.execute(sql, searchTrain)
        trainschedule = cursor.fetchall()


        db.commit() ##not sure if this is necessary/what its supposed to do
        cursor.close()  #adds the entry info into the database without a first name, commits it to the database and then closes the cursor


        f=Frame(self.trainSchedWin)


        Number = self.trainNum.get() ##pulling train number from user entry

        frameRows = 1



        L=Label(f,text="Train (Train Number)").grid(row=0, column=0, sticky=E)
        L2=Label(f,text="Arrival Time").grid(row=0,column=1,sticky=E)
        L3=Label(f,text="Departure Time").grid(row=0,column=2,sticky=E)
        L4=Label(f,text="Station").grid(row=0,column=3,sticky=E)
        L5=Label(f, text=Number).grid(row=1,column=0, sticky=E)


        for train in trainschedule:
            LT = Label(f, text=train[0]).grid(row=frameRows, column=1)
            LT2 = Label(f, text=train[1]).grid(row=frameRows, column=2)
            LT3 = Label(f, text=train[2]).grid(row=frameRows, column=3)
            frameRows=frameRows+1



        b=Button(f, text="back", width=10, command = self.trainscheduleback)
        b.grid(column=0, row=(frameRows+1))

        f.pack()


    def trainscheduleback(self):
        self.trainSchedWin.withdraw()
        self.nueWind.deiconify()

        #destroys train schedule window & brings back up functionality window

    def MakeReservation(self):
        self.resPage = Toplevel()
        self.resPage.title("Make Reservation")

        f = Frame(self.resPage)

        l1 = Label(f, text='Search Train').grid(row=0, column=0, columnspan = 2, sticky=EW)
        l2 = Label(f, text = 'Departs From').grid(row = 1, column = 0, sticky = W)
        l3 = Label(f, text = 'Arrives At').grid(row = 2, column = 0, sticky = W)
        l2 = Label(f, text = 'Departure Date').grid(row = 3, column = 0, sticky = W)

        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return

        self.stationList = []
        sql = '''SELECT * FROM Station'''
        cursor = db.cursor()
        cursor.execute(sql)
        fetch = cursor.fetchall()

        self.departsFrom = StringVar()
        self.departsFrom.set(fetch[0])
        self.arrivesAt = StringVar()
        self.arrivesAt.set(fetch[0])

        self.departsFromDropDown = OptionMenu(f, self.departsFrom, *fetch)
        self.departsFromDropDown.grid(row=1, column=1, sticky=E)
        self.arrivesAtDropDown = OptionMenu(f, self.arrivesAt, *fetch)
        self.arrivesAtDropDown.grid(row=2, column=1, sticky=E)
        # TODO need to import date somehow.
        ##
        ##
        ##
        self.departDateStrVar = StringVar()
        self.departsOnDate = Entry(f, width=20, textvariable = self.departDateStrVar)
        self.departsOnDate.grid(row=3, column=1, sticky=E)
        
        
        

        b = Button(f, text="Find Trains", width=10, command=self.FindTrains)  # adds Search button
        b.grid(row=4, column=0, padx=30)

        f.pack(side=BOTTOM, anchor=E, padx=30, pady=20)

    def FindTrains(self):
        self.resPage.withdraw()
        departsFrom = ''
        for i in self.departsFrom.get()[1:]:
            if i!= "'":
                if i == ",":
                    break
                departsFrom += i

        arrivesAt = ''
        for i in self.arrivesAt.get()[1:]:
            if i != "'":
                if i == ",":
                    break
                arrivesAt += i

        self.dateList.append(self.departDateStrVar.get())
        
        
        self.departsFromList.append(departsFrom)
        self.arrivesAtList.append(arrivesAt)
        

        self.selectDeparture = Toplevel()
        self.selectDeparture.title("Select Departure")

        f = Frame(self.selectDeparture)

        l1 = Label(f, text = 'Train \n (Train Number)').grid(row = 0, column = 0)
        l2 = Label(f, text = 'Time \n (Duration)').grid(row = 0, column = 1)
        l3 = Label(f, text = '1st Class Price').grid(row = 0, column = 2)
        l4 = Label(f, text = '2nd Class Price').grid(row = 0, column = 3)

        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return

        cursor = db.cursor()
        sql = "SELECT Train_Number, Departure_Time FROM Stops WHERE Name = %s"
        cursor.execute(sql, departsFrom)
        fetchDeparture = cursor.fetchall()


        sql = '''SELECT Train_Number, Arrival_Time FROM Stops WHERE Name = %s'''
        cursor.execute(sql, arrivesAt)
        fetchArrival = cursor.fetchall()


        myList = []
        arrTimesList = []

        for i in fetchDeparture:
            for j in fetchArrival:
                if i[1] != None and j[1] != None and i[0] == j[0] and i[1] < j[1]:
                    myList.append(i)
                    arrTimesList.append(j[1])

        if len(myList) == 0:
            messagebox.showerror("No trains travel this route", "No trains travel this route, pick a different one")
            self.selectDeparture.withdraw()
            return


        priceList = []
        for i in myList:
            sql = '''SELECT Train_Number, First_Class_Price, Second_Class_Price FROM Train_Route WHERE
                    Train_Number = %s'''
            cursor.execute(sql, i[0])
            priceList.append(cursor.fetchone())

        finalList = []

        db.commit()
        cursor.close()

        for i in range(len(myList)):
            tempList = []
            tempList.append(priceList[i][0])
            tempList.append(myList[i][1])
            tempList.append(arrTimesList[i])
            tempList.append(priceList[i][1])
            tempList.append(priceList[i][2])
            finalList.append(tempList)

        radioButList = []
        j = 0
        k = 1
        self.iVar = IntVar()
        for i in finalList:
            j += 1
            self.iVar.set(0)
            lab1 = Label(f, text = i[0]).grid(row = j, column = 0)
            lab2 = Label(f, text = str(i[1]) + ' - ' + str(i[2]) + '\n(' + str(i[2] - i[1])+")").grid(row=j, column=1)
            rad1 = Radiobutton(f, text=i[3], variable = self.iVar, value = k)
            rad1.grid(row=j, column=2)
            rad2 = Radiobutton(f, text=i[4], variable = self.iVar, value = k + 1)
            rad2.grid(row=j, column=3)
            k += 2
        self.finalList = finalList

        
        but = Button(f, text = "Next", command = self.Baggage).grid(row = j + 1, column = 3)
        backBut = Button(f, text = "Back", command = self.GoToMainFromFindTrains).grid(row = j + 1, column= 2)

        f.pack()

    def GoToMainFromFindTrains(self):
        self.selectDeparture.withdraw()
        self.nueWind.deiconify()

    def Baggage(self):

        self.BaggageWin=Toplevel()
        self.BaggageWin.title('Travel Extras & Passenger Info')
        self.selectDeparture.withdraw()

        f=Frame(self.BaggageWin)
        L1=Label(f, text="Number of Baggage").grid(row=0, column=0, sticky=E)
        L2=Label(f, text="Every Passenger can bring up to 4 baggage, 2 free of charge, 2 for $30 per bag").grid(row=1, column = 0, sticky=E)
        L3=Label(f, text="Passenger Name").grid(row=2, column = 0, sticky=E)

        self.NumBagsStringVar = StringVar(f)
        self.NumBagsStringVar.set('1') #default
        X=OptionMenu(f, self.NumBagsStringVar, "1","2","3","4")
        X.grid(row=0, column=1)


        self.PNameStrVar = StringVar()

        self.PName = Entry(f, width=30, textvariable=self.PNameStrVar).grid(row=2, column =1, columnspan=2, sticky=E)

        B1=Button(f, text="Back", width=10, command=self.BaggageBack).grid(row=3, column = 0, sticky=E)
        B2=Button(f, text="Next", width=10, command=self.resTrainNumCall).grid(row=3, column=1, sticky=E)

        f.pack()


    def BaggageBack(self):
        self.BaggageWin.destroy()

    def BaggageNext(self):
        self.BaggageWin.destroy()
        self.RewWin.deiconify()


    def resTrainNumCall (self):

                

        tempInt = self.iVar.get()//2

        

        if tempInt == 0:
            self.isFirstClassList.append(1)
            self.tripPriceList.append(self.finalList[self.iVar.get()//3][3])
            
        else:
            self.isFirstClassList.append(0)
            self.tripPriceList.append(self.finalList[self.iVar.get()//3][4])

        self.resTrainNumberList.append(self.finalList[self.iVar.get()//3][0])
        
        self.tripDurationList.append(self.finalList[self.iVar.get()//3][2] - self.finalList[self.iVar.get()//3][1])
        self.MakeReservation2()



    def MakeReservation2(self):
        self.numBagsList.append(self.NumBagsStringVar.get())
        self.pNameList.append(self.PNameStrVar.get()) #maybe this'll work

        self.ResWin=Toplevel()
        self.BaggageWin.withdraw()

        self.ResWin.title("Make Reservation")




        

        self.PassName = self.PNameStrVar.get()
        NumBags = self.NumBagsStringVar.get()

        f2=Frame(self.ResWin)

        L=Label(f2, text="Currently Selected").grid(column=0, row=0)
        L2 = Label(f2, text="Train (Train Number)").grid(column=0, row=1)
        L3 = Label(f2, text="Time (Duration)").grid(column=1, row=1)
        L4 = Label(f2, text="Departs From").grid(column=2, row=1)
        L5 = Label(f2, text="Arrives At").grid(column=3, row=1)
        L6 = Label(f2, text="Class").grid(column=4, row=1)
        L7 = Label(f2, text="Price").grid(column=5, row=1)
        L8 = Label(f2, text="#of Baggage").grid(column=6, row=1)
        L9 = Label(f2, text="Passenger Name").grid(column=7, row=1)
        L10 = Label(f2, text="Remove").grid(column=8, row=1)

        rowCounter=2

        strVar = StringVar(f2)
        strVar.set('NO')
        if self.isStudent == "YES":
            strVar.set('YES')

        self.totalCost = 0
        for i in self.tripPriceList:
            self.totalCost += float(i)

        if NumBags == "3":
            self.totalCost = self.totalCost + 30

        if NumBags == "4":
            self.totalCost = self.totalCost + 60

        if self.isStudent == "YES":
            self.totalCost= .8 * float(self.totalCost)


        TCstrVar = StringVar(f2)
        TCstrVar.set(self.totalCost)

        db = self.Connect()
        cursor = db.cursor()
        sql ='''SELECT Card_Number FROM Payment_Info WHERE Username = %s'''

        cursor.execute(sql,self.UserName)
        fetch=cursor.fetchall()
        self.cardNumbers = fetch

        cardNumList=[]
        for nums in fetch:
            last4 = nums[0][-4:]

            cardNumList.append(last4)

        if len(cardNumList) == 0:
            cardNumList.append(" ")

        self.CCstrVar = StringVar(f2)
        self.CCstrVar.set(cardNumList[0]) #set to card number
        counter = 0
        self.removeIntVar = IntVar()
        self.removeIntVar.set(-1)

        for i in range(len(self.resTrainNumberList)):

            if self.isFirstClassList[i]==int(1):
                Class="First Class"
            if self.isFirstClassList[i]==int(0):
                Class="Second Class"



            L1Row2 = Label(f2, text=self.resTrainNumberList[i]).grid(column=0, row=2 + i)
            L2Row2 = Label(f2, text=self.tripDurationList[i]).grid(column=1, row=2 + i)
            L3Row2 = Label(f2, text=self.departsFromList[i]).grid(column=2, row=2 + i)
            L4Row2 = Label(f2, text=self.arrivesAtList[i]).grid(column=3, row=2 + i)
            L5Row2 = Label(f2, text=Class).grid(column=4, row=2 + i)
            L6Row2 = Label(f2, text=self.tripPriceList[i]).grid(column=5, row=2 + i)
            L7Row2 = Label(f2, text=self.numBagsList[i]).grid(column=6, row=2 + i)
            L8Row2 = Label(f2, text=self.pNameList[i]).grid(column=7, row=2 + i)
            RButton = Radiobutton(f2, text = '', variable = self.removeIntVar, value = i)
            RButton.grid(column = 8, row = 2 + i)



            counter = counter + 1

        B1 = Button(f2, text="Remove", width=10, command = self.RemoveFunc)
        B1.grid(column=8, row= 2 + counter)


        L11 = Label(f2, text="Student Discount Applied?").grid(column=0, row=3 + counter)



        E1 = Entry(f2, width=10, textvariable=strVar)
        E1.configure(state='readonly')
        E1.grid(column=1, row=3 + counter)


        L12 = Label(f2, text="Total Cost").grid(column=0, row=4 + counter)




        E2 = Entry(f2, width=10, textvariable=TCstrVar)
        E2.configure(state="readonly")
        E2.grid(column=1, row=4 + counter)

        L13 = Label(f2, text="Use Card:").grid(column=0, row=5 + counter)


        X=OptionMenu(f2, self.CCstrVar, *cardNumList) #option menu needs to be credit cards
        X.grid(row=5 + counter, column=1)
       

        B2 = Button (f2, text="Add Card", command = self.PaymentInfo)
        B2.grid(row=5 + counter, column = 2)

        B3 = Button(f2, text="Continue Adding A Train", command=self.contAddTrain)
        B3.grid(row=6 + counter, column=0)

        B4 = Button(f2, text="Back", command=self.baggageBack2).grid(row=7 + counter, column = 0)
        B5 = Button(f2, text="Submit", command=self.getReservationNumber).grid(row=7 + counter, column = 1)

        f2.pack(side=BOTTOM,anchor=E)

        db.commit()
        cursor.close()

    def getReservationNumber(self):
        self.getReservationWindow=Toplevel()
        self.ResWin.withdraw()

        creditCardNumberFinal4 = self.CCstrVar.get()

        for numbers in self.cardNumbers:
            
            if numbers[0][-4:] == creditCardNumberFinal4:
                self.creditCardNumberFinal = numbers[0]
      

        self.getReservationWindow.title("Confirmation")

        db=self.Connect()   
        if db==None:        
            return
        cursor=db.cursor()

        sql1 = '''INSERT INTO Reservation(Username, Card_Number) VALUES (%s, %s)'''

        cursor.execute(sql1, (self.UserName, self.creditCardNumberFinal))
        
        sql = '''SELECT MAX(Reservation_ID) FROM Reservation WHERE Username = %s AND Card_Number = %s'''

        cursor.execute(sql, (self.UserName,self.creditCardNumberFinal))
        reservationID = cursor.fetchall()

        sql3 = '''INSERT INTO Reserves (Train_Number, First_Class, Total_Cost, Departs_From, Arrives_At, Number_Of_Baggage, Passenger_Name, Departure_Date, Reservation_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        for i in range(len(self.resTrainNumberList)):

            TotalCost = float(self.tripPriceList[i])


            if self.numBagsList[i] == '3':
                TotalCost = TotalCost + 30
            if self.numBagsList[i] == '4':
                TotalCost = TotalCost + 60
            

            if self.isStudent == "YES":
                TotalCost = .8 * float(TotalCost)

                
 
            cursor.execute(sql3, (self.resTrainNumberList[i], self.isFirstClassList[i], TotalCost, self.departsFromList[i],self.arrivesAtList[i], self.numBagsList[i], self.pNameList[i], self.dateList[i], reservationID))

        
        db.commit()
        cursor.close()  #adds the entry info into the database without a first name, commits it to the database and then closes the cursor


        f=Frame(self.getReservationWindow)

        L=Label(f, text="Reservation ID").grid(column=0, row=0)
        L2=Label(f, text="Thank you for your purchase! Please save Reservation ID for your records").grid(column=0, row=1, columnspan=2)


        strVar = StringVar(f)
        strVar.set(reservationID[0][0])
        E1 = Entry(f, width=10, textvariable=strVar)
        E1.configure(state='readonly')
        E1.grid(column=1, row=0)

        B=Button(f, text="Go Back to Choose Functionality", command=self.reservationBack).grid(column=0, row=2, columnspan=2)
        f.pack(side=BOTTOM,anchor=E)
    
    def baggageBack2(self):
        self.BaggageWin.deiconify()
        self.ResWin.withdraw()

    def reservationBack(self):
        self.nueWind.deiconify()
        self.getReservationWindow.withdraw()

    def RemoveFunc(self):
        self.departsFromList.pop(self.removeIntVar.get())
        
        self.arrivesAtList.pop(self.removeIntVar.get())
        self.tripDurationList.pop(self.removeIntVar.get())
        self.resTrainNumberList.pop(self.removeIntVar.get())
        
        self.tripPriceList.pop(self.removeIntVar.get())
        self.pNameList.pop(self.removeIntVar.get())
        self.numBagsList.pop(self.removeIntVar.get())
        self.isFirstClassList.pop(self.removeIntVar.get())
        self.ResWin.destroy()
        self.MakeReservation2()


    def contAddTrain(self):
        self.resPage.deiconify()
        self.ResWin.withdraw()

    def Review(self):

        self.Review=Toplevel()

        self.Review.title("View Review")

        f2=Frame(self.Review)

        L=Label(f2, text="Train Number").grid(column=0, row=0)


        self.reviewNum=Entry(f2,width=30)
        self.reviewNum.grid(row=0, column=1)


        B = Button(f2, text="Back", command=self.backFromViewReview).grid(column=1, row=2)
        B2 = Button(f2, text="Next", command=self.SearchReview).grid(column=0, row=2)


        f2.pack(side=BOTTOM,anchor=E)

    def backFromViewReview(self):
        
        self.Review.destroy()

    def GiveReview(self):

        self.GReview=Toplevel()
        self.GReview.withdraw()
        self.GReview.deiconify()

        self.GReview.title("Give Review")

        f2=Frame(self.GReview)

        L=Label(f2, text="Train Number").grid(column=0, row=0)
        L2=Label(f2, text="Rating").grid(column=0, row=1)
        L3=Label(f2, text="Comment").grid(column=0, row=2)

        self.TNstrVar = StringVar(f2)
        E=Entry(f2, width=30, textvariable=self.TNstrVar).grid(column=1, row=0)
        self.commentStrVar = StringVar(f2)
        E2=Entry(f2, width=30, textvariable=self.commentStrVar).grid(column=1, row=2)

        self.ratingStrVar = StringVar(f2)
        self.ratingStrVar.set('Good') #default
        X=OptionMenu(f2, self.ratingStrVar, "Good","Neutral","Bad")
        X.grid(row=1, column=1)

        B=Button(f2, text="Submit", command=self.submitReview).grid(row=3, column=1)

        f2.pack(side=BOTTOM,anchor=E)

    def submitReview(self):

        comment = self.commentStrVar.get()
        
        TN = self.TNstrVar.get()
        if TN == "":
            messagebox.showerror("You must enter a Train Number", "You must enter a Train Number")
            return

        rating = self.ratingStrVar.get()
        if rating == "Good":
            rating = '3'
        if rating == "Neutral":
            rating = '2'
        if rating == "Bad":
            rating = '1'
        
        UN = self.UserName
        

        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return

        sql = '''INSERT INTO Review (Rating, Comment, Train_Number, Username) VALUES (%s, %s, %s, %s)'''
        cursor = db.cursor()
        cursor.execute(sql, (rating, comment, TN, UN))
        fetch = cursor.fetchall()

        db.commit()
        cursor.close()
        self.GReview.destroy()


    def SearchReview(self):
        self.nueWind.withdraw()
        self.viewReview=Toplevel()


        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return
        getReviewNum = self.reviewNum.get()
        

        sql = '''SELECT Rating, Comment FROM Review WHERE Train_Number = %s'''
        cursor = db.cursor()
        cursor.execute(sql, getReviewNum)
        fetch = cursor.fetchall()
        


        self.viewReview.title("View Review")

        f2=Frame(self.viewReview)

        rowCounter = 1

        L=Label(f2, text="Rating").grid(column=0, row=0)
        L1=Label(f2, text="Comment").grid(column=1, row=0)
        L2=Label(f2, text="Good").grid(column=0, row=1)

        goodComment = ""
        badComment = ""
        neutralComment= ""
        for comments in fetch:
            if comments[0] == "3":
                goodComment= goodComment + " | " + comments[1]
            elif comments[0] == "2":
                neutralComment = neutralComment + " | " + comments[1]
            elif comments[0] == "1":
                badComment = badComment + " | " + comments[1]


        L3=Label(f2, text="Neutral").grid(column=0, row=2)
        L5 = Label(f2, text=neutralComment).grid(column=1, row=2)


        L4=Label(f2, text="Bad").grid(column=0, row=3)
        L6 = Label(f2, text=badComment).grid(column=1, row=3)

        L7 = Label(f2, text=goodComment).grid(column=1, row=1)

        B=Button(f2, text="Back to Choose Functionality", command=self.exitReview)
        B.grid(column=0, row=4)

        f2.pack(side=BOTTOM,anchor=E)
        db.commit()
        cursor.close()
        self.Review.withdraw()

    def exitReview(self):
        self.viewReview.destroy()
        self.nueWind.deiconify()

    def ManagerFunctionality(self):

        self.managerWin=Toplevel()
        self.loginWin.withdraw()

        self.managerWin.title("Choose Functionality")

        f=Frame(self.managerWin)
        B=Button(f, text="View Revenue Report", command=self.RevenueReport).grid(row=0, column=0)
        B2=Button(f, text="View Popular Route Report", command=self.PopularRoute).grid(row=1, column=0)

        B3=Button(f, text="Log Out", command=self.ManagerLogOut).grid(row=2, column=0)

        f.pack(side=BOTTOM, anchor=E)

    def RevenueReport(self):
        self.RevenueWindow=Toplevel()
        self.managerWin.withdraw()

        self.RevenueWindow.title("View Revenue Report")

        F=Frame(self.RevenueWindow)
        L=Label(F, text="Month").grid(column=0, row=0)
        L2=Label(F, text="Revenue").grid(column=1, row=0)


        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return
        

        sql = '''SELECT MONTHNAME(A.Departure_Date) AS MONTH, SUM(A.Total_Cost) AS Revenue FROM Reserves AS A NATURAL JOIN Reservation AS B WHERE A.Departure_Date >= DATE_FORMAT(CURDATE( ), '%Y-%m-01') - INTERVAL 3 MONTH AND A.Departure_Date <= DATE_FORMAT(CURDATE( ), '%Y-%m-01') GROUP BY MONTH'''
        cursor = db.cursor()
        cursor.execute(sql)
        fetch = cursor.fetchall()

        L3 = Label(F, text=fetch[1][0]).grid(column=0,row=1)
        L4 = Label(F, text=fetch[0][0]).grid(column=0,row=2)
        L5 = Label(F, text=fetch[2][0]).grid(column=0, row=3)

        L6 = Label(F, text=fetch[1][1]).grid(column=1,row=1)
        L7 = Label(F, text=fetch[0][1]).grid(column=1, row=2)
        L8 = Label(F, text=fetch[2][1]).grid(column=1, row=3)

        B=Button(F, text="Back", command=self.exitRevenue).grid(row=4, column=0)

        F.pack(side=BOTTOM, anchor=E)

        db.commit()
        cursor.close()

    def PopularRoute(self):
        self.PopularWin=Toplevel()
        self.managerWin.withdraw()

        self.PopularWin.title("View Popular Route Report")

        F=Frame(self.PopularWin)

        L=Label(F, text="Month").grid(column=0, row=0)
        L2=Label(F, text="Train Number").grid(column=1, row=0)
        L3=Label(F, text="# of Reservations").grid(column=2, row=0)

        B=Button(F, text="Back", command=self.exitPopRoute).grid(column=0, row=10)


        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return
        

        sql = '''SELECT MONTHNAME(Departure_Date) AS Month, Train_Number, COUNT(Reservation_ID) FROM Reserves NATURAL JOIN Reservation WHERE Departure_Date >= DATE_FORMAT(CURDATE( ), '%Y-%m-01') - INTERVAL 3 MONTH AND Departure_Date <= DATE_FORMAT(CURDATE( ) , '%Y-%m-01') GROUP BY Train_Number ORDER BY Month'''
        cursor = db.cursor()
        cursor.execute(sql)
        fetch = cursor.fetchall()

        L13=Label(F, text=fetch[3][0]).grid(column=0, row=1)
        L14=Label(F, text=fetch[3][1]).grid(column=1, row=1)
        L15 = Label(F, text=fetch[3][2]).grid(column=2,row=1)

        L4=Label(F, text=fetch[0][0]).grid(column=0, row=2)
        L5=Label(F, text=fetch[0][1]).grid(column=1, row=2)
        L6 = Label(F, text=fetch[0][2]).grid(column=2,row=2)

        L8=Label(F, text=fetch[1][1]).grid(column=1, row=4)
        L9 = Label(F, text=fetch[1][2]).grid(column=2,row=4)

        L11=Label(F, text=fetch[2][1]).grid(column=1, row=3)
        L12 = Label(F, text=fetch[2][2]).grid(column=2,row=3)

        L16=Label(F, text=fetch[4][0]).grid(column=0, row=5)
        L17=Label(F, text=fetch[4][1]).grid(column=1, row=5)
        L18 = Label(F, text=fetch[4][2]).grid(column=2,row=5)

        L19=Label(F, text=fetch[5][1]).grid(column=1, row=6)
        L20 = Label(F, text=fetch[5][2]).grid(column=2,row=6)
        
        L21=Label(F, text=fetch[6][1]).grid(column=1, row=7)
        L22 = Label(F, text=fetch[6][2]).grid(column=2,row=7)

        F.pack(side=BOTTOM, anchor=E)

        db.commit()
        cursor.close()

    def exitPopRoute(self):
        self.managerWin.deiconify()
        self.PopularWin.withdraw()

    def exitRevenue(self):
        self.managerWin.deiconify()
        self.RevenueWindow.withdraw()


    def PaymentInfo(self):
        self.PaymentWin=Toplevel()
        self.ResWin.destroy()


        self.PaymentWin.title("Payment Information")

        f2=Frame(self.PaymentWin)

        L=Label(f2, text="Add Card").grid(column=0, row=0)

        L2 = Label(f2, text="Name on Card").grid(column=0, row=1)

        L3 = Label(f2, text="Card Number").grid(column=0, row=2)

        L4 = Label(f2, text="CVV").grid(column=0, row=3)

        L5 = Label(f2, text="Expiration Date").grid(column=0, row=4)


        self.nameOnCard = StringVar()
        self.nameOnCard.set('')
        E1 = Entry(f2, width=10,textvariable=self.nameOnCard).grid(column=1, row=1)

        self.ccNum = StringVar()
        self.ccNum.set('')
        E2 = Entry(f2, width=10,textvariable=self.ccNum).grid(column=1, row=2)

        self.cvvNum = StringVar()
        self.cvvNum.set('')
        E3 = Entry(f2, width=10,textvariable=self.cvvNum).grid(column=1, row=3)

        self.expDate = StringVar()
        self.expDate.set('')
        E4 = Entry(f2, width=10,textvariable = self.expDate).grid(column=1, row=4)

        B = Button(f2, text="Add Card",command = self.AddCard).grid(column=1, row=5)

        L6 = Label(f2, text="Delete Card").grid(column=2, row=0)
        L7 = Label(f2, text="Card Number").grid(column=2, row=1)
        B = Button(f2, text="Delete Card", command=self.deleteCard).grid(column=3, row=5)


        db = self.Connect()
        cursor = db.cursor()
        sql ='''SELECT Card_Number FROM Payment_Info WHERE Username = %s'''

        cursor.execute(sql,self.UserName)
        fetch=cursor.fetchall()
        self.cardNumbers = fetch

        cardNumList=[]
        for nums in fetch:
            last4 = nums[0][-4:]

            cardNumList.append(last4)

        if len(cardNumList) == 0:
            cardNumList.append(" ")

        self.CCstrVar = StringVar(f2)
        self.CCstrVar.set(cardNumList[0]) #set to card number
        X=OptionMenu(f2, self.CCstrVar, *cardNumList) #option menu needs to be credit cards
        X.grid(row=1, column=3)


        f2.pack(side=BOTTOM,anchor=E)
        self.CardNumberList=cardNumList

        db.commit()
        cursor.close()

    def AddCard(self):
        db = self.Connect()
        cursor = db.cursor()
        self.creditcardNum=self.ccNum.get()
        sqlAdd = "INSERT INTO Payment_Info(Card_Number,CVV,Exp_Date,Name_on_Card,Username) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sqlAdd,(self.creditcardNum,self.cvvNum.get(),self.expDate.get(),self.nameOnCard.get(),self.UserName))
        db.commit()
        cursor.close()

        self.MakeReservation2()
        self.PaymentWin.withdraw()


    def deleteCard(self):

        num = self.CCstrVar.get()

        if num == " ":
            messagebox.showerror("you do not have a credit card on file to delete", "you do not have a credit card on file to delete")
            return

        count = 0
        for items in self.cardNumbers:
            if num == self.cardNumbers[count][0][-4:]:
                CCnumber = self.cardNumbers[count][0]
            count = count + 1

        db = self.Connect()
        cursor = db.cursor()
        sql = '''DELETE FROM Payment_Info WHERE Card_Number = %s'''
        cursor.execute(sql, CCnumber)
        db.commit()
        cursor.close()
        messagebox.showerror("your card has been deleted", "your card has been deleted")


    def UpdateReservation(self):
        self.updateResWin = Toplevel()

        self.updateResWin.title("Update Reservation")

        f = Frame(self.updateResWin)

        l = Label(f, text = "Reservation ID: ").grid(column = 0, row = 0)
        b1 = Button(f, text = "Back", command = self.returnToMainFromUpdateRes).grid(column = 0, row = 1)
        b2 = Button(f, text = "Next", command = self.UpdateReservation2).grid(column = 1, row = 1)

        self.updateResNum = StringVar()

        e = Entry(f, textvariable = self.updateResNum).grid(column = 1, row = 0)
        f.pack()


    def returnToMainFromUpdateRes(self):
        self.updateResWin.destroy()
        self.nueWind.deiconify()


    def UpdateReservation2(self):

        self.updateResWin2 = Toplevel()
        self.updateResWin.withdraw()
        self.updateResWin2.title("Update Reservation")

        f = Frame(self.updateResWin2)

        L = Label(f, text="Select").grid(column=0, row=0)
        L2 = Label(f, text="Train\n(Train Number)").grid(column=1, row=0)
        L3 = Label(f, text="Time\n(Duration)").grid(column=2, row=0) #todo
        L4 = Label(f, text="Departs From").grid(column=3, row=0)
        L5 = Label(f, text="Arrives At").grid(column=4, row=0)
        L6 = Label(f, text="Class").grid(column=5, row=0)
        L7 = Label(f, text="Price").grid(column=6, row=0) #todo
        L8 = Label(f, text="# of Baggage").grid(column=7, row=0)
        L9 = Label(f, text="Passenger Name").grid(column=8, row=0)

        db = self.Connect()
        cursor = db.cursor()
        sql = '''Select First_Class from Reserves where Reservation_ID = {}'''
        cursor.execute(sql.format(self.updateResNum.get()))
        isFirstClass = cursor.fetchall()


        sql = '''SELECT D.Train_Number, D.Departure_Date, D.Departure_Time, E.Arrival_Time, D.Departs_From, D.Arrives_At, D.First_Class, D.Total_Cost, D.Number_Of_Baggage, D.Passenger_Name
            FROM (
            SELECT A.Reservation_ID, A.Train_Number, A.Departs_From, A.Arrives_At, A.Departure_Date, C.Departure_Time, C.Arrival_Time, A.First_Class, A.Total_Cost, A.Number_Of_Baggage, A.Passenger_Name
            FROM Reserves AS A, Train_Route AS B, Stops AS C
            WHERE A.Train_Number = B.Train_Number
            AND A.Train_Number = C.Train_Number
            AND A.Reservation_ID = {}
            AND A.Train_Number = B.Train_Number
            AND (
            A.Departs_From = C.Name
            OR A.Arrives_At = C.Name
            )
            ) AS D,
            (
            SELECT A.Reservation_ID, A.Train_Number, A.Departs_From, A.Arrives_At, A.Departure_Date, C.Departure_Time, C.Arrival_Time, A.First_Class, A.Total_Cost, A.Number_Of_Baggage, A.Passenger_Name
            FROM Reserves AS A, Train_Route AS B, Stops AS C
            WHERE A.Train_Number = B.Train_Number
            AND A.Train_Number = C.Train_Number
            AND A.Reservation_ID = {}
            AND A.Train_Number = B.Train_Number
            AND (
            A.Departs_From = C.Name
            OR A.Arrives_At = C.Name
            )
            ) as E
            WHERE D.Departure_Time < E.Arrival_Time and D.Reservation_ID = E.Reservation_ID and D.Train_Number = E.Train_Number and D.Departure_Date > CurDate()'''
        cursor.execute(sql.format(self.updateResNum.get(), self.updateResNum.get()))
        db.commit()
        cursor.close()
        self.updateResTuples = cursor.fetchall()

        if len(self.updateResTuples) == 0:
            messagebox.showerror("Error", "You cannot alter this reservation because either it has already passed or there is no matching Reservation ID")

        #todo add some sort of check to make sure you cant change someone else reservation
        self.resUpdateIndex = IntVar()
        self.resUpdateIndex.set(-1)
        counter = 0

        for i in range(len(self.updateResTuples)):
            counter += 1
            R1 = Radiobutton(f, text='', value = i, variable = self.resUpdateIndex).grid(column = 0, row = 1 + i) #radiobutton
            L11 = Label(f, text=self.updateResTuples[i][0]).grid(column=1, row=1 + i)
            L12 = Label(f, text= str(self.updateResTuples[i][1]) + "\n" + str(self.updateResTuples[i][2]) + '-' + str(self.updateResTuples[i][3]) + '\n('
                    + str(self.updateResTuples[i][3] - self.updateResTuples[i][2]) + ') hours').grid(column=2, row=1 + i)
            L13 = Label(f, text=self.updateResTuples[i][4]).grid(column=3, row=1 + i)
            L14 = Label(f, text=self.updateResTuples[i][5]).grid(column=4, row=1 + i)
            if self.updateResTuples[i][6] == 0:
                L15 = Label(f, text = "2nd").grid(column=5, row=1 + i)
            else:
                L15 = Label(f, text = "1st").grid(column = 5, row = 1 + i)
            L16 = Label(f, text=self.updateResTuples[i][7]).grid(column=6, row=1 + i)
            L17 = Label(f, text=self.updateResTuples[i][8]).grid(column=7, row=1 + i)
            L18 = Label(f, text=self.updateResTuples[i][9]).grid(column=8, row=1 + i)

        L19 = Label(f, text="New Departure Date: ").grid(column=0, row=2 + counter)
        self.dateEntStrVar = StringVar()
        dateEnt = Entry(f, textvariable=self.dateEntStrVar).grid(column=1, row=2 + counter)

        backBut = Button(f, text = "Back", command = self.BackToUpdateReservationFromUpdateReservation2).grid(row = 3 + counter, column = 0)
        nextBut = Button(f, text = "Next", command = self.UpdateReservation3).grid(row = 3 + counter, column = 1)

        f.pack()

    def BackToUpdateReservationFromUpdateReservation2(self):
        self.updateResWin2.destroy()
        self.updateResWin.deiconify()

    def UpdateReservation3(self):
        self.updateResWin3 = Toplevel()
        self.updateResWin2.withdraw()
        self.updateResWin3.title("Update Reservation")

        f = Frame(self.updateResWin3)

        structTime = datetime.strptime(self.dateEntStrVar.get(), "%Y-%m-%d")
        currTime = datetime.now()
        if structTime - currTime < timedelta(hours=24):
            messagebox.showerror("Error", "Cannot change reservation to within 1 day of departure")
            self.BackToUpdateReservationFromUpdateReservation2()

        L = Label(f, text = "Current Train Ticket").grid(row = 1, column = 0)

        L2 = Label(f, text="Train\n(Train Number)").grid(column=1, row=0)
        L3 = Label(f, text="Time\n(Duration)").grid(column=2, row=0)
        L4 = Label(f, text="Departs From").grid(column=3, row=0)
        L5 = Label(f, text="Arrives At").grid(column=4, row=0)
        L6 = Label(f, text="Class").grid(column=5, row=0)
        L7 = Label(f, text="Price").grid(column=6, row=0)
        L8 = Label(f, text="# of Baggage").grid(column=7, row=0)
        L9 = Label(f, text="Passenger Name").grid(column=8, row=0)


        L11 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][0]).grid(column=1, row=1)
        L12 = Label(f, text=str(self.updateResTuples[self.resUpdateIndex.get()][1]) + "\n" + str(self.updateResTuples[self.resUpdateIndex.get()][2]) + '-' + str(
            self.updateResTuples[self.resUpdateIndex.get()][3]) + '\n('
                            + str(self.updateResTuples[self.resUpdateIndex.get()][3] - self.updateResTuples[self.resUpdateIndex.get()][2]) + ') hours').grid(
            column=2, row=1)
        L13 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][4]).grid(column=3, row=1)
        L14 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][5]).grid(column=4, row=1)
        if self.updateResTuples[self.resUpdateIndex.get()][6] == 0:
            L15 = Label(f, text="2nd").grid(column= 5, row=1)
        else:
            L15 = Label(f, text="1st").grid(column=5, row=1)
        L16 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][7]).grid(column=6, row=1)
        L17 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][8]).grid(column=7, row=1)
        L18 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][9]).grid(column=8, row=1)

        L20 = Label(f, text = "Updated Train Ticket").grid(column = 0, row = 2)

        L11 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][0]).grid(column=1, row=2)
        L12 = Label(f, text=str(self.dateEntStrVar.get()) + "\n" + str(
            self.updateResTuples[self.resUpdateIndex.get()][2]) + '-' + str(
            self.updateResTuples[self.resUpdateIndex.get()][3]) + '\n('
                            + str(
            self.updateResTuples[self.resUpdateIndex.get()][3] - self.updateResTuples[self.resUpdateIndex.get()][
                2]) + ') hours').grid(
            column=2, row=2)
        L13 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][4]).grid(column=3, row=2)
        L14 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][5]).grid(column=4, row=2)
        if self.updateResTuples[self.resUpdateIndex.get()][6] == 0:
            L15 = Label(f, text="2nd").grid(column=5, row=2)
        else:
            L15 = Label(f, text="1st").grid(column=5, row=2)
        L16 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][7]).grid(column=6, row=2)
        L17 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][8]).grid(column=7, row=2)
        L18 = Label(f, text=self.updateResTuples[self.resUpdateIndex.get()][9]).grid(column=8, row=2)

        B = Button(f, text = "Back", command = self.BackToUpdateReservation2FromUpdateReservation3).grid(row = 3, column = 1)
        B = Button(f, text = "Submit", command = self.CommitUpdateRes).grid(row = 4, column = 1)

        db = self.Connect()
        cursor = db.cursor()
        sql = '''Select Sum(Total_Cost) from Reserves where Reservation_ID = {}'''
        cursor.execute(sql.format(self.updateResNum.get()))
        newTotalCost = cursor.fetchone()

        L = Label(f, text = "Change Fee: 50").grid(row = 3, column = 0)
        L = Label(f, text = "Updated Total Cost: " + str(newTotalCost[0] + 50)).grid(row = 4, column = 0)

        db.commit()
        cursor.close()

        f.pack()
        
    def BackToUpdateReservation2FromUpdateReservation3(self):
        self.updateResWin3.destroy()
        self.UpdateReservation2()


    def CommitUpdateRes(self):
        db = self.Connect()
        cursor = db.cursor()
        sql = '''Update Reserves Set Total_Cost = (Total_Cost + 50.00), Departure_Date = '{}' Where Reservation_ID = {} and Train_Number = "{}"'''
        
        cursor.execute(sql.format(self.dateEntStrVar.get(), self.updateResNum.get(), self.updateResTuples[self.resUpdateIndex.get()][0]))
        db.commit()
        cursor.close()

        self.updateResWin3.destroy()
        self.updateResWin2.destroy()



    def CancelReservation(self):
        self.cancelResWin = Toplevel()
        self.cancelResWin.title("Cancel Reservation")

        f = Frame(self.cancelResWin)

        l = Label(f, text="Reservation ID: ").grid(column=0, row=0)
        b1 = Button(f, text="Back", command=self.ReturnToMainFromCancelReservation).grid(column=0, row=1)
        b2 = Button(f, text="Search", command=self.CancelReservation2).grid(column=1, row=1)

        self.cancelResNum = StringVar()

        e = Entry(f, textvariable=self.cancelResNum).grid(column=1, row=0)
        f.pack()

    def ReturnToMainFromCancelReservation(self):
        self.cancelResWin.withdraw()
        self.nueWind.deiconify()


    def CancelReservation2(self):
        self.cancelResWin2 = Toplevel()
        self.cancelResWin2.title("Cancel Reservation")

        f = Frame(self.cancelResWin2)


        L2 = Label(f, text="Train\n(Train Number)").grid(column=1, row=0)
        L3 = Label(f, text="Time\n(Duration)").grid(column=2, row=0)  # todo
        L4 = Label(f, text="Departs From").grid(column=3, row=0)
        L5 = Label(f, text="Arrives At").grid(column=4, row=0)
        L6 = Label(f, text="Class").grid(column=5, row=0)
        L7 = Label(f, text="Price").grid(column=6, row=0)  # todo
        L8 = Label(f, text="# of Baggage").grid(column=7, row=0)
        L9 = Label(f, text="Passenger Name").grid(column=8, row=0)

        db = self.Connect()
        cursor = db.cursor()

        sql = '''SELECT D.Train_Number, D.Departure_Date, D.Departure_Time, E.Arrival_Time, D.Departs_From, D.Arrives_At, D.First_Class, D.Total_Cost, D.Number_Of_Baggage, D.Passenger_Name
                FROM (
                SELECT A.Reservation_ID, A.Train_Number, A.Departs_From, A.Arrives_At, A.Departure_Date, C.Departure_Time, C.Arrival_Time, A.First_Class, A.Total_Cost, A.Number_Of_Baggage, A.Passenger_Name
                FROM Reserves AS A, Train_Route AS B, Stops AS C
                WHERE A.Train_Number = B.Train_Number
                AND A.Train_Number = C.Train_Number
                AND A.Reservation_ID = {}
                AND A.Train_Number = B.Train_Number
                AND (
                A.Departs_From = C.Name
                OR A.Arrives_At = C.Name
                )
                ) AS D,
                (
                SELECT A.Reservation_ID, A.Train_Number, A.Departs_From, A.Arrives_At, A.Departure_Date, C.Departure_Time, C.Arrival_Time, A.First_Class, A.Total_Cost, A.Number_Of_Baggage, A.Passenger_Name
                FROM Reserves AS A, Train_Route AS B, Stops AS C
                WHERE A.Train_Number = B.Train_Number
                AND A.Train_Number = C.Train_Number
                AND A.Reservation_ID = {}
                AND A.Train_Number = B.Train_Number
                AND (
                A.Departs_From = C.Name
                OR A.Arrives_At = C.Name
                )
                ) as E
                WHERE D.Departure_Time < E.Arrival_Time and D.Reservation_ID = E.Reservation_ID and D.Train_Number = E.Train_Number and D.Departure_Date > CurDate()'''
        cursor.execute(sql.format(self.cancelResNum.get(), self.cancelResNum.get()))
        self.cancelResTuples = cursor.fetchall()
        if len(self.cancelResTuples) == 0:
            messagebox.showerror("Error", "No trips under this reservation number to cancel")
        counter = 0
        self.resCancelIndex = IntVar()

        for i in range(len(self.cancelResTuples)):
            counter += 1
            L11 = Label(f, text=self.cancelResTuples[i][0]).grid(column=1, row=1 + i)
            L12 = Label(f, text=str(self.cancelResTuples[i][1]) + "\n" + str(self.cancelResTuples[i][2]) + '-' + str(
                self.cancelResTuples[i][3]) + '\n('
                                + str(self.cancelResTuples[i][3] - self.cancelResTuples[i][2]) + ') hours').grid(
                column=2, row=1 + i)
            L13 = Label(f, text=self.cancelResTuples[i][4]).grid(column=3, row=1 + i)
            L14 = Label(f, text=self.cancelResTuples[i][5]).grid(column=4, row=1 + i)
            if self.cancelResTuples[i][6] == 0:
                L15 = Label(f, text="2nd").grid(column=5, row=1 + i)
            else:
                L15 = Label(f, text="1st").grid(column=5, row=1 + i)
            L16 = Label(f, text=self.cancelResTuples[i][7]).grid(column=6, row=1 + i)
            L17 = Label(f, text=self.cancelResTuples[i][8]).grid(column=7, row=1 + i)
            L18 = Label(f, text=self.cancelResTuples[i][9]).grid(column=8, row=1 + i)


        sql = '''Select Sum(Total_Cost) from Reserves where Reservation_ID = %s and Departure_Date > CurDate()'''
        cursor.execute(sql, self.cancelResNum.get())
        self.totCostFromCancel = cursor.fetchone()
        db.commit()
        cursor.close()

        L = Label(f, text = ("Total Cost of Reservation: " + str(self.totCostFromCancel[0]))).grid(row = 2 + counter, column = 1)
        L = Label(f, text = "Date of Cancellation: " + str(datetime.now().date())).grid(row = 3 + counter, column = 1)

        earliestTime = self.cancelResTuples[0][1]

        for i in self.cancelResTuples:
            if i[1] < earliestTime:
                earliestTime = i[1]


        timediff = earliestTime - datetime.now().date()
        timediff = str(timediff)

        oldTimeDiff = timediff
        timediff = ''
        for i in oldTimeDiff:
            if i == ' ':
                break
            else:
                timediff += i

        timediff = int(timediff)

        self.totCostFloat = float(self.totCostFromCancel[0])

        if timediff > 7:
            refundFactor = .8
        elif timediff > 1:
            refundFactor = .5
        else:
            refundFactor = 0
            messagebox.showerror("Error", "cannot cancel less than a day in advance")

        db = self.Connect()
        cursor = db.cursor()
        sql = "Update Reservation Set Is_Cancelled =  '1' Where Reservation_ID = '{}'"
        cursor.execute(sql.format(self.cancelResNum.get()))
        db.commit()
        cursor.close()

        self.refundAmt = refundFactor * self.totCostFloat + 50

        L = Label(f, text = "Amount to be Refunded: " + str(min(int(self.refundAmt), int(self.totCostFromCancel[0])))).grid(row = 4 + counter, column = 1)

        B = Button(f, text = "Submit", command = self.CompleteCancellation).grid(row = 3 + counter, column = 2)
        B = Button(f, text = "Back", command = self.LastGoBackEver).grid(row = 4 + counter, column = 2)

        f.pack()

    def LastGoBackEver(self):
        self.cancelResWin2.destroy()
        self.cancelResWin.deiconify()

    def CompleteCancellation(self):
        index = 0
        resID = self.cancelResNum.get()

        while self.refundAmt > 0 and index < len(self.cancelResTuples):
            
            db = self.Connect()
            cursor = db.cursor()
            sql = "Select Total_Cost from Reserves where Reservation_ID = '{}' and Train_Number = '{}'"
            cursor.execute(sql.format(resID, self.cancelResTuples[index][0]))
            tempCost = int(cursor.fetchone()[0])
            if tempCost - self.refundAmt >= 0:
                sql = "Update Reserves Set Total_Cost = {} Where Reservation_ID = '{}' and Train_Number = '{}'"
                cursor.execute(sql.format((tempCost - self.refundAmt), resID, self.cancelResTuples[index][0]))
            else:
                sql = "Update Reserves Set Total_Cost = 0 Where Reservation_ID = '{}' and Train_Number = '{}'"
                cursor.execute(sql.format(resID, self.cancelResTuples[index][0]))
                self.refundAmt = self.refundAmt - tempCost
            db.commit()
            cursor.close()
            index += 1

            self.cancelResWin2.destroy()
            self.cancelResWin.destroy()

rootWin = Tk()
app = CS4400(rootWin)
rootWin.mainloop()

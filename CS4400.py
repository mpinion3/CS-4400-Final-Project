#data from data file
# use sncf_team3;
from tkinter import *
from tkinter import messagebox
import pymysql
import time
from datetime import *
import calendar

class CS4400:
    def __init__(self,rootWin):
        self.Login(rootWin)
        self.db = pymysql.connect(host = "localhost", user = "root", db = "sncf_team3", passwd = "")

    def Login(self,rootWin):
        self.loginWin=rootWin        
        self.loginWin.title('SNCF Login')
        f2=Frame(self.loginWin)     
        #Username
        userL=Label(f2, text='Email').grid(row=0,column=0,sticky=E) 
        self.Custemail=Entry(f2,width=30)
        self.Custemail.grid(row=0, column=1)
        #password
        passL=Label(f2, text='Password').grid(row=1,column=0,sticky=E) 
        self.CustPassword=Entry(f2,width=30,show="*")
        self.CustPassword.grid(row=1, column=1)

        f2.pack(padx=50,pady=50)  

        f3=Frame(self.loginWin)   

        b1=Button(f3, text='Login',width=10,command=self.CheckLogin)  
        b1.grid(row = 0, column = 0,padx=30)


        b2=Button(f3, text='Register', bd=0, command=self.New_User)  

        b2.grid(row=0,column=2)

        f3.pack(side=BOTTOM,anchor=E)  

    def New_User(self):

        self.loginWin.iconify()

        self.nuWin=Toplevel()
        self.nuWin.title("Register an Account")

        f2=Frame(self.nuWin)

        fname=Label(f2, text='First Name:').grid(row=0,column=0,sticky=W,padx=5)  
        self.NUfname=Entry(f2,width=30)
        self.NUfname.grid(row=0,column=1,pady=2)

        lname=Label(f2, text='Last Name:').grid(row=1,column=0,sticky=W,padx=5) 
        self.NUlname=Entry(f2,width=30)
        self.NUlname.grid(row=1,column=1,pady=2)

        email=Label(f2, text='Email Address:').grid(row=2,column=0,sticky=W,padx=5)  
        self.NUemail=Entry(f2,width=30)
        self.NUemail.grid(row=2,column=1,pady=2)

        passL=Label(f2, text='Password:').grid(row=3,column=0,sticky=W,padx=5)  
        self.NUpassword=Entry(f2,width=30,show="*")
        self.NUpassword.grid(row=3,column=1,pady=2)

        con_passL=Label(f2, text='Confirm Password:').grid(row=4,column=0,sticky=W,padx=5)  
        self.NUconfirm=Entry(f2,width=30,show="*")
        self.NUconfirm.grid(row=4,column=1,pady=2)

        adl1=Label(f2, text='Address Line 1').grid(row=5,column=0,sticky=W,padx=5) 
        self.NUadl1=Entry(f2,width=30)
        self.NUadl1.grid(row=5,column=1,pady=2)

        adl2=Label(f2, text='Address Line 2').grid(row=6,column=0,sticky=W,padx=5)  
        self.NUadl2=Entry(f2,width=30)
        self.NUadl2.grid(row=6,column=1,pady=2)

        city=Label(f2, text='City').grid(row=7,column=0,sticky=W,padx=5)  
        self.NUcity=Entry(f2,width=30)
        self.NUcity.grid(row=7,column=1,pady=2)

        state=Label(f2, text='State').grid(row=8,column=0,sticky=W,padx=5)  
        self.NUstate=Entry(f2,width=30)
        self.NUstate.grid(row=8,column=1,pady=2)

        Zip=Label(f2, text='Zip').grid(row=9,column=0,sticky=W,padx=5)  
        self.NUZip=Entry(f2,width=30)
        self.NUZip.grid(row=9,column=1,pady=2)

        country=Label(f2, text='Country').grid(row=10,column=0,sticky=W,padx=5)  
        self.NUcountry=Entry(f2,width=30)
        self.NUcountry.grid(row=10,column=1,pady=2)

        birthdate=Label(f2, text='Birthdate (YYYY-MM-DD)').grid(row=11,column=0,sticky=W,padx=5)  
        self.NUbirthdate=Entry(f2,width=30)
        self.NUbirthdate.grid(row=11,column=1,pady=2)

        CC =Label(f2, text='Credit Card Number (16 digits)').grid(row=12,column=0,sticky=W,padx=5)  
        self.NUCC=Entry(f2,width=30)
        self.NUCC.grid(row=12,column=1,pady=2)

        CCEXP = Label(f2, text='Credit Card Expiration (YYYY-MM-DD)').grid(row=13,column=0,sticky=W,padx=5)  
        self.NUCCEXP=Entry(f2,width=30)
        self.NUCCEXP.grid(row=13,column=1,pady=2)

        f2.pack(padx=30, pady=20)

        f3=Frame(self.nuWin)     

        b1=Button(f3, text='Create Account',width=10, command=self.RegisterNew)   
        b1.grid(row = 0, column = 0,padx=30,pady=10)
        f3.pack(side=BOTTOM,anchor=E)

    def RegisterNew(self): 
        self.Fname=self.NUfname.get()
        self.Lname=self.NUlname.get()
        self.Email=self.NUemail.get()
        self.Password=self.NUpassword.get()
        self.adl1 = self.NUadl1.get()
        self.adl2 = self.NUadl2.get()
        self.city = self.NUcity.get()
        self.state = self.NUstate.get()
        self.Zip = self.NUZip.get()
        self.country = self.NUcountry.get()
        self.birthdate = self.NUbirthdate.get()
        self.CC = self.NUCC.get()
        self.CCEXP = self.NUCCEXP.get()
        confirm=self.NUconfirm.get()

        if self.Fname =="":
            messagebox.showerror('Input Error', 'Name cannot be blank')
            return
        elif self.Lname =="":
            messagebox.showerror('Input Error' 'Name cannot be blank')
            return    
        elif self.Email=="":            
            messagebox.showerror('Input Error','Must have an Email')      
            return
        elif len(self.Email)>32:      
            messagebox.showerror('Input Error','Your email is too long!')  
            return
        elif self.Password != confirm:          
            messagebox.showerror('Input Error','Passwords do not match')   
            return
        elif self.adl1 == "":
            messagebox.showerror('Input Error', 'Address cannot be blank')
            return
        elif len(self.state) != 2:
            messagebox.showerror('Input Error', 'Enter a 2 character state code')
            return
        elif len(self.Zip) != 5:
            messagebox.showerror('Input Error','Please enter 5 digit zip!') 
            return
        elif self.country =="":
            messagebox.showerror('Input Error', 'Please enter your country')
            return
        elif len(self.birthdate) != 10:
            messagebox.showerror('Input Error', 'Please enter a valid birthday using the format provided') 
            return
        elif len(self.CC) != 16:
            messagebox.showerror('Input Error','You have entered a wrong credit card number!')
            return


        cursor=self.db.cursor()  #creates a cursor


        sql = '''SELECT email FROM User WHERE email = %s'''
        cursor.execute(sql, self.Email)    
        fetch = cursor.fetchall()
        LocalnameList = fetch
        
        if len(LocalnameList)!= 0:   
            messagebox.showerror("Input Error",'You are already registered. Please Login') 
            return
        else:
            sql2 = '''INSERT INTO user (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql2,(self.Email, self.Password, self.Fname, self.Lname))

        sql3 = '''SELECT user_id from user order by user_id DESC LIMIT 1'''
        cursor.execute(sql3)
        fetch2 = cursor.fetchall()
        fetch3 = fetch2[0]
        print(fetch3)

        sql4 = '''INSERT INTO address (line1,line2,city,state,post_code,country) VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql4,(self.adl1, self.adl2, self.city, self.state, self.Zip, self.country))
       
        sql6 = '''SELECT address_id from address order by address_id DESC LIMIT 1'''
        cursor.execute(sql6)
        fetch4 = cursor.fetchall()
        fetch5 = fetch4[0]
        
        sql5 = '''INSERT INTO customer (user_id,address_id,birthdate,credit_card_no,credit_card_expiry) VALUES (%s,%s,%s,%s,%s)'''
        cursor.execute(sql5,(fetch3, fetch5, self.birthdate, self.CC, self.CCEXP))
 
        self.db.commit() 
        cursor.close()  
        self.nuWin.withdraw()
        self.MM()

    def CheckLogin(self):
        self.email=self.Custemail.get()
        self.Password=self.CustPassword.get()

        cursor=self.db.cursor()
        sql = '''SELECT email, password FROM user WHERE email = %s AND password = %s'''
        cursor.execute(sql, (self.email,self.Password))   
        fetch = cursor.fetchall() 
        LocalnameList = fetch
        
        if len(LocalnameList) == 0:
            messagebox.showerror("You have entered in an incorrect username/password combination","Please try again")

        else:
                    
            self.loginWin.withdraw()
            self.MM()
            
        self.db.commit()
        cursor.close()
    
    def MM(self):


        self.nueWind=Toplevel()
        self.nueWind.title("Dashboard")

        f22=Frame(self.nueWind)

        TrainS=Button(f22, text='Search Trip', fg='blue', command=self.TrainSchedule).grid(row=0,column=0,sticky=EW,padx=5)  

        Make=Button(f22, text='Make A Reservation', command=self.bookTrip).grid(row=1,column=0,sticky=EW,padx=5)  


        bp=Button(f22, text='Log Out',width=10, command=self.LogOut)   
        bp.grid(row = 7, column = 1,padx=30,pady=10)
        f22.pack(side=BOTTOM,anchor=E,padx=30, pady=20)

    def TrainSchedule(self):

        self.trainS=Toplevel()
        self.trainS.title("Search Train")

        f=Frame(self.trainS)

        L=Label(f, text='Train Number').grid(row=0,column=0,sticky=E)  
        self.trainNum=Entry(f,width=30)
        self.trainNum.grid(row=0, column=1, sticky = E)

        b=Button(f, text="Enter Train number for information", width=10, command=self.PullTrainSchedule) 
        b.grid(row=2, column = 0, padx=30)

        f.pack(side = BOTTOM, anchor = E, padx=30, pady=20)

    def PullTrainSchedule(self):
        self.trainSchedWin = Toplevel()
        self.trainSchedWin.title("Train Schedule")

        searchTrain = self.trainNum.get()
        cursor = self.db.cursor()  
        sql = '''SELECT arrival_Time, departure_Time, name FROM stop JOIN station using (station_id) WHERE train_id = %s ORDER BY arrival_Time''' #fix query, semantic error. 
        cursor.execute(sql, searchTrain)
        trainschedule = cursor.fetchall()

        if len(trainschedule) == 0:
        	messagebox.showerror("Train does not exist","Please try again")
        	self.trainSchedWin.withdraw()
        	return



        self.db.commit() 
        cursor.close() 


        f=Frame(self.trainSchedWin)


        Number = self.trainNum.get() 

        frameRows = 1



        L=Label(f,text="Train (Train Number)").grid(row=0, column=0, sticky=E)
        L2=Label(f,text="Arrival Time").grid(row=0,column=1,sticky=E)
        L3=Label(f,text="Departure Time").grid(row=0,column=2,sticky=E)
        L4=Label(f,text="Station").grid(row=0,column=3,sticky=E)
        L5=Label(f, text=Number).grid(row=1,column=0, sticky=E)

        print(trainschedule)
        for x in trainschedule:
            LT = Label(f, text=x[0]).grid(row=frameRows, column=1)
            LT2 = Label(f, text=x[1]).grid(row=frameRows, column=2)
            LT3 = Label(f, text=x[2]).grid(row=frameRows, column=3)
            frameRows=frameRows+1



        b=Button(f, text="back", width=10, command = self.trainscheduleback)
        b.grid(column=0, row=(frameRows+1))

        f.pack()


    def trainscheduleback(self):
        self.trainSchedWin.withdraw()
        self.nueWind.deiconify()


    def goToMainFromBookTrain(self):
        self.bookPage.withdraw()
        self.nueWind.deiconify()


    def bookTrip(self):
        cursor = self.db.cursor()
        self.bookPage = Toplevel()
        self.bookPage.title("Book Trip")

        f = Frame(self.bookPage)

        l1 = Label(f, text='Select Stations').grid(row=0, column=0, columnspan = 2, sticky=EW)
        l2 = Label(f, text = 'Embark Station').grid(row = 1, column = 0, sticky = W)
        l3 = Label(f, text = 'Disembark Station').grid(row = 2, column = 0, sticky = W)
        l4 = Label(f, text = 'Birth Date YYYY-MM-DD').grid(row = 3, column = 0, sticky = W)
        l5 = Label(f, text = 'First Name').grid(row = 4, column = 0, sticky = W)
        l6 = Label(f, text = 'Last Name').grid(row = 5, column = 0, sticky = W)


        self.stationList = []
        sql = '''SELECT * FROM Station'''
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

        self.birthdateStrVar = StringVar()
        self.birthdate = Entry(f, width=20, textvariable = self.birthdateStrVar)
        self.birthdate.grid(row=3, column=1, sticky=E)

        self.fnameStrVar = StringVar()
        self.fname = Entry(f, width=20, textvariable = self.fnameStrVar)
        self.fname.grid(row=4, column=1, sticky=E)

        self.lnameStrVar = StringVar()
        self.lname = Entry(f, width=20, textvariable = self.goToMainFromBookTrain)
        self.lname.grid(row=5, column=1, sticky=E)

        b = Button(f, text="Find Trains", width=10, command=self.FindTrains)  # adds Search button
        b.grid(row=6, column=0, padx=30)

        b=Button(f, text="back", width=10, command = self.goToMainFromBookTrain)
        b.grid(row = 7, column = 0,padx = 30)

        f.pack(side=BOTTOM, anchor=E, padx=30, pady=20)

    def FindTrains(self):
        self.bookPage.withdraw()
        self.nueWind.deiconify()
        cursor = self.db.cursor()
        self.FindTrains = Toplevel()
        self.FindTrains.title("Train Options")

        self.Fname=self.fname.get()
        self.Lname=self.lname.get()
        self.embark=self.departsFromDropDown.get()
        self.arrive=self.arrivesAtDropDown.get()
        self.bday=self.birthdate.get()


        print(self.Fname)
        print(self.Lname)
        print(self.bday)
        
        
        #self.departsFromList.append(departsFrom)
        #self.arrivesAtList.append(arrivesAt)
        


        f = Frame(self.selectDeparture)

        l1 = Label(f, text = 'Train \n (Train Number)').grid(row = 0, column = 0)
        l2 = Label(f, text = 'Time \n (Duration)').grid(row = 0, column = 1)
        l3 = Label(f, text = '1st Class Price').grid(row = 0, column = 2)
        l4 = Label(f, text = '2nd Class Price').grid(row = 0, column = 3)

        db = self.Connect()  # runs method for connecting
        if db == None:  # if self.Connect returns nothing then end register new
            return

        cursor = self.db.cursor()  #creates a cursor
    ### SQL Queries messed up*** Need fixing.

        #idd = cursor.execute(''' SELECT (customer_id) FROM customer ORDER BY customer_id DESC LIMIT 1; ''')
        #cursor.execute("insert into trip (customer_id, price) values (%s, 0.1);", (idd))
        #origDist = cursor.execute("SELECT distance from trip_train join stop on trip_train.embark_stop_id = stop.stop_id where trip_id = (select trip_id from trip order by trip_id desc limit 1);")
        #lastDist = cursor.execute("SELECT distance from trip_train join stop on trip_train.disembark_stop_id = stop.stop_id where trip_id = (select trip_id from trip order by trip_id desc limit 1);")
        #priceDist = lastDist - origDist
        #distSum = priceDist
        




    #     f.pack()

    def LogOut(self):

        self.loginWin.deiconify()
        self.nueWind.withdraw()

    def Back(self):
        self.schoolwin.withdraw()
        self.nueWind.deiconify()
def main():
	rootWin = Tk()
	app = CS4400(rootWin)
	rootWin.mainloop()
if __name__ =="__main__":
	main()
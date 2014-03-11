def rmbs_show(self):
    self.clr_update_frame()
 
    # Prepayment Rate
    Label( self.update_frame, text="CPR" ).grid( row = 0, column= 0 )    
    w = Scale( self.update_frame, from_=0.01, to=0.20, resolution = 0.005, orient=HORIZONTAL, variable=self.rmbs_cpr, showvalue = True )
    w.grid(row = 0, column = 1)
 
    # Mortgage Type (1 == Fixed Principal)
    cb_mortgage_type = Checkbutton(self.update_frame,variable=self.rmbs_mortgageType ,text="Fix Principal")
    cb_mortgage_type.grid(row=0, column=2)
 
    # MBS Outstanding Balance
    Label( self.update_frame, text="Outstanding Bal" ).grid( row = 1, column= 0 )
    e = Entry( self.update_frame)
    e.insert(0,"100000")
    e.grid(row = 2, column =0)
 
    # MBS Average Period
    Label( self.update_frame, text="Period").grid(row = 1, column=1 )
    term = Entry(self.update_frame)
    term.insert(0,"360")
    term.grid(row = 2, column=1)
 
    # MBS Average Rate
    Label( self.update_frame, text="Mortgage Rate").grid(row = 1, column=2 )
    mortgage_rate = Entry(self.update_frame)
    mortgage_rate.insert(0,"0.16")
    mortgage_rate.grid(row = 2, column=2)
 
    # MBS Senior Tranche Balance
    Label( self.update_frame, text="Senior Tranche" ).grid( row = 4, column= 0 )
    de = Entry( self.update_frame)
    de.grid(row = 5, column =0)
    de.insert(0,"50000")
 
    # MBS Senior Tranche Rate
    Label( self.update_frame, text="Senior Rate" ).grid( row = 4, column= 1 )
    de_rate = Entry( self.update_frame )
    de_rate.grid(row = 5, column = 1)
    de_rate.insert(0,"0.03") ## senior rate
 
    # MBS Junior Tranche Balance
    Label( self.update_frame, text="Junior Tranche" ).grid( row = 6, column= 0 )
    de1 = Entry( self.update_frame)
    de1.grid(row = 7, column =0)
    de1.insert(0,"10000")
 
    # MBS Junior Tranche Rate
    Label( self.update_frame, text="Junior Rate" ).grid( row = 6, column= 1 )
    de_rate1 = Entry( self.update_frame )
    de_rate1.grid(row = 7, column = 1)
    de_rate1.insert(0,"0.11") ## junior rate
 
    # Equity is Outstanding - Senior - Junior Balances
    Label( self.update_frame, text="Equity" ).grid( row = 8, column= 0 ) 
 
    ## 1 == fixed principal
    def cal_rmbs():
        self.period = int(term.get())
        self.mortgage_cf = []
        #cb_mortgage_type.select()
        # calculate the SMM based on assumed CPR
        smm = 1 - math.pow(( 1 - float(self.rmbs_cpr.get())),1/12.0)
        #print smm
        #print "SMM %f" % smm
        balance = float(e.get())
        #print balance
        period = int(term.get())
        #mortgage_rate = 
 
        r = float(mortgage_rate.get())/12.0
        #print self.rmbs_mortgageType.get()
        if self.rmbs_mortgageType.get() == 1 :
        #fix principal method
            monthly_principal = balance / float(period)
            for i in range(period):
                mcf = 0.0
                mcf += monthly_principal
                mcf += balance * r
                mcf += balance * smm
                if balance >= monthly_principal:
                    balance -= monthly_principal
                else:
                    break
                if balance >= balance * smm:
                    balance -= balance * smm
                else:
                    break
                self.mortgage_cf.append(mcf)
        #fix amount method
        else:
            mthpyt = balance * r * math.pow((1+r),period)/ (math.pow((1+r),period) -1)
            for i in range(period):
                mcf = 0.0
                interest = balance * r
                mcf += mthpyt
                mcf += balance * smm
 
                if balance >= (mthpyt - interest):
                    balance -= mthpyt - interest
                else:
                    break
                if balance >= balance * smm:
                    balance -= balance * smm
                else:
                    break
 
                self.mortgage_cf.append(mcf)
 
        #self.mortgage_cf = x for x in self.mortgage_cf if x > 0
 
        self.senior_cf = []
        self.junior_cf = []
        self.equity_cf = []
        senior_req = float(de.get()) * float(de_rate.get())
        junior_req = float(de1.get()) * float(de_rate1.get())

        ## this is the waterfall
        ## individual cash flows or total cashflows for a period?
        for i in self.mortgage_cf:
            if i <= senior_req:
                # if we have less than the senior requirement then only the senior tranche is paid
                self.senior_cf.append(i)
                self.junior_cf.append(0)
                self.equity_cf.append(0)
            elif i <=  senior_req+junior_req:
                # append the full senior requirement to the tranche
                # and give the remainder to the senior, equity tranche gets nothing
                self.senior_cf.append(senior_req)      
                self.junior_cf.append(i - senior_req)
                self.equity_cf.append(0)
            else:
                # if monthly cashflows are sufficient then all tranches get paid 
                self.senior_cf.append(senior_req)
                self.junior_cf.append(junior_req)
                self.equity_cf.append(i-senior_req-junior_req )
 
        self.rmbs_render()
 
 
def rmbs_render(self):
    #print self.mortgage_cf
    #print self.senior_cf
    #print self.junior_cf
    #print self.equity_cf
 
    plt.cla()
    x = np.arange(0.0, len(self.mortgage_cf), 1)
 
    from pylab import *
 
    plot(x, self.mortgage_cf,color='#ff9999',linewidth=2.0, label='Total MBS Cash Flow')
    plot(x, self.equity_cf,color='#BB1BF5',linewidth=2.0, label='Equity Tranche Cash Flow')
    plot(x, self.junior_cf,color='#2340E8',linewidth=2.0, label='Junior Tranche Cash Flow')
    plot(x, self.senior_cf,color='#1DF0A2',linewidth=2.0, label='Senior Tranche Cash Flow')
 
    legend( ('Total MBS Cash Flow', 'Equity Tranche Cash Flow', 'Junior Tranche Cash Flow','Senior Tranche Cash Flow'), loc='upper right')
    #plt.fill_between(x, self.mortgage_cf,0, 'r')
    plt.grid(True)
    plt.show()


from django.shortcuts import render, resolve_url
import numpy as np
import scipy
import json
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['GET','POST'])
def home(request):
    endpoints = 'hello'
    if request.method == 'POST':
        ce = request.data["ce"]
        pe = request.data["pe"]
        fudi = request.data["fudi"]
        lots = request.data["lots"]

        ce_col = ["Symbol", "Expiry","Date","Strike Price","LTP"]
        pe_col = ["Date","Strike Price",'LTP']

        pe_d = []
        fu_d = []
        fu_u = []

        date_validator = []
        strike_validator = []

        dfce = pd.read_csv(ce,usecols=ce_col)
        dfpe = pd.read_csv(pe,usecols=pe_col)
        dffudi = pd.read_csv(fudi)
        
        dffudi.columns = dffudi.columns.str.replace(' ','')
        
        dffudi = dffudi[["Date","LTP","UnderlyingValue"]]

        for pe in dfpe.iterrows():
            pe_d.append(pe[1]["LTP"])

        for pe in dfpe.iterrows():
            date_validator.append(pe[1]["Date"])

        for pe in dfpe.iterrows():
            strike_validator.append(pe[1]["Strike Price"])


        for du in dffudi.iterrows():
            fu_d.append(du[1]["LTP"])
        
        for du in dffudi.iterrows():
            fu_u.append(du[1]["UnderlyingValue"])

        
        context = {
            "basics":get_expiry(dfce),
            "option_chain":get_optionchain(dfce,pe_d,fu_d,fu_u,lots,date_validator,strike_validator)
        }

        return Response(context)
    

    return Response(endpoints)




def get_optionchain(chain,pe_d,fu_d,fu_u,lots,date_validator,strike_validator):
    options = []
    count = 0
    for ce in chain.iterrows():
        count = count + 1
        d = {
            "id": count ,
            "Symbol":ce[1]["Symbol"],
            "Expiry":ce[1]["Expiry"],
            "Date":ce[1]["Date"],
            "Strikes":ce[1]["Strike Price"],
            "CallLTP":ce[1]["LTP"],
            "PutLTP":None,
            "Lotsize":int(lots),
            "FuturePrice":None,
            "SpotPrice":None,
        }
        options.append(d)
    


    for d in range(len(options)):
        r = [x for x in options if x['Date'] == date_validator[d] and x["Strikes"] == strike_validator[d]]
        
        i = options.index(r[0])
        options[i]["PutLTP"] = pe_d[d]



    x = options[0]["Date"]
    i = 0
    for d in range(len(options)):

        if options[d]["Date"] == x:
            options[d]["FuturePrice"] = fu_d[i]
            options[d]["SpotPrice"] = fu_u[i]


        else:
            i += 1
            options[d]["FuturePrice"] = fu_d[i]
            options[d]["SpotPrice"] = fu_u[i]
            x = options[d]["Date"]
        
        if i == len(fu_d)-1:
           break
    

    return options


    
def get_expiry(ce_data):
    expiries = ce_data["Expiry"]
    all_expiry = []
    symbols = ce_data["Symbol"]
    all_symbol = []

    for expiry in expiries:
        if expiry not in all_expiry:
            all_expiry.append(expiry)
    
    for symbol in symbols:
        if symbol not in all_symbol:
            all_symbol.append(symbol)


    context = {
        "expiry":all_expiry[0],
        "symbol":all_symbol[0]
    }

    return context


@api_view(["POST"])
def payoff(request):
    if request.method == 'POST':
        op_list = request.data["op_list"]


        optionchain = request.data["optionchain"]


    ######################################## creating the x axis ##########################################################

        #taking the objects based on the expiry date as the name of spotprice
       

        #teking all the strikes here
        strikes = []
        for strike in optionchain:
            strikes.append(int(strike["Strikes"]))

        x= np.arange(round(min(strikes),3) - 1000 ,round(max(strikes),3) + 1000,100)

    ############################################ x ends here ######################################################################


        #if there is no expiry date matched 
        if len(optionchain) < 1:
            return Response({'err':'expiry date does not exist'},status=503)
    

        #get the actuall price here

        #hard string to python objects
        python_obj_oplist = json.loads(op_list)
        op_list = python_obj_oplist
        
        t = int(optionchain[0]["Expiry"][:2]) - int(optionchain[0]["Date"][:2])
       

        
        y0=np.zeros_like(x)  

        y_list=[]
        y = 0

        greek = []

        for op in op_list:
            op_type=str.lower(op['op_type'])
            tr_type=str.lower(op['tr_type'])
            lotsize = op['lotsize']
            strike=op['strike']
            op_pr=op['op_pr']
            lots = int(op["contract"])
                
            try:
                contract=op['contract']
            except:
                contract=1

            y_list.append(payoff_calculator(x,op_type,strike,op_pr,tr_type,contract,lotsize))


            greek.append(main(t=t, p=int(op_pr), K=strike, St=int(op["fp"]),type=op_type,lot=lots,ttype=tr_type))

            print(greek)

# t = exipry date - date
#p = put LTP or call LTP based on type c/p
#K = strike price
#st = Future price
#type = c for CE and p for PE
            

        for i in range (len(op_list)):
            try:
                contract=str(op_list[i]['contract'])  
                y+=np.array(y_list[i]) # just plot the combined value only
            except:
                contract='1'
        
        

        return Response({'y':y,'x':x,'greeks':greek})




################### provided scripts here ####################

def payoff_calculator(x, op_type, strike, op_pr, tr_type, n,lotsize):
    y=[]
    
    if n==0:
        for i in range(len(x)):
            y.append(op_pr)
        y=np.array(y)
        if tr_type=='s':
            y=-y
        return y*lotsize

    else:
        if op_type=='c':
            for i in range(len(x)):
                y.append(max((x[i]-strike-op_pr),-op_pr))
        elif op_type=='p':
            for i in range(len(x)):
                y.append(max(strike-x[i]-op_pr,-op_pr))
        else:
            for i in range(len(x)):
                y.append(x[i]-op_pr)


        y=np.array(y)

        if tr_type=='s':
            y=-y

        return y* int(n) * int(lotsize)

        



import numpy as np
from scipy.stats import norm


def black_scholes(t=2, r=10, v=15.28, K=17400, St=17327.40, type='c'):
    """
    Parameters:
    K : Excercise Price
    St: Current Stock Price
    v : Volatility in percentage
    r : Risk free rate in percentage
    t : Time to expiration in days
    type: Type of option 'c' for call 'p' for put
    default: 'c'
    """
    # if type = 'c' or 'C' call option else put option
    try:
        type=type.lower()
        if(type=='c'):
            option_type='call'
        else:
            option_type='put'
    except:
        option_type='put'

    #Check time 
    try:
        #convert time in days to years
        t=t/365
    except:
        raise TypeError("Enter numerical value for time")

    #Check risk free rate 
    try:
        #convert percentage to decimal
        r=r/100
    except:
        raise TypeError("Enter numerical value for risk free rate")
    
    #Check volatility
    try:
        #convert percentage to decimal
        v=v/100
    except:
        raise TypeError("Enter numerical value for volatility")  

    #Check Stock Price
    try:
        St=St+0
    except:
        raise TypeError("Enter numerical value for stock price")
    
    #Check Exercise Price
    try:
        K=K+0
    except:
        raise TypeError("Enter numerical value for Exercise price")    
    
    n1=np.log(St/K)
    n2=(r+(np.power(v,2)/2))*t
    d=v*(np.sqrt(t))

    d1=(n1+n2)/d
    d2=d1-(v*np.sqrt(t))

    if type=='c':
        N_d1=norm.cdf(d1)
        N_d2=norm.cdf(d2)
    else:
        N_d1=norm.cdf(-d1)
        N_d2=norm.cdf(-d2)

    A=(St*N_d1)
    B=(K*N_d2*(np.exp(-r*t)))

    if type=='c':
        val=A-B
        val_int=max(0,St-K)
    else:
        val=B-A
        val_int=max(0,K-St)
    val_time=val-val_int

    # Option values in dictionary
    value={'option value':val, 'intrinsic value':val_int, 'time value':val_time}

    #CALCULATE OPTION GREEKS
    if type=='c':
        delta=N_d1
        theta=(-((St*v*np.exp(-np.power(d1,2)/2))/(np.sqrt(8*np.pi*t)))-(N_d2*r*K*np.exp(-r*t)))/365
        rho=t*K*N_d2*np.exp(-r*t)/100
    else:
        delta=-N_d1
        theta=(-((St*v*np.exp(-np.power(d1,2)/2))/(np.sqrt(8*np.pi*t)))+(N_d2*r*K*np.exp(-r*t)))/365
        rho=-t*K*N_d2*np.exp(-r*t)/100

    gamma=(np.exp(-np.power(d1,2)/2))/(St*v*np.sqrt(2*np.pi*t))
    vega=(St*np.sqrt(t)*np.exp(-np.power(d1,2)/2))/(np.sqrt(2*np.pi)*100)
    
    #Option greeks in Dictionary
    greeks={'delta':delta, 'gamma':gamma, 'theta':theta, 'vega':vega, 'iv':v*100}

    return greeks





def IV(t=2, r=10, v=15.28, K=17400, St=17327.40, type='c'):
    """
    Parameters:
    K : Excercise Price
    St: Current Stock Price
    v : Volatility in percentage
    r : Risk free rate in percentage
    t : Time to expiration in days
    type: Type of option 'c' for call 'p' for put
    default: 'c'
    """
    # if type = 'c' or 'C' call option else put option
    try:
        type=type.lower()
        if(type=='c'):
            option_type='call'
        else:
            option_type='put'
    except:
        option_type='put'

    #Check time 
    try:
        #convert time in days to years
        t=t/365
    except:
        raise TypeError("Enter numerical value for time")

    #Check risk free rate 
    try:
        #convert percentage to decimal
        r=r/100
    except:
        raise TypeError("Enter numerical value for risk free rate")
    
    #Check volatility
    try:
        #convert percentage to decimal
        v=v/100
    except:
        raise TypeError("Enter numerical value for volatility")  

    #Check Stock Price
    try:
        St=St+0
    except:
        raise TypeError("Enter numerical value for stock price")
    
    #Check Exercise Price
    try:
        K=K+0
    except:
        raise TypeError("Enter numerical value for Exercise price")    
    
    n1=np.log(St/K)
    n2=(r+(np.power(v,2)/2))*t
    d=v*(np.sqrt(t))

    d1=(n1+n2)/d
    d2=d1-(v*np.sqrt(t))

    if type=='c':
        N_d1=norm.cdf(d1)
        N_d2=norm.cdf(d2)
    else:
        N_d1=norm.cdf(-d1)
        N_d2=norm.cdf(-d2)

    A=(St*N_d1)
    B=(K*N_d2*(np.exp(-r*t)))

    if type=='c':
        val=A-B
    else:
        val=B-A

    return val


def main(t=2,p=47.34, K=17400, St=17327.40, type='c',lot=1,ttype='b'):
# t = exipry date - date
#p = put LTP or call LTP based on type c/p
#K = strike price
#st = Future price
#type = c for CE and p for PE

    if type=='f':
        grk={'delta':1, 'gamma':0, 'theta':0, 'vega':0, 'iv':0,"type":type,"ttype":ttype,"K":K} 
    
    else:
        target=p
        high=500.0
        low=0.0
        estimate=0.0

            #decimals = len(str(target).split('.')[1])
        for i in range(100):# To avoid infinite loops
            mid = (high + low) / 2
            estimate = IV(t=t, r=0, v=mid, K=K, St=St, type=type)
            if mid < 0.00001:
                mid = 0.00001
            if round(estimate, 2) == target: 
                break
            elif estimate > target: 
                high = mid
            elif estimate < target: 
                low = mid
        grk = black_scholes(t=t, r=0, v=mid, K=K, St=St, type=type)

    if ttype=='s':
        grk['delta']=grk['delta']*lot*-1
        grk['gamma']=grk['gamma']*lot*-1
        grk['theta']=grk['theta']*lot*-1
        grk['vega']=grk['vega']*lot*-1
        grk["type"] = type
        grk["ttype"] = ttype
        grk["K"] = K
    else:
        grk['delta']=grk['delta']*lot
        grk['gamma']=grk['gamma']*lot
        grk['theta']=grk['theta']*lot
        grk['vega']=grk['vega']*lot    
        grk["type"] = type
        grk["ttype"] = ttype
        grk["K"] = K

    return grk



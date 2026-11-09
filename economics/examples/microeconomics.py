"""Original, deterministic teaching models. All units and assumptions are explicit."""
from math import isfinite, sqrt, log


def finite(**values):
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"{name} must be a finite real number")


def ppf(x, x_max=100, y_max=80):
    """Bowed-out production frontier. Endpoint slope is infinite, not zero."""
    finite(x=x, x_max=x_max, y_max=y_max)
    if x_max <= 0 or y_max <= 0 or not 0 <= x <= x_max: raise ValueError("Invalid PPF domain")
    y = y_max * sqrt(max(0, 1-(x/x_max)**2))
    marginal_cost = None if x == x_max else y_max*x/(x_max*x_max*sqrt(1-(x/x_max)**2))
    return {"x":x,"y":y,"marginal_y_per_x":marginal_cost}


def market(a=100, b=1, c=20, d=1, tax=0):
    """Inverse demand a-bQ and supply c+dQ. Constant per-unit tax, interior or no trade."""
    finite(a=a,b=b,c=c,d=d,tax=tax)
    if a <= c or b <= 0 or d <= 0 or tax < 0: raise ValueError("Require a>c, b,d>0, tax>=0")
    q0 = (a-c)/(b+d)
    q = max(0,(a-c-tax)/(b+d))
    buyer, seller = (a-b*q,a-b*q-tax) if q else (None,None)
    cs, ps, revenue = .5*b*q*q, .5*d*q*q, tax*q
    total = cs+ps+revenue
    return {"q":q,"buyer_price":buyer,"seller_price":seller,"cs":cs,"ps":ps,
            "revenue":revenue,"total_surplus":total,"dwl":.5*(a-c)*q0-total,
            "buyer_tax_share":b/(b+d),"seller_tax_share":d/(b+d)}


def price_control(price, kind="ceiling", a=100,b=1,c=20,d=1):
    """Efficient rationing assumption for surplus; rationing itself is not modeled."""
    finite(price=price)
    base = market(a,b,c,d)
    if price < 0 or kind not in {"ceiling","floor"}: raise ValueError("Invalid price control")
    equilibrium=base["buyer_price"]
    binding = price < equilibrium if kind == "ceiling" else price > equilibrium
    if not binding: return {**base,"binding":False,"shortage":0,"excess_supply":0}
    qd,qs = max(0,(a-price)/b),max(0,(price-c)/d)
    q=min(qd,qs)
    cs=(a-price)*q-.5*b*q*q
    ps=(price-c)*q-.5*d*q*q
    return {"binding":True,"q":q,"cs":cs,"ps":ps,"shortage":max(0,qd-qs),
            "excess_supply":max(0,qs-qd),"dwl":base["total_surplus"]-cs-ps}


def midpoint_elasticity(q1,q2,p1,p2):
    finite(q1=q1,q2=q2,p1=p1,p2=p2)
    if min(q1,q2,p1,p2)<0 or q1+q2<=0 or p1+p2<=0 or p1==p2: raise ValueError("Undefined midpoint elasticity")
    return ((q2-q1)/((q1+q2)/2))/((p2-p1)/((p1+p2)/2))


def consumer(income=120,px=2,py=3,alpha=.5):
    finite(income=income,px=px,py=py,alpha=alpha)
    if income<0 or min(px,py)<=0 or not 0<alpha<1: raise ValueError("Interior Cobb-Douglas requires positive prices and 0<alpha<1")
    x,y=alpha*income/px,(1-alpha)*income/py
    return {"x":x,"y":y,"utility":x**alpha*y**(1-alpha),"expenditure":px*x+py*y}


def hicks_decomposition(income=120,px_old=2,px_new=3,py=3,alpha=.5):
    old,new=consumer(income,px_old,py,alpha),consumer(income,px_new,py,alpha)
    compensated_income=old["utility"]/((alpha/px_new)**alpha*((1-alpha)/py)**(1-alpha))
    compensated=consumer(compensated_income,px_new,py,alpha)
    return {"old_x":old["x"],"new_x":new["x"],"compensated_x":compensated["x"],
            "substitution":compensated["x"]-old["x"],"income_effect":new["x"]-compensated["x"],
            "total":new["x"]-old["x"],"compensated_income":compensated_income}


def leisure(wage=10,time=16,nonlabor=0,alpha=.6):
    finite(wage=wage,time=time,nonlabor=nonlabor,alpha=alpha)
    if wage<=0 or time<=0 or nonlabor<0 or not 0<alpha<1: raise ValueError("Invalid labor-leisure parameters")
    rest=min(time,(1-alpha)*(wage*time+nonlabor)/wage)
    return {"leisure":rest,"hours":time-rest,"consumption":wage*(time-rest)+nonlabor}


def intertemporal(y1=100,y2=110,rate=.05,alpha=.5):
    finite(y1=y1,y2=y2,rate=rate,alpha=alpha)
    if min(y1,y2)<0 or rate<=-1 or not 0<alpha<1: raise ValueError("Invalid two-period budget")
    wealth=y1+y2/(1+rate)
    c1=alpha*wealth
    c2=(1-alpha)*wealth*(1+rate)
    return {"c1":c1,"c2":c2,"saving":y1-c1,"present_value":wealth}


def firm(price=50,fixed=100,c=10,d=2):
    finite(price=price,fixed=fixed,c=c,d=d)
    if min(price,fixed,c)<0 or d<=0: raise ValueError("Invalid cost parameters")
    q=max(0,(price-c)/d)
    variable=c*q+.5*d*q*q
    return {"q":q,"revenue":price*q,"variable_cost":variable,"fixed_cost":fixed,
            "profit":price*q-variable-fixed,"producer_surplus":price*q-variable,
            "mc":c+d*q,"min_atc_quantity":sqrt(2*fixed/d) if fixed else 0,
            "shutdown":price<=c}


def monopoly(a=100,b=1,c=20,d=0,fixed=0):
    finite(a=a,b=b,c=c,d=d,fixed=fixed)
    if a<=c or b<=0 or d<0 or fixed<0: raise ValueError("Invalid monopoly model")
    q=(a-c)/(2*b+d); p=a-b*q
    qc=(a-c)/(b+d)
    cs=.5*b*q*q; ps=(p-c)*q-.5*d*q*q
    efficient=(a-c)*qc-.5*(b+d)*qc*qc
    return {"q":q,"price":p,"mc":c+d*q,"profit":ps-fixed,"cs":cs,"ps":ps,
            "competitive_q":qc,"dwl":efficient-cs-ps,"mr":a-2*b*q}


def cournot(n=2,a=100,b=1,c=20):
    finite(a=a,b=b,c=c)
    if type(n) is not int or n<1 or b<=0 or a<=c: raise ValueError("Invalid Cournot model")
    each=(a-c)/(b*(n+1)); q=n*each
    return {"n":n,"each_q":each,"total_q":q,"price":a-b*q,"each_profit":b*each*each}


def game(a=((3,0),(5,1)),b=((3,5),(0,1))):
    """Two-player 2x2 normal form. Weak best responses keep all tied pure equilibria."""
    if any(len(matrix)!=2 or any(len(row)!=2 for row in matrix) for matrix in (a,b)): raise ValueError("Require 2x2 payoffs")
    for matrix in (a,b):
        for row in matrix:
            for value in row: finite(payoff=value)
    pure=[(i,j) for i in range(2) for j in range(2)
          if a[i][j]>=a[1-i][j] and b[i][j]>=b[i][1-j]]
    den_q=a[0][0]-a[0][1]-a[1][0]+a[1][1]
    den_p=b[0][0]-b[0][1]-b[1][0]+b[1][1]
    mixed=None
    if den_q and den_p:
        q=(a[1][1]-a[0][1])/den_q
        p=(b[1][1]-b[1][0])/den_p
        if 0<p<1 and 0<q<1: mixed={"row0_probability":p,"column0_probability":q}
    return {"pure":pure,"interior_mixed":mixed}


def externality(a=100,b=1,c=20,d=1,damage=1):
    finite(damage=damage)
    if damage<0: raise ValueError("Damage slope must be nonnegative")
    base=market(a,b,c,d)
    qm=base["q"]; qo=(a-c)/(b+d+damage)
    welfare=lambda q:(a-c)*q-.5*(b+d+damage)*q*q
    return {"market_q":qm,"optimal_q":qo,"pigou_tax":damage*qo,
            "market_social_welfare":welfare(qm),"optimal_social_welfare":welfare(qo),
            "externality_loss":welfare(qo)-welfare(qm)}


def abatement(target=12,costs=(1,3),capacities=(10,15)):
    finite(target=target)
    if len(costs)!=len(capacities) or not costs: raise ValueError("Costs and capacities must align")
    for c,cap in zip(costs,capacities):
        finite(cost=c,capacity=cap)
        if c<=0 or cap<0: raise ValueError("Require positive MAC slopes and nonnegative capacity")
    if not 0<=target<=sum(capacities): raise ValueError("Infeasible abatement target")
    low,high=0,max(c*cap for c,cap in zip(costs,capacities))
    for _ in range(100):
        price=(low+high)/2
        if sum(min(cap,price/c) for c,cap in zip(costs,capacities))<target: low=price
        else: high=price
    price=(low+high)/2
    amounts=[min(cap,price/c) for c,cap in zip(costs,capacities)]
    return {"amounts":amounts,"total_cost":sum(.5*c*z*z for c,z in zip(costs,amounts)),"marginal_price":price}


def insurance(wealth=100,loss=40,probability=.2,premium=None):
    finite(wealth=wealth,loss=loss,probability=probability)
    if wealth<=0 or not 0<=loss<wealth or not 0<=probability<=1: raise ValueError("Log utility requires positive wealth in every state")
    premium=probability*loss if premium is None else premium
    finite(premium=premium)
    if not 0<=premium<wealth: raise ValueError("Invalid insurance premium")
    expected=(1-probability)*log(wealth)+probability*log(wealth-loss)
    return {"fair_premium":probability*loss,"expected_utility_uninsured":expected,
            "utility_insured":log(wealth-premium),"prefer_insurance":log(wealth-premium)>=expected}


def distribution(incomes=(10,20,30,40),poverty_line=25):
    values=sorted(incomes)
    if not values: raise ValueError("Empty population")
    finite(poverty_line=poverty_line)
    for value in values:
        finite(income=value)
        if value<0: raise ValueError("This Gini fixture requires nonnegative income")
    if poverty_line<=0: raise ValueError("Positive poverty line required")
    n,total=len(values),sum(values)
    gini=0 if total==0 else 2*sum((i+1)*v for i,v in enumerate(values))/(n*total)-(n+1)/n
    gaps=[max(0,(poverty_line-v)/poverty_line) for v in values]
    return {"gini":gini,"headcount":sum(v<poverty_line for v in values)/n,"poverty_gap":sum(gaps)/n}


def trade(labor=120,ax=1,ay=2,bx=3,by=1,price=1,export_x=30):
    finite(labor=labor,ax=ax,ay=ay,bx=bx,by=by,price=price,export_x=export_x)
    if min(labor,ax,ay,bx,by,price)<=0 or export_x<0: raise ValueError("Invalid trade parameters")
    if not ax/ay<price<bx/by: raise ValueError("World price must lie between opportunity costs; A exports X")
    produced_x,produced_y=labor/ax,labor/by
    imported_y=price*export_x
    if export_x>produced_x or imported_y>produced_y: raise ValueError("Trade exceeds production")
    autarky_a=(labor/(2*ax),labor/(2*ay)); autarky_b=(labor/(2*bx),labor/(2*by))
    after_a=(produced_x-export_x,imported_y); after_b=(export_x,produced_y-imported_y)
    utility=lambda bundle:sqrt(bundle[0]*bundle[1])
    return {"a_opportunity_cost":ax/ay,"b_opportunity_cost":bx/by,"a_consumption":after_a,"b_consumption":after_b,
            "a_utility_gain":utility(after_a)-utility(autarky_a),"b_utility_gain":utility(after_b)-utility(autarky_b)}


def tariff(world_price=40,tariff_rate=10,a=100,b=1,c=20,d=1):
    """Small importing economy, specific tariff. No terms-of-trade improvement."""
    finite(world_price=world_price,tariff_rate=tariff_rate)
    base=market(a,b,c,d)
    if not c<=world_price<base["buyer_price"] or tariff_rate<0: raise ValueError("Require an importing economy with interior domestic supply")
    def outcome(price,t):
        qd,qs=(a-price)/b,(price-c)/d
        imports=max(0,qd-qs)
        cs,ps=.5*b*qd*qd,.5*d*qs*qs
        return {"price":price,"demand":qd,"supply":qs,"imports":imports,"revenue":t*imports,"welfare":cs+ps+t*imports}
    free=outcome(world_price,0)
    after=outcome(min(world_price+tariff_rate,base["buyer_price"]),tariff_rate)
    return {**after,"dwl":free["welfare"]-after["welfare"],"free_trade_welfare":free["welfare"]}

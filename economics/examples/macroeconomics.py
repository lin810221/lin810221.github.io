"""Accounting identities and explicitly simplified macroeconomic models."""
from math import log, isfinite
from microeconomics import finite


def expenditure_gdp(consumption,investment,government,exports,imports):
    finite(consumption=consumption,investment=investment,government=government,exports=exports,imports=imports)
    if min(consumption,government,exports,imports)<0: raise ValueError("Negative inventories may enter investment; other fixture components are nonnegative")
    return consumption+investment+government+exports-imports


def price_indexes(p0,q0,pt,qt):
    if not p0 or len({len(p0),len(q0),len(pt),len(qt)})!=1: raise ValueError("Aligned nonempty baskets required")
    for prices in (p0,pt):
        for value in prices:
            finite(price=value)
            if value<=0: raise ValueError("Positive prices required")
    for quantities in (q0,qt):
        for value in quantities:
            finite(quantity=value)
            if value<0: raise ValueError("Nonnegative quantities required")
    base=sum(p*q for p,q in zip(p0,q0)); real=sum(p*q for p,q in zip(p0,qt))
    nominal=sum(p*q for p,q in zip(pt,qt))
    if min(base,real)<=0: raise ValueError("Positive base basket and current production required")
    return {"nominal":nominal,"fixed_base_real":real,"cpi_laspeyres":100*sum(p*q for p,q in zip(pt,q0))/base,
            "gdp_deflator_fixed_base":100*nominal/real,"base_nominal":base}


def percent_change(old,new):
    finite(old=old,new=new)
    if old<=0: raise ValueError("Positive base value required")
    return 100*(new/old-1)


def labor(employed,unemployed,working_age):
    finite(employed=employed,unemployed=unemployed,working_age=working_age)
    lf=employed+unemployed
    if min(employed,unemployed)<0 or working_age<=0 or lf<=0 or lf>working_age: raise ValueError("Invalid population accounting")
    return {"labor_force":lf,"not_in_labor_force":working_age-lf,"unemployment_rate":unemployed/lf,
            "participation_rate":lf/working_age,"employment_population":employed/working_age}


def growth(initial=100,final=150,years=10):
    finite(initial=initial,final=final,years=years)
    if min(initial,final,years)<=0: raise ValueError("Positive levels and duration required")
    rate=(final/initial)**(1/years)-1
    return {"cagr":rate,"doubling_years":log(2)/log(1+rate) if rate>0 else None}


def solow(s=.2,alpha=.3,delta=.05,n=.01,g=.02,k0=1,periods=30,A=1):
    finite(s=s,alpha=alpha,delta=delta,n=n,g=g,k0=k0,A=A)
    if not 0<s<1 or not 0<alpha<1 or not 0<=delta<=1 or min(n,g)<0 or min(k0,A)<=0 or type(periods) is not int or not 0<=periods<=10000:
        raise ValueError("Invalid discrete Solow parameters")
    replacement=delta+n+g+n*g
    if replacement<=0: raise ValueError("Positive effective capital dilution required for a finite steady state")
    kstar=(s*A/replacement)**(1/(1-alpha))
    kgold=(alpha*A/replacement)**(1/(1-alpha))
    path=[]; k=k0
    for t in range(periods+1):
        y=A*k**alpha
        path.append({"t":t,"k":k,"y":y,"consumption":(1-s)*y})
        k=((1-delta)*k+s*y)/((1+n)*(1+g))
    return {"path":path,"steady_k":kstar,"golden_rule_k":kgold,"replacement_rate":replacement,
            "steady_consumption":(1-s)*A*kstar**alpha}


def growth_accounting(y0,y1,k0,k1,l0,l1,alpha=.3):
    finite(y0=y0,y1=y1,k0=k0,k1=k1,l0=l0,l1=l1,alpha=alpha)
    if min(y0,y1,k0,k1,l0,l1)<=0 or not 0<alpha<1: raise ValueError("Positive levels required")
    output,capital,labor_component=log(y1/y0),alpha*log(k1/k0),(1-alpha)*log(l1/l0)
    return {"log_output_growth":output,"capital_contribution":capital,"labor_contribution":labor_component,
            "residual_tfp":output-capital-labor_component}


def fisher(nominal=.05,inflation=.02):
    finite(nominal=nominal,inflation=inflation)
    if min(nominal,inflation)<=-1: raise ValueError("Gross rates must be positive")
    return {"real_exact":(1+nominal)/(1+inflation)-1,"real_approx":nominal-inflation}


def present_value(cashflows=(-100,40,40,40),rate=.05):
    finite(rate=rate)
    if rate<=-1 or not cashflows: raise ValueError("Invalid discounting model")
    for cash in cashflows: finite(cash=cash)
    return sum(cash/(1+rate)**t for t,cash in enumerate(cashflows))


def bond(face=100,coupon_rate=.04,yield_rate=.05,years=5):
    finite(face=face,coupon_rate=coupon_rate,yield_rate=yield_rate)
    if face<=0 or coupon_rate<0 or yield_rate<=-1 or type(years) is not int or not 1<=years<=200: raise ValueError("Invalid annual fixed-coupon bond")
    flows=[face*coupon_rate+(face if t==years else 0) for t in range(1,years+1)]
    pv=[cash/(1+yield_rate)**t for t,cash in enumerate(flows,1)]
    price=sum(pv)
    return {"price":price,"macaulay_duration":sum(t*v for t,v in enumerate(pv,1))/price,
            "modified_duration":sum(t*v for t,v in enumerate(pv,1))/price/(1+yield_rate)}


def bank_loan(reserves=20,loans=60,bonds=20,deposits=80,equity=20,new_loan=10):
    finite(reserves=reserves,loans=loans,bonds=bonds,deposits=deposits,equity=equity,new_loan=new_loan)
    if min(reserves,loans,bonds,deposits,equity,new_loan)<0 or abs(reserves+loans+bonds-deposits-equity)>1e-8:
        raise ValueError("Opening bank balance sheet must balance")
    return {"assets":{"reserves":reserves,"loans":loans+new_loan,"bonds":bonds},
            "liabilities":{"deposits":deposits+new_loan},"equity":equity,
            "loans_risk_weight_100pct_capital_ratio":equity/(loans+new_loan) if loans+new_loan else None}


def multiplier(c=.75,t=.2,m=.1,C0=20,T0=0,I=30,G=40,X=20):
    finite(c=c,t=t,m=m,C0=C0,T0=T0,I=I,G=G,X=X)
    if not 0<=c<1 or not 0<=t<1 or m<0 or min(C0,I,G,X)<0: raise ValueError("Invalid Keynesian-cross fixture")
    denominator=1-c*(1-t)+m
    autonomous=C0-c*T0+I+G+X
    if autonomous<0: raise ValueError("This linear fixture requires nonnegative autonomous demand")
    y=autonomous/denominator
    return {"output":y,"spending_multiplier":1/denominator,"lump_sum_tax_multiplier":-c/denominator,
            "consumption":C0+c*((1-t)*y-T0),"imports":m*y,"taxes":T0+t*y}


def ad_as(A=200,B=1,C=20,D=1):
    finite(A=A,B=B,C=C,D=D)
    if min(B,D)<=0: raise ValueError("Positive slopes required")
    price=(A-C)/(B+D); y=A-B*price
    if min(price,y)<0: raise ValueError("Outside nonnegative model domain")
    return {"price_level":price,"output":y}


def is_mp_pc(a=0,b=1,phi=1,kappa=.5,expected_inflation=2,target=2,natural_real=1,cost_shock=0,policy_shock=0):
    """Static IS-MP-PC. Rates/gap in percentage points; r is ex-ante real, i ~= r + pi_e."""
    finite(a=a,b=b,phi=phi,kappa=kappa,expected_inflation=expected_inflation,target=target,natural_real=natural_real,cost_shock=cost_shock,policy_shock=policy_shock)
    if b<=0 or kappa<=0 or phi<0: raise ValueError("Invalid static policy model")
    y=(a-b*(phi*(expected_inflation-target+cost_shock)+policy_shock))/(1+b*phi*kappa)
    inflation=expected_inflation+kappa*y+cost_shock
    real=natural_real+phi*(inflation-target)+policy_shock
    return {"output_gap_pp":y,"inflation_percent":inflation,"real_rate_percent":real,
            "nominal_rate_percent":real+expected_inflation}


def debt_path(initial=.6,nominal_interest=.04,nominal_growth=.03,primary_surplus=.01,periods=20):
    """Net debt / GDP. Primary surplus is a share of current GDP; no stock-flow adjustments."""
    finite(initial=initial,nominal_interest=nominal_interest,nominal_growth=nominal_growth,primary_surplus=primary_surplus)
    if min(nominal_interest,nominal_growth)<=-1 or type(periods) is not int or not 0<=periods<=10000: raise ValueError("Invalid net-debt path")
    factor=(1+nominal_interest)/(1+nominal_growth)
    rows=[{"t":0,"net_debt_ratio":initial}]; ratio=initial
    for t in range(1,periods+1):
        ratio=factor*ratio-primary_surplus
        rows.append({"t":t,"net_debt_ratio":ratio})
    return {"rows":rows,"stabilizing_primary_surplus":(factor-1)*initial}


def exchange(spot=32,forward=None,domestic_rate=.03,foreign_rate=.02,foreign_price=100,domestic_price=3200):
    finite(spot=spot,domestic_rate=domestic_rate,foreign_rate=foreign_rate,foreign_price=foreign_price,domestic_price=domestic_price)
    if min(spot,foreign_price,domestic_price)<=0 or min(domestic_rate,foreign_rate)<=-1: raise ValueError("Invalid currency quotation")
    fair_forward=spot*(1+domestic_rate)/(1+foreign_rate)
    if forward is not None: finite(forward=forward)
    if forward is not None and forward<=0: raise ValueError("Positive forward quote required")
    return {"quotation":"domestic currency per foreign currency","real_exchange_level":spot*foreign_price/domestic_price,
            "covered_parity_forward":fair_forward,"given_forward":forward}


def balance_of_payments(current=-20,capital=0,financial=-18):
    """FA = net acquisition of assets - net incurrence of liabilities, including reserves."""
    finite(current=current,capital=capital,financial=financial)
    discrepancy=financial-current-capital
    return {"current":current,"capital":capital,"financial_assets_minus_liabilities":financial,
            "statistical_discrepancy":discrepancy,"identity_residual":current+capital-financial+discrepancy}

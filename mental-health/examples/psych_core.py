"""Original educational arithmetic and fictional cases, not psychological assessment."""
from math import isfinite,sqrt
from statistics import mean,median,stdev
import re

def finite(**values):
    for key,value in values.items():
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value):raise ValueError(f'{key}: finite numeric input required')

def nonnegative(**values):
    finite(**values)
    if any(v<0 for v in values.values()):raise ValueError('Nonnegative input required')

def positive(**values):
    nonnegative(**values)
    if any(v==0 for v in values.values()):raise ValueError('Positive denominator required')

def count(**values):
    nonnegative(**values)
    if any(type(v) is not int for v in values.values()):raise ValueError('Whole counts required')

def probability(**values):
    nonnegative(**values)
    if any(v>1 for v in values.values()):raise ValueError('Probability 0..1 required')

def diary_summary(values):
    """Original 0..10 diary observations; ordinal numeric summaries are descriptive only."""
    values=list(values)
    for value in values:
        if value is not None:
            nonnegative(value=value)
            if value>10:raise ValueError('Original diary uses 0..10, not a validated clinical scale')
    known=[v for v in values if v is not None]
    return {'scheduled':len(values),'observed':len(known),'missing':len(values)-len(known),
            'available_mean':mean(known) if known else None,'median':median(known) if known else None,
            'complete_mean':mean(known) if known and len(known)==len(values) else None,
            'scope':'Descriptive original ordinal diary; not diagnosis, severity bands, risk prediction or a reason to delay help'}

def rolling(values,window=3):
    count(window=window)
    if window==0:raise ValueError('Window must be positive')
    diary_summary(values)
    return [mean(values[i-window+1:i+1]) if i+1>=window and all(v is not None for v in values[i-window+1:i+1]) else None for i in range(len(values))]

def opportunity(values):
    if any(v is not None and type(v) is not bool for v in values):raise ValueError('True, False or unknown required')
    known=[v for v in values if v is not None];acted=sum(known)
    return {'scheduled':len(values),'observed':len(known),'acted':acted,
            'available_fraction':acted/len(known) if known else None,
            'complete_fraction':acted/len(values) if values and len(known)==len(values) else None,
            'scope':'A recorded action proportion, not motivation, moral worth or treatment success'}

def minutes_total(values):
    values=list(values)
    for v in values:
        if v is not None:nonnegative(minutes=v)
    known=[v for v in values if v is not None]
    return {'known_subtotal':sum(known),'complete_total':sum(known) if len(known)==len(values) else None,'missing':len(values)-len(known)}

def task_switch(blocks=6,minutes_each=20,assumed_switch_seconds=30):
    count(blocks=blocks);nonnegative(minutes_each=minutes_each,assumed_switch_seconds=assumed_switch_seconds)
    if blocks<1:raise ValueError('At least one block required')
    seconds=blocks*minutes_each*60;overhead=(blocks-1)*assumed_switch_seconds
    return {'working_seconds':seconds,'switches':blocks-1,'assumed_overhead_seconds':overhead,'total_seconds':seconds+overhead,
            'scope':'Explicit hypothetical switch cost; not a universal cognitive constant or productivity promise'}

def clock_minute(value):
    if not isinstance(value,str) or not re.fullmatch(r'(?:[01][0-9]|2[0-3]):[0-5][0-9]',value):raise ValueError('24-hour HH:MM required')
    h,m=map(int,value.split(':'));return h*60+m

def time_window(start='23:00',end='07:00',next_day=True):
    if type(next_day) is not bool:raise ValueError('Day boundary must be explicit')
    duration=clock_minute(end)-clock_minute(start)+(1440 if next_day else 0)
    if not 0<=duration<=1440:raise ValueError('This window is limited to 0..24 hours; verify day boundary')
    return {'minutes':duration,'hours':duration/60,'scope':'Time-window arithmetic, not actual sleep time, sleep need or CBT-I sleep restriction'}

def breath_cycle(inhale=4,exhale=6,cycles=3):
    positive(inhale=inhale,exhale=exhale);count(cycles=cycles)
    if cycles<1:raise ValueError('Positive cycle count required')
    duration=inhale+exhale
    return {'cycle_seconds':duration,'cycles':cycles,'total_seconds':cycles*duration,'cycles_per_minute':60/duration,
            'scope':'Optional comfortable timing illustration without holds; not HRV, cortisol, symptom prediction or a required target'}

def work_ledger(available=240,tasks=(90,60,None),overhead=30):
    nonnegative(available=available,overhead=overhead);total=minutes_total(tasks)
    complete=total['complete_total'];need=None if complete is None else complete+overhead
    return {'available_minutes':available,'known_task_minutes':total['known_subtotal'],'missing_tasks':total['missing'],
            'complete_required_minutes':need,'difference_minutes':None if need is None else available-need,
            'scope':'Planned time ledger, not burnout diagnosis, worker ranking or a physiological capacity estimate'}

def recovery_analogy(load=10,retention=.75,steps=28):
    nonnegative(load=load);probability(retention=retention);count(steps=steps)
    if not 1<=steps<=200:raise ValueError('1..200 illustrative steps required')
    state=0;rows=[]
    for i in range(steps):
        pulse=load if i in (1,5,12) else 0;state=retention*state+pulse;rows.append({'step':i+1,'input':pulse,'state':state})
    return {'rows':rows,'scope':'Uncalibrated accumulation/decay analogy with arbitrary units; not human stress, hormones, recovery or resilience prediction'}

def paired_association(xs,ys):
    if len(xs)!=len(ys):raise ValueError('Paired arrays must have equal lengths')
    for v in [*xs,*ys]:
        if v is not None:finite(value=v)
    pairs=[(x,y) for x,y in zip(xs,ys) if x is not None and y is not None]
    if len(pairs)<2:return {'paired_n':len(pairs),'r':None,'scope':'Descriptive association only, not causality'}
    mx=mean(x for x,y in pairs);my=mean(y for x,y in pairs)
    xx=sum((x-mx)**2 for x,y in pairs);yy=sum((y-my)**2 for x,y in pairs)
    r=sum((x-mx)*(y-my) for x,y in pairs)/sqrt(xx*yy) if xx and yy else None
    return {'paired_n':len(pairs),'r':r,'scope':'Pairwise available fictional observations; serial dependence and confounding remain, no causal interpretation'}

def screening(population=10000,prevalence=.05,sensitivity=.8,specificity=.9):
    count(population=population);positive(population=population);probability(prevalence=prevalence,sensitivity=sensitivity,specificity=specificity)
    affected=population*prevalence;other=population-affected;tp=affected*sensitivity;fn=affected-tp;tn=other*specificity;fp=other-tn
    return {'tp':tp,'fp':fp,'tn':tn,'fn':fn,'ppv':tp/(tp+fp) if tp+fp else None,'npv':tn/(tn+fn) if tn+fn else None,
            'scope':'Expected counts for an invented test; not a named questionnaire, personal diagnosis or suicide-risk model'}

def standardized_difference(mean_a=50,mean_b=45,sd_a=10,sd_b=12,n_a=30,n_b=30):
    finite(mean_a=mean_a,mean_b=mean_b);positive(sd_a=sd_a,sd_b=sd_b);count(n_a=n_a,n_b=n_b)
    if min(n_a,n_b)<2:raise ValueError('Each independent group requires at least two observations')
    df=n_a+n_b-2;pooled=sqrt(((n_a-1)*sd_a**2+(n_b-1)*sd_b**2)/df);d=(mean_b-mean_a)/pooled;j=1-3/(4*df-1)
    return {'raw_difference':mean_b-mean_a,'pooled_sd':pooled,'cohen_d':d,'hedges_g_approx':j*d,
            'scope':'Independent-group, same-outcome arithmetic with approximate small-sample correction; not clinical importance, individual improvement or cross-scale permission'}

def coverage(record,required):
    return {'known':[key for key in required if key in record and record[key] is not None],
            'unknown':[key for key in required if key not in record or record[key] is None]}

CASES={
 'message':{'observation':'同事兩小時沒有回覆非緊急訊息','interpretation':'他一定覺得我的問題很糟','emotion':'擔心','alternative':'可能忙碌，也可能需要時間；目前原因未知','action':'確認截止時間，需要時禮貌補充背景，而非假定對方想法'},
 'meeting':{'observation':'會議時一次發言被打斷','interpretation':'我永遠都不適合發言','emotion':'挫折','alternative':'一次互動不能定義全部能力；也可評估會議規則是否公平','action':'準備一個要點、表達需要完整發言的界線，必要時尋求支持'},
 'deadline':{'observation':'今天新增兩項工作，原排程未調整','interpretation':'做不完就是我不夠努力','emotion':'緊繃','alternative':'工作量與可用時間需要重新協調','action':'列出任務、未知工時與優先順序，向可協助者討論資源或期限'}
}
def thought_case(name='message'):
    if name not in CASES:raise ValueError('Use one of the fictional cases')
    return dict(CASES[name],scope='Original fictional reflection, not a truth detector, diagnosis or an instruction to ignore mistreatment')

def support_response(name='listen'):
    responses={'listen':'先詢問對方願不願意談，回應感受，再問希望陪伴、一起想辦法或協助找資源。',
               'boundary':'說明你可提供的時間與協助，尊重對方意願，也保留自己的界線與專業轉介。',
               'urgent':'若有立即安全問題，陪同連結當地緊急醫療與受訓專業人員；不以網頁分數宣告安全。'}
    if name not in responses:raise ValueError('Known teaching scenario required')
    return {'scenario':name,'example':responses[name],'scope':'General support education, not automated crisis triage or a substitute for emergency help'}

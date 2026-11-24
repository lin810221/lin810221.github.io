"""Reproduce original chapter diagrams and editable reading tasks (no network)."""
import html
import json
import math
import re
import unicodedata
from pathlib import Path
from visual_specs import SPECS

ROOT=Path(__file__).resolve().parents[1]
C=['#b8e895','#89c9e8','#eebc79','#c3a6ed','#ef9eaa']
def esc(s):return html.escape(str(s),quote=True)
def txt(x,y,s,size=22,color='#e5e9e2',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{esc(s)}</text>'
def line(x,y,u,v,color='#526053',width=2,arrow=False):
    return f'<path d="M{x},{y} L{u},{v}" stroke="{color}" stroke-width="{width}" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def box(x,y,w,h,label,color=C[0]):
    size=20 if h>=60 else 17
    capacity=(w-22)/size;rows=[''];used=0
    for ch in str(label):
        width=1 if unicodedata.east_asian_width(ch) in 'WF' else .6
        if used+width>capacity and rows[-1]:rows.append('');used=0
        rows[-1]+=ch;used+=width
    result=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#1b251f" stroke="{color}"/>'
    for i,row in enumerate(rows):result+=txt(x+w/2,y+h/2+(i-(len(rows)-1)/2)*(size+4)+size*.35,row,size,color,'middle')
    return result
def dot(x,y,r=5,color=C[0]):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'
def path(points,color=C[0],width=4):
    return '<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>'
def axes(xlabel='x（教學單位）',ylabel='y（教學單位）'):
    s=line(160,530,1030,530,arrow=True)+line(160,530,160,210,arrow=True)
    for y in [290,370,450]:s+=line(160,y,1010,y,'#28352c',1)
    return s+txt(1020,568,xlabel,20,anchor='end')+txt(165,190,ylabel,20)
def curve(fn,color=C[0]):return path([(170+i*8.3,520-fn(i/100)*280) for i in range(101)],color)

def draw(kind,labels):
    """Geometry communicates relationships; numeric plots are explicit toy models."""
    s=''; quantitative=False
    if kind=='population':
        s+=f'<rect x="125" y="210" width="950" height="340" rx="26" fill="#1b251f" stroke="{C[0]}"/>'
        s+=txt(150,245,'目標母體',24,C[0])
        s+=f'<rect x="350" y="265" width="660" height="245" rx="20" fill="#152027" stroke="{C[1]}"/>'+txt(375,300,'抽樣框涵蓋部分',23,C[1])
        for i in range(40):
            x=390+i*83%560;y=340+i*37%130
            s+=dot(x,y,7,C[2] if i%5==0 else '#5a7468')
        for i in range(12):s+=dot(170+i*31%130,300+i*47%190,7,'#5a7468')
        s+=txt(600,590,'橙點：實際抽到的樣本；框外：未涵蓋對象',23,C[2],'middle')
    elif kind=='factors':
        s+=box(125,315,200,80,'潛在構念',C[0])
        for i in range(3):
            y=220+i*115;s+=line(325,355,590,y+35,C[1],2,True)+box(600,y,200,70,f'題項 {i+1}',C[1])
        s+=box(880,235,225,80,'信度：一致性',C[2])+box(880,415,225,80,'效度：解釋證據',C[3])
        s+=txt(600,585,'反映式測量示意；信度與效度是不同的評估問題',22,C[1],'middle')
    elif kind=='balance':
        s+=txt(340,225,'資產',28,C[0],'middle')+txt(850,225,'負債與權益',28,C[1],'middle')
        s+=line(600,250,600,530,C[1],3)+line(140,250,1080,250,C[1],3)
        s+=box(190,285,340,75,'準備資產 20',C[0])+box(190,385,340,110,'貸款 80',C[0])
        s+=box(680,285,340,110,'存款負債 90',C[1])+box(680,420,340,75,'權益 10',C[2])
        s+=txt(600,580,'資產 100 = 負債 90 + 權益 10（任意貨幣單位）',24,C[2],'middle')
    elif kind=='trade':
        s+=txt(600,210,'每投入相同一單位資源的產量（算例）',25,C[1],'middle')
        s+=txt(610,265,'商品 X',23,C[0],'middle')+txt(890,265,'商品 Y',23,C[1],'middle')
        for i,(country,a,b) in enumerate([('國家 A',6,3),('國家 B',2,2)]):
            y=300+i*100;s+=box(165,y,240,75,country,C[i])+box(490,y,240,75,str(a),C[0])+box(775,y,240,75,str(b),C[1])
        s+=txt(180,550,'A：1 X 的成本 = 0.5 Y；B：1 X 的成本 = 1 Y',23,C[2])
        s+=txt(180,590,'A 在 X 有比較利益；B 在 Y 有比較利益',23,C[1])
    elif kind in {'flow','gate','timeline','lanes','chunks','funnel','accounting','compare'}:
        if kind in {'balance','trade','compare'}:
            n=len(labels);w=900/n
            for i,label in enumerate(labels):
                s+=box(150+i*w,250,w-18,90,label,C[i%5])
                s+=line(165+i*w,380,130+(i+1)*w,380,C[i%5],4)
                s+=txt(150+i*w,425,['條件／輸入','行為／計算','結果／驗收','紀錄／限制','比較基準'][i],19)
            s+=txt(600,500,'依相同任務與條件比較，不由外觀推論等價',22,C[1],'middle')
        elif kind=='chunks':
            for i in range(3):
                s+=box(170,225+i*90,320,65,f'文件區段 {i+1}',C[1])
                s+=line(500,255+i*90,655,255+i*55,C[0],2,True)
            for i in range(5):s+=box(675,205+i*58,340,44,f'{labels[min(i,len(labels)-1)]} · {i+1}',C[i%5])
            s+=txt(180,560,'相鄰區塊可保留重疊；ID與版本跟著區塊走',22)
        else:
            n=len(labels);w=1000/n
            for i,label in enumerate(labels):
                s+=box(100+i*w,290,w-26,90,label,C[i%5])
                s+=txt(100+i*w,260,str(i+1).zfill(2),20,C[i%5])
                if i<n-1:s+=line(80+(i+1)*w,335,96+(i+1)*w,335,C[0],2,True)
            if kind=='gate':
                s+=line(600,380,600,455,C[2],3)+line(600,455,190,455,C[2],3,True)
                s+=txt(600,495,'條件不符：停止、修正或交由人工處理',22,C[2],'middle')
            elif kind=='timeline':
                s+=line(100,465,1100,465,C[1],3,True)+txt(600,510,'時間／事件順序 →',22,C[1],'middle')
            elif kind=='funnel':
                s+=path([(140,410),(1060,410),(820,530),(380,530),(140,410)],C[1])
                s+=txt(600,495,'逐階段縮小候選；在每一層記錄損失',22,C[1],'middle')
            elif kind=='accounting':s+=txt(600,490,'Y = C + I + G + NX（會計恆等式）',28,C[1],'middle')
            else:s+=txt(600,485,'沿箭頭追蹤：每一步用了哪些輸入、產生哪些輸出？',22,C[1],'middle')
    elif kind in {'fork','loop','tree','graph','network','factors','attention','convolution','sequence','diffusion'}:
        if kind in {'loop','sequence','diffusion'}:
            for i,label in enumerate(labels):
                x=100+i*200;s+=box(x,280,174,86,label,C[i%5])
                if i<4:s+=line(x+176,323,x+198,323,C[0],2,True)
            if kind=='loop':
                s+=path([(1070,375),(1070,465),(185,465),(185,375)],C[1])+line(185,400,185,370,C[1],2,True)
                s+=txt(600,510,'完成條件成立 → 離開；否則帶著更新資料繼續',22,C[1],'middle')
            elif kind=='diffusion':
                for j in range(5):
                    for k in range(24):
                        x=140+j*200+(k*37%96);y=408+(k*23%95)
                        s+=dot(x,y,2+(4-j)*0.8,C[j])
                s+=txt(600,552,'示意逐步改變狀態；點的位置不代表模型實測',20,C[1],'middle')
            else:s+=txt(600,490,'順序與上下文沿連接傳遞，注意每一步的可見範圍',22,C[1],'middle')
        elif kind in {'network','attention','convolution'}:
            counts=[4,5,3] if kind!='convolution' else [5,3,2]
            for layer,n in enumerate(counts):
                for i in range(n):
                    x=240+layer*350;y=260+i*55
                    if layer<2:
                        for j in range(counts[layer+1]):
                            if kind!='convolution' or abs(i-j)<=1:s+=line(x,y,x+350,260+j*55,'#405b4b',2)
                    s+=dot(x,y,14,C[layer])
                s+=txt(240+layer*350,555,labels[min(layer,len(labels)-1)],22,C[layer],'middle')
            if kind=='attention':s+=txt(600,200,'連線強度隨輸入改變；此圖只示意資料關係',21,C[1],'middle')
        else:
            nodes=[(135,325),(470,225),(470,425),(825,325),(1000,325)]
            edges=[(0,1),(0,2),(1,3),(2,3),(3,4)]
            if kind in {'tree','factors'}:
                nodes=[(160,325),(490,220),(490,430),(890,220),(890,430)];edges=[(0,1),(0,2),(1,3),(2,4)]
            for a,b in edges:s+=line(nodes[a][0]+74,nodes[a][1],nodes[b][0]-75,nodes[b][1],C[1],2,True)
            for i,(x,y) in enumerate(nodes):s+=box(x-80,y-35,160,70,labels[min(i,len(labels)-1)],C[i])
            s+=txt(600,550,'分支與匯合需說清楚：分開的是資料、路徑，還是責任？',21,C[1],'middle')
    elif kind in {'matrix','payoff','tensor'}:
        rows=3 if kind!='payoff' else 2;cols=4 if kind!='payoff' else 2
        for r in range(rows):
            for c in range(cols):
                value=f'{(r+1)*(c+1)}' if kind!='payoff' else [['3, 3','0, 5'],['5, 0','1, 1']][r][c]
                s+=box(265+c*155,240+r*85,142,74,value,C[(r+c)%5])
        s+=txt(600,550,'形狀與軸的語意一起看；矩陣數值為教學算例',22,C[1],'middle')
        s+=txt(600,200,' × '.join(labels[:3]),23,C[0],'middle')
        if kind=='payoff':
            s+=txt(225,285,'A 策略1',20,C[0],'end')+txt(225,370,'A 策略2',20,C[0],'end')
            s+=txt(335,220,'B 策略1',20,C[1],'middle')+txt(490,220,'B 策略2',20,C[1],'middle')
            s+=txt(600,475,'格內為（玩家 A 報酬，玩家 B 報酬）',22,C[2],'middle')
    else:
        quantitative=True
        xy={
          'supply-demand':('數量 Q／產出 Y','價格 P／物價水準'),
          'externality':('數量 Q','邊際成本／利益'),
          'budget':('商品 X','商品 Y'), 'frontier':('商品 X 產量','商品 Y 產量'),
          'cost':('產量 Q（任意尺度）','每單位成本（任意尺度）'), 'growth':('人均資本 k','投資／折舊（示意）'),
          'histogram':('數值區間','次數'), 'distribution':('隨機變數 x','密度 f(x)'),
          'tails':('檢定統計量','虛無假設下密度'), 'sampling':('樣本平均值','重複抽樣的密度'),
          'calibration':('預測機率','觀察比例'), 'regression':('解釋變數 x','反應變數 y'),
          'contour':('參數一','參數二'), 'bars':('候選項目','機率（示意）'),
          'classification':('特徵一','特徵二'), 'scatter':('第一維','第二維'),
          'vectors':('向量第一維','向量第二維'), 'contrast':('投影第一維','投影第二維'),
          'projection':('投影第一維','投影第二維'), 'interval':('參數值（示意尺度）','不同重複樣本'),
          'boxplot':('觀察值（示意尺度）','資料摘要'), 'anova':('組別','反應值（示意）'),
          'folds':('樣本區段','不同訓練／驗證輪次'), 'population':('觀察值（示意尺度）','資料來源')}
        s+=axes(*xy.get(kind,('x（教學單位）','y（教學單位）')))
        if kind in {'supply-demand','externality','budget','frontier','cost','growth'}:
            if kind=='supply-demand':
                s+=curve(lambda x:1-x*.9,C[1])+curve(lambda x:.1+x*.9,C[0])+dot(585,366,8,C[2])
                s+=txt(930,272,labels[3] if len(labels)>3 else 'S',23,C[0])+txt(930,480,labels[2],23,C[1])
                s+=txt(600,345,'均衡',23,C[2])
            elif kind=='externality':
                s+=curve(lambda x:.1+.5*x,C[0])+curve(lambda x:.3+.5*x,C[2])+curve(lambda x:1-.7*x,C[1])
                s+=txt(790,250,'社會成本',22,C[2])+txt(820,410,'私人成本',22,C[0])
            elif kind in {'budget','frontier'}:
                s+=curve(lambda x:1-x if kind=='budget' else math.sqrt(max(0,1-x*x)),C[0])
                s+=dot(450,440,9,C[1])+txt(470,442,'可行組合',22,C[1])+dot(900,230,9,C[2])+txt(805,205,'限制之外',22,C[2])
            elif kind=='growth':
                s+=curve(lambda x:.92*math.sqrt(x),C[0])+curve(lambda x:x,C[2])
                s+=txt(480,275,'投資',22,C[0])+txt(830,230,'折舊',22,C[2])+dot(873,283,8,C[1])
            else:
                # AC=a/q+b+cq, MC=b+2cq; intersection at AC's minimum.
                s+=curve(lambda x:(.09/(.12+x)+.08+.48*(.12+x))*.8,C[0])+curve(lambda x:(.08+.96*(.12+x))*.8,C[1])
                s+=txt(800,420,'AC（示意）',22,C[0])+txt(820,255,'MC（示意）',22,C[1])
        elif kind in {'distribution','sampling','tails'}:
            bell=lambda x:math.exp(-((x-.5)/.19)**2/2)
            if kind=='tails':
                pts=[(170,530)]+[(170+i*8.3,520-bell(i/100)*280) for i in range(0,26)]+[(378,530)]
                pts2=[(792,530)]+[(170+i*8.3,520-bell(i/100)*280) for i in range(75,101)]+[(1000,530)]
                for ps in [pts,pts2]:s+='<polygon points="'+' '.join(f'{x},{y}' for x,y in ps)+f'" fill="{C[2]}" opacity=".35"/>'
            s+=curve((lambda x:.5*bell(x)) if kind=='sampling' else bell,C[0])
            if kind=='sampling':s+=curve(lambda x:math.exp(-((x-.5)/.095)**2/2),C[1])+txt(690,235,'藍：樣本數較大，標準誤較小',20,C[1])+txt(690,275,'綠：樣本數較小',20,C[0])
            if kind=='tails':s+=txt(770,325,'尾端面積',23,C[2])+line(880,340,905,476,C[2],2,True)
        elif kind in {'histogram','bars'}:
            heights=[3/16,7/16,12/16,1,10/16,4/16] if kind=='histogram' else [.05,.12,.24,.31,.19,.09]
            for i,h in enumerate(heights):
                x=200+i*128;w=118 if kind=='histogram' else 65
                height=h*(280 if kind=='histogram' else 800)
                s+=f'<rect x="{x}" y="{530-height}" width="{w}" height="{height}" fill="{C[i%5]}" opacity=".8"/>'
                s+=txt(x+w/2,515-height,str(round(h*16)) if kind=='histogram' else f'{h:.2f}',18,anchor='middle')
                s+=txt(x+w/2,560,str(i+1),19,anchor='middle')
        elif kind in {'interval','boxplot','folds','population','anova'}:
            if kind=='interval':
                s+=line(585,230,585,520,C[2],3)+txt(605,230,'固定參數',21,C[2])
                for i,(a,b) in enumerate([(380,710),(450,820),(640,940),(300,650)]):
                    y=290+i*65;color=C[0] if a<=585<=b else C[4]
                    s+=line(a,y,b,y,color,5)+line(a,y-12,a,y+12,color,3)+line(b,y-12,b,y+12,color,3)
            elif kind=='boxplot':
                s+=line(260,365,950,365,C[1],4)+box(400,305,340,120,'',C[0])+line(530,305,530,425,C[2],5)
                for x,t in [(260,'最小值'),(400,'Q1'),(530,'中位數'),(740,'Q3'),(950,'最大值')]:s+=txt(x,475,t,21,anchor='middle')
            elif kind=='folds':
                for r in range(4):
                    for c in range(5):s+=f'<rect x="{210+c*152}" y="{240+r*65}" width="140" height="48" rx="5" fill="{C[2] if c==r else C[0]}" opacity=".75"/>'
                s+=txt(600,510,'綠：訓練　橙：驗證；最後測試集另行保留',21,C[1],'middle')
            else:
                for g in range(3):
                    for i in range(12):s+=dot(310+g*275+(i%3-1)*24,465-g*60-(i*37%110),6,C[g])
                    s+=txt(310+g*275,564,labels[g],21,C[g],'middle')
                    s+=line(250+g*275,415-g*60,370+g*275,415-g*60,C[g],4)
        elif kind=='contour':
            for i in range(5):s+=f'<ellipse cx="590" cy="375" rx="{70+i*65}" ry="{30+i*26}" stroke="{C[i]}" stroke-width="3" fill="none"/>'
            s+=path([(910,250),(820,400),(710,320),(650,385),(590,375)],C[0])+dot(590,375,8,C[2])
        elif kind in {'vectors','projection'}:
            for i,(u,v) in enumerate([(430,270),(850,335),(750,470)]):s+=line(165,525,u,v,C[i],5,True)+txt(u+10,v-10,labels[i],22,C[i])
            s+=line(430,270,570,420,C[3],2)+txt(560,390,'投影／比較方向',21,C[3])
        else:
            for i in range(34):
                x=210+(i*83%740)
                if kind in {'classification','contrast','scatter'}:
                    g=i%2;y=260+(i*31%130)+g*125;color=C[g]
                else:y=515-(x-170)*.29+((i*47)%90-45);color=C[0]
                s+=dot(x,y,6,color)
            if kind in {'regression','calibration'}:
                s+=line(190,510,1000,260,C[2],4)
                if kind=='regression':s+=line(608,385,608,425,C[3],3)+txt(630,421,'殘差',22,C[3])
            if kind=='classification':s+=line(240,410,950,330,C[2],4)+txt(790,310,'分類邊界（示意）',21,C[2])
    return s,quantitative

def generate(only=None):
    reports=[]
    for slug,specs in SPECS.items():
        if only and slug not in only:continue
        folder=ROOT/slug;catalog=json.loads((folder/'course.json').read_text(encoding='utf-8'))
        assert len(specs)==len(catalog['groups']),(slug,len(specs),len(catalog['groups']))
        figures=[];index=['# 章節圖解與讀圖練習','','原創概念圖；數值圖為明示的教學算例。軟體基準沿用課程既有版本。','']
        for number,(group,spec) in enumerate(zip(catalog['groups'],specs),1):
            kind,title,labels,notes=spec;name=f'review-{number:02d}-{group["id"]}'
            file=f'assets/figures/{name}.svg';target=folder/file;target.parent.mkdir(parents=True,exist_ok=True)
            body,quantitative=draw(kind,labels)
            desc='；'.join(notes)+'。'+('座標圖為教學算例，沒有使用實測或臨床資料。' if quantitative else '')
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#89c9e8"/></marker></defs><rect width="1200" height="800" rx="20" fill="#101812"/><g font-family="Microsoft JhengHei,Noto Sans CJK TC,sans-serif">'
            svg+=txt(54,58,f'{slug.upper()} / {group["number"]}',19,C[0])+txt(54,115,title,34)
            svg+=txt(54,154,'原創概念圖 · '+('教學算例，非實測數據' if quantitative else '沿資料、控制與比較關係讀圖'),20,'#9aaf9f')
            svg+=body+line(54,620,1146,620,'#405448')
            for i,note in enumerate(notes):svg+=txt(60,668+i*43,f'{i+1}. {note}',23,C[i])
            svg+=txt(54,766,'Learning Notes · Visual review 2026-11-24',17,'#9aaf9f')+'</g></svg>'
            target.write_text(svg,encoding='utf-8')
            figure={'id':name,'file':file,'title':title,'alt':title+'；'+desc,'caption':desc,'group':group['id'],'kind':kind,'origin':'Original instructional diagram, 2026-11-24','sourceIds':[]}
            figures.append(figure)
            units=[l for l in catalog['lessons'] if l['group']==group['id']]
            for i,lesson in enumerate(units):
                focus=labels[i%len(labels)]
                task=f'讀完「{lesson["title"]}」後，在圖上指出「{focus}」的位置或對應關係；用本單元的一個例子說明它與「{labels[(i+1)%len(labels)]}」的關係，再寫出一個適用條件或限制。'
                lesson['visual']=name;lesson['visualTask']=task
                p=folder/'chapters'/f'{lesson["id"]}.md';source=p.read_text(encoding='utf-8')
                block=f'\n\n<!-- chapter-visual:start -->\n## 圖解與讀圖任務\n\n![{figure["alt"]}]({file})\n\n> **圖解｜{title}**：{desc}\n\n**本單元讀圖任務**：{task}\n<!-- chapter-visual:end -->\n'
                if '<!-- chapter-visual:start -->' in source:source=re.sub(r'\n*<!-- chapter-visual:start -->.*?<!-- chapter-visual:end -->\n*',block+'\n',source,flags=re.S)
                else:
                    m=re.search(r'^## ',source,re.M);pos=m.start() if m else len(source)
                    source=source[:pos]+block+'\n'+source[pos:]
                if p.read_text(encoding='utf-8')!=source:p.write_text(source,encoding='utf-8')
            index+=[f'## {group["number"]} {title}','',f'![{title}](../{file})','',desc,'']
            index +=[f'- **{l["title"]}**：{l["visualTask"]}' for l in units];index+=['']
        catalog['visuals']=figures;catalog['visualPresentation']='chapter';catalog['visualUpdated']='2026-11-24'
        # Preserve software/content version dates: this review adds illustrations.
        study=folder/'study';study.mkdir(exist_ok=True);(study/'chapter-figures.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
        if not catalog.get('studyBundle'):catalog['studyBundle']=f'{slug}-study.zip'
        catalog['studyFiles']=list(dict.fromkeys(catalog.get('studyFiles',[])+['study','assets/figures']))
        resources=catalog.setdefault('learningResources',[])
        resources=[r for r in resources if isinstance(r,str)]
        if catalog['studyBundle'] not in resources:resources.append(catalog['studyBundle'])
        catalog['learningResources']=resources
        (folder/'course.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        reports.append({'course':slug,'figures':len(figures),'units':len(catalog['lessons'])})
    return reports
if __name__=='__main__':
    import sys
    print(json.dumps(generate(sys.argv[1:]),ensure_ascii=False,indent=2))

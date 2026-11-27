"""Find mathematical notation left in ordinary course prose, outside LaTeX/code.

This is an editorial queue, not an automatic formula converter. It never guesses
whether C is a class count or a constant and never edits code or Markdown itself.
"""
import argparse,json,re
from collections import Counter
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROTECTED=re.compile(r'<!-- chapter-visual:start -->[\s\S]*?<!-- chapter-visual:end -->|<div class="(?:tf-task|health-read-task)"[^>]*>[\s\S]*?</div>|(?m:^```[^\n]*\n[\s\S]*?^```[^\n]*$)|(?m:^~~~[^\n]*\n[\s\S]*?^~~~[^\n]*$)|\$\$[\s\S]*?\$\$|(?<![\\$])\$(?!\$)[^\n$]+\$(?!\$)|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|`+[^`\n]+`+|</?[A-Za-z][A-Za-z0-9:-]*(?=[\s/>])(?:[^"\'<>]|"[^"]*"|\'[^\']*\')*>|!?\[[^\n]*?\]\([^\n]*?\)|https?://\S+|\{#[^}]+\}')
CHARS=r'A-Za-z0-9_α-ωΑ-Ωȳŷ∂∇∫∑∏√∞∈∉∪∩²³⁴⁵⁶⁷⁸⁹⁰¹⁻⁺ᵀᵗᶜ₀-₉ᵢⱼₖₙ̄̂̃()\[\]{}.,+*/^=<>!≤≥≠≈±−×·⊙∝∼|%′\-'
RUN=re.compile('['+CHARS+']+')
SIGNAL=re.compile(r'(?:[A-Za-z0-9α-ωΑ-Ω)\]]\s*[=<>≤≥≠≈±^×⊙∝∼−+*/]\s*[A-Za-z0-9α-ωΑ-Ω(\[\d.-])|[∫∑∏√²³ᵀ₀-₉̄̂]|(?:\b(?:P|E|Var|Cov|SD|SE|N|U)\()|(?<![A-Za-z])npq?(?![A-Za-z])')
NON_MATH={'I/O','TCP/IP','HTTP/HTTPS','CI/CD','A/B','FP32/FP16','Q/K/V','FP/FN','TP/FP','CPU/GPU','train/eval','sin/cos','precision/recall'}
LITERALS_PATH=ROOT/'tools/math-prose-literals.json'
def uncovered(source):
    return PROTECTED.sub(lambda m:re.sub(r'[^\n]',' ',m[0]),source)
def candidates(source):
    text=uncovered(source)
    for m in RUN.finditer(text):
        token=m[0].strip('.,')
        if token in NON_MATH or not SIGNAL.search(token):continue
        if not re.search(r'[A-Za-z0-9α-ωΑ-Ω]',token):continue
        line=source.count('\n',0,m.start())+1
        yield {'line':line,'token':token,'context':source.splitlines()[line-1]}
@lru_cache(maxsize=1)
def literal_tokens():
    if not LITERALS_PATH.exists():return set()
    return {x['token'] for x in json.loads(LITERALS_PATH.read_text(encoding='utf-8'))['literals']}
def issues(source):
    """Reject uncovered equations; approved literal units/names remain prose."""
    approved=literal_tokens()|NON_MATH
    rows=[r for r in candidates(source) if r['token'] not in approved]
    masked=uncovered(source)
    for m in re.finditer(r'\\(?:frac|dfrac|sqrt|sum|int|begin|alpha|beta|mu|sigma|theta)\b',masked):
        rows.append({'line':source.count('\n',0,m.start())+1,'token':m[0],'context':'TeX command outside a math delimiter'})
    return rows
def assert_math_prose(source,label):
    rows=issues(source)
    if rows:raise ValueError(f'Unformatted mathematical prose in {label}: '+str(rows[:5]))
def audit(names=None,strict=False):
    results=[]
    for p in sorted(ROOT.glob('*/course.json')):
        if names and p.parent.name not in names:continue
        for path in sorted((p.parent/'chapters').glob('*.md')):
            for row in (issues if strict else candidates)(path.read_text(encoding='utf-8')):results.append({'file':path.relative_to(ROOT).as_posix(),**row})
        c=json.loads(p.read_text(encoding='utf-8'))
        for lesson in c['lessons']:
            for row in (issues if strict else candidates)(lesson.get('summary','')):results.append({'file':p.relative_to(ROOT).as_posix(),'field':lesson['id']+'/summary',**row})
    return results
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('courses',nargs='*');parser.add_argument('--output',type=Path);parser.add_argument('--strict',action='store_true');args=parser.parse_args()
    rows=audit(args.courses,args.strict)
    if args.output:args.output.parent.mkdir(exist_ok=True,parents=True);args.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Candidates:',len(rows));print(json.dumps(Counter(r['file'].split('/')[0] for r in rows),ensure_ascii=False))
    for r in rows[:60]:print(f'{r["file"]}:{r["line"]}: {r["token"]}')
    if args.strict and rows:raise SystemExit(1)

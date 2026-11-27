"""Catch omitted definitions as well as equations left outside math delimiters."""
import json,re,unittest
from pathlib import Path
from audit_math_prose import issues,audit
from build import assert_readable
ROOT=Path(__file__).resolve().parents[1]

def sections(source):
    return {m[1]:m[2] for m in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',source,re.M|re.S)}
def display_math(source):
    source=re.sub(r'```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~','',source,flags=re.S)
    return '\n'.join(a or b for a,b in re.findall(r'\$\$(.*?)\$\$|\\\[(.*?)\\\]',source,re.S))
def assert_topic_definitions(catalog):
    errors=[]
    for slug,course in catalog['courses'].items():
        for lesson,expected in course['formulaSections'].items():
            source=(ROOT/slug/'chapters'/(lesson+'.md')).read_text(encoding='utf-8')
            present=sections(source)
            for entry in expected:
                heading=entry['heading']
                if heading not in present or not display_math(present[heading]).strip():errors.append((slug,lesson,heading))
    return errors

class MathEditorialTests(unittest.TestCase):
    def test_plain_math_is_flagged_even_without_existing_tex(self):
        for text in ['各機率1/k，均值(a+b)/2。','均值np。','變異數np(1−p)。','標準誤σ/√n。','P(A|B)=P(A∩B)/P(B)。',r'未包分隔符的 \frac{a}{b}。']:
            self.assertTrue(issues(text),text)
    def test_inequality_is_not_mistaken_for_an_html_tag(self):
        self.assertTrue(issues('條件 x<3，下一行 y>4。'))
        self.assertTrue(issues('P(a<X≤b)=F(b)−F(a)。'))
        self.assertTrue(issues('K∼Binomial(n,p)。'))
    def test_existing_math_and_code_keep_their_roles(self):
        self.assertEqual(issues(r'公式 $\frac{a+b}{2}$，API `randint(1, 7)`。'),[])
        self.assertEqual(issues('```python\nx = y / z\n```\n體積以 mg/dL 表示，CO₂ 是分子名稱。'),[])
    def test_unknown_ratio_does_not_get_a_blanket_slash_exception(self):
        self.assertTrue(issues('新公式 FooBar/BazQux。'))
        self.assertTrue(issues('公式 R²=1-SSE/SST。'))
        self.assertTrue(issues('均衡條件 P=MC。'))
        self.assertTrue(issues('圖像大小 3×3。'))
    def test_no_invisible_control_characters(self):
        for token in ['\x07lpha','\x08eta','\x0crac']:
            with self.assertRaises(ValueError):assert_readable(token,'fixture')
    def test_all_course_sources_and_summaries_have_been_checked(self):
        self.assertEqual(audit(strict=True),[])
    def test_definitions_remain_in_their_own_topic_sections(self):
        coverage=json.loads((ROOT/'tools/math-topic-coverage.json').read_text(encoding='utf-8'))
        self.assertEqual(set(coverage['courses']),{p.parent.name for p in ROOT.glob('*/course.json')})
        self.assertEqual(assert_topic_definitions(coverage),[])
    def test_each_discrete_distribution_has_its_own_pmf_and_moments(self):
        source=(ROOT/'applied-statistics/chapters/17-discrete-families.md').read_text(encoding='utf-8')
        items=sections(source)
        for anchor in ['4-4-1','4-4-2','4-4-3','4-4-4-poisson']:
            body=next(b for h,b in items.items() if '{#'+anchor+'}' in h);tex=display_math(body)
            self.assertIn('P(X=',tex);self.assertIn('E[X]',tex);self.assertIn(r'\operatorname{Var}(X)',tex)
        uniform=next(b for h,b in items.items() if '{#4-4-1}' in h)
        self.assertIn(r'\begin{cases}',display_math(uniform))
        self.assertIn(r'\dfrac{1}{m}',display_math(uniform))
    def test_sibling_formula_cannot_hide_an_omitted_definition(self):
        source=(ROOT/'applied-statistics/chapters/17-discrete-families.md').read_text(encoding='utf-8')
        damaged=re.sub(r'(## 離散均勻分配[^\n]*\n).*?(?=## 二項分配)',r'\1有限 m 個結果，各機率 1/m。\n\n',source,flags=re.S)
        body=next(b for h,b in sections(damaged).items() if '{#4-4-1}' in h)
        self.assertFalse(display_math(body))
        self.assertTrue(display_math(next(b for h,b in sections(damaged).items() if '{#4-4-2}' in h)))
        self.assertTrue(issues(body))
    def test_mse_and_bce_have_definitions_in_pytorch_too(self):
        source=(ROOT/'pytorch/chapters/18-losses.md').read_text(encoding='utf-8')
        for heading,body in sections(source).items():
            if 'BCEWithLogitsLoss' in heading or 'MSELoss' in heading:self.assertTrue(display_math(body),heading)

if __name__=='__main__':unittest.main()

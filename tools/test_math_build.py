"""Meaningful regression cases for TeX/Markdown boundaries and damaged encoding."""
import unittest
import markdown
from build import MathExtension, summary_math, assert_readable

def convert(s):return markdown.markdown(s,extensions=['fenced_code','tables',MathExtension()])
class MathPipelineTests(unittest.TestCase):
    def test_inline_underscore_and_comparison_survive(self):
        h=convert(r'估計 $x_i < y_j$ 與 $\alpha + \beta$。')
        self.assertIn('data-tex="x_i &lt; y_j"',h)
        self.assertNotIn('<em>',h)
    def test_matrix_display_survives(self):
        h=convert('$$\n'+r'\begin{bmatrix}1&2\\3&4\end{bmatrix}'+'\n$$')
        self.assertIn('class="math-block"',h)
        self.assertIn('1&amp;2',h)
    def test_table_tex_pipe_is_not_a_column(self):
        h=convert('| 公式 | 意義 |\n|---|---|\n| $P(A|B)$ | 條件機率 |')
        self.assertEqual(h.count('<td>'),2)
        self.assertIn('P(A|B)',h)
    def test_code_and_escaped_money_stay_literal(self):
        h=convert('`$x$` 與 `$$`\n\n```python\ns = "$$x$$"\n```\n\n價格 \\$10。')
        self.assertNotIn('data-tex',h)
    def test_parentheses_and_brackets(self):
        h=convert(r'\(a_i\)'+'\n\n'+r'\[a^2+b^2\]')
        self.assertEqual(h.count('data-tex'),2)
    def test_summary_escapes_markup_and_preserves_tex(self):
        h=summary_math(r'<img src=x>，$x<y$')
        self.assertIn('&lt;img',h);self.assertNotIn('<img',h)
        self.assertIn('data-tex="x&lt;y"',h)
    def test_unclosed_display_fails(self):
        with self.assertRaisesRegex(ValueError,'Unclosed'):convert('$$x')
    def test_real_damage_fails_but_code_question_marks_are_valid(self):
        for s in ['內容???失去','內容\ufffd']:
            with self.assertRaises(ValueError):assert_readable(s,'fixture')
        assert_readable('```python\ns="???"\n```','fixture')
if __name__=='__main__':unittest.main()

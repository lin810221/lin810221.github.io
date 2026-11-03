# 多重比較：Tukey、Games–Howell與Holm {#8-3-tukeygameshowellholm}

先定比較家族，再選與模型相符的差異、區間及調整p。

## 比較家族是什麼

三組全部兩兩比較有3項，四組有6項。若只關心A對控制組C，研究問題也許只需要兩項，而不是所有組合。事前contrast與事後探索應區分；不能事後只把顯著那對當成唯一研究問題。

## Tukey HSD

傳統共同variance模型下，Tukey以studentized range處理全部兩兩比較，提供家族層次的調整p及同時區間；不等樣本數時常稱Tukey–Kramer延伸。不能把普通t的未調整CI貼到Tukey p旁邊而不說明差別。

## Games–Howell

適合不同variance與樣本數的兩兩平均比較，以各對SE與近似自由度處理。statsmodels0.15提供pairwise_tukeyhsd(...,use_var='unequal')；參數名雖仍是tukeyhsd，結果方法已改，教材與報表要明確標Games–Howell。

## Holm與其他控制

Holm逐步控制家族型I錯誤，不要求檢定相互獨立；Bonferroni簡單但可能保守。Benjamini–Hochberg則控制不同目標FDR，在其適用條件下使用，不能和FWER當同一承諾。本課用[.01,.03,.20]示範Holm調整為[.03,.06,.20]。

## 差異方向與報告

第26例statsmodels兩兩差定義為第二組−第一組，與前面Welch的A−B方向不同，程式已標示。讀CI若全正，代表第二組較高；反向報告就需同時改差及區間符號。不要只依組名排列猜方向。

## 練習與解答

三組平均4、6、8，程式依G1、G2、G3排列差為2、4、2。若整體ANOVA未顯著是否能隨意到處搜尋？不能；事前規劃contrast和事後全部比較有不同程序。任何做法都需預先定義或清楚標探索，並處理家族錯誤。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/26_posthoc.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:26_posthoc.py -->

## 參考與官方來源

- [Tukey與Games–Howell介面](https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html)
- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)

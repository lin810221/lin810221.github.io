# 附錄F　符號、公式、版本與原目錄對照速查

讓你回來查定義、尾向與章節位置，保留完整學習脈絡。

## 版本與可重現基準

查核日期2026-11-02，SciPy1.18.1、statsmodels0.15.0、NumPy2.5.4、pandas3.1.0，Python3.13.13實測。需求檔包含已測相依版本；沒有宣稱每個底層套件都必須全球最新。更新時先重新查官方穩定版，在隔離環境實跑，再同步日期、程式、教材與ZIP。

## 常用符號

母體N、樣本n；母體平均μ、樣本平均x̄；母體variance σ²、樣本s²；母體比例p、樣本p̂；顯著水準α、型II誤差β、power1−β。SD描述觀察分散，SE描述統計量抽樣變動。q通常是左尾累積分位，不一定是上尾面積。

## 公式先配條件

平均SE=σ/√n是iid有限變異形式；未知σ的t精確需常態，比例二項需要固定n、獨立同p；variance卡方及精確F對正常性更敏感。ANOVA整體檢定不告訴你每對差異；相關與迴歸不自動支持因果。方法名稱永遠不能省略設計。

## 原目錄如何保留

Chapter01至09名稱與1-1到9-3節號保留；所有原列細目放在對應頁內標題與段落。Chapter10改為「問卷調查分析與Python實作」，保留10-1到10-11，基本操作換成Python與資料流程，其餘問卷、信效度、因素、交叉表和各項比較皆保留。十章各有習題詳解，附錄補查表、方法選擇與完整專題。

## 課程與檔案

70個閱讀單元在chapters，course.json定順序與分組；40個Python入口、獨立course_core與survey.csv在examples，完整下載包examples.zip。八個首頁互動實驗用JavaScript計算，沒有在瀏覽器執行SciPy。網站的搜尋、筆記與閱讀進度沿用共用閱讀器，並與其他領域分別保存。

## 參考與使用方式

教材為針對本課原創的說明、手算、合成案例與程式，並提供OpenStax、NIST、ASA及套件官方文件作進一步閱讀，沒有重製特定教科書正文或題庫。數理統計、機率與時間序列仍保留獨立領域；本課聚焦如何對資料選法、診斷、解讀與報告。

## 最後的自我檢核

若看到一個p值，能否說出其H0、模型、觀察單位、尾向、比較家族及效果區間？若做不到，回到對應章節補齊。讀完統計的成果不是記住所有表格數字，而是知道自己能回答什麼、不能從資料推出什麼。

## 參考與官方來源

- [SciPy官方發布](https://scipy.org/)
- [statsmodels正式文件](https://www.statsmodels.org/stable/)
- [NumPy統計運算](https://numpy.org/doc/stable/reference/routines.statistics.html)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)

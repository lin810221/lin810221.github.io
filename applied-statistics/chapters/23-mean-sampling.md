# 樣本平均數的抽樣分配與中央極限定理 {#5-4}

把精確常態結果、漸近結果與有限母體修正分開。

## 平均與變異 {#5-4-1}

iid、有限μ與σ²時，E(X̄)=μ、Var(X̄)=σ²/n，SE=σ/√n。期望的線性不需要獨立，但變異簡化需要處理共變異數。時間相關或同群資料會改SE，不能只把人數放入根號。

$$
E(\bar X)=\mu,\qquad \operatorname{SE}(\bar X)=\frac\sigma{\sqrt n}
$$

## 抽樣分配的形態 {#5-4-2}

若原母體常態，iid樣本平均任何n皆精確常態。若母體非正態，經典CLT在iid有限正變異等條件下，使標準化平均漸近標準常態；它沒有說原始資料變常態，也沒有普遍保證n=30足夠。偏態、尾端、少見事件與所需精確度都影響近似。

## 有限母體修正

從有限N不放回SRS，若σ_N²以N為分母定義母體變異，平均SE為σ_N/√n乘√((N−n)/(N−1))。n接近N時修正明顯，普查時抽樣誤差為0；測量錯誤仍可能存在。若用N−1分母定義母體變異，修正式會換等價形式，請先對齊記號。

## 指數母體的實際模擬

第09例以均值1、SD1的Exponential生成4000組，每組30筆，查看平均分布的實際均值與SD，理論SE=1/√30。觀察某一母體下近似表現，是具體證據而非所有分布的通用定理。首頁也可改n觀察偏態平均逐漸集中。

## 規模與成本

SE要縮半，iid條件下n需約四倍，不是兩倍。更多樣本的利益會遞減；改善測量、分層或研究設計也可能提升有效資訊。但改設計後需使用相符SE，不能保留原SRS公式再宣稱精度提升。

## 練習與解答

σ=12，n=36時SE2；n=144時SE1。某人說「樣本SD從12變2」，哪裡不對？2是平均估計的標準誤，不是單筆資料本身的標準差。兩者描述不同變動，報表應清楚標SD或SE。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/09_sampling_distribution.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:09_sampling_distribution.py -->

## 參考與官方來源

- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
- [SciPy統計文件](https://docs.scipy.org/doc/scipy/reference/stats.html)

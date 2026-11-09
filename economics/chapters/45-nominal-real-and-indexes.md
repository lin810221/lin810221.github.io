# 名目、實質、GDP平減與CPI

用同一份虛構商品表計算價格與數量變動，分清不同指數的權重。

## 固定基期分解

名目值用當期價格×當期數量；定基實質值用基期價格×當期數量。GDP平減指數在這個簡化中為名目/實質×100。若只看名目成長，可能把漲價誤認成產量增加。官方通常使用更複雜的連鎖方法，本例不冒充它。

## 固定籃子的CPI

Laspeyres形式用基期數量q0比較pt與p0；因此與使用當期產出組合的GDP平減不同。CPI涵蓋家庭消費範圍，進口消費品也可影響；GDP衡量境內產出。實際各國籃子、權重更新與住宅處理需查方法。

$$
CPI_t=100\frac{\sum_i p_{it}q_{i0}}{\sum_i p_{i0}q_{i0}},\qquad
D_t=100\frac{\sum_i p_{it}q_{it}}{\sum_i p_{i0}q_{it}}
$$

## 讀範例輸出

synthetic_basket.csv有2024–2026三種虛構最終商品。基期兩個指數都是100；後續價格與數量變動使兩指數不同。檔案中的年份不代表任何國家觀測，幣別是教學代幣。若替換成真實資料，先檢查籃子完整與商品定義，不直接沿用這個加總方法。

## 變動率與指數點

通膨率用指數相對變化，與指數點差不同。同比、月比、季調年率也不是同一概念；解讀時要說基期與頻率。若資料會修訂，還要標vintage，避免把今天修訂值當當時已知。

## 可執行實驗

依 [範例說明](examples/README.md) 準備 Python 3.15.2，在 `examples` 目錄執行 `python 23_price_indexes.py`。不需第三方套件、金鑰或網路。數字來自明確模型或虛構資料，先檢查單位與假設，再解讀輸出。

<!-- example:23_price_indexes.py -->

## 練習與解答

**先試著回答：** 為什麼CPI和GDP平減可能不同，即使使用同一商品表？

<details><summary>展開推導與解答</summary>

權重不同：CPI固定基期數量，定基GDP平減的比率反映當期數量組合。真實統計的涵蓋範圍與編製方法也不同；差異不等於有一方必然錯。

</details>

## 參考與跨課閱讀

- [BLS：CPI 問答](https://www.bls.gov/cpi/questions-and-answers.htm)
- [主計總處：連鎖值使用注意](https://www.stat.gov.tw/News_Content.aspx?n=2679&s=103006)
- [BEA：GDP 定義](https://www.bea.gov/help/glossary/gross-domestic-product-gdp)

[課程總覽](#overview) · [完整程式與資料](examples.zip)

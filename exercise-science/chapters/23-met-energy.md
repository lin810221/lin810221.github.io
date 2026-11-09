# MET與耗能估計：gross、net與適用範圍

用標準成人MET驗算，同時保留估計、年齡和活動體系的差別。

## 標準不是個人量測

成人Compendium的標準MET使用3.5mL O₂/kg/min作基準，2024成人資料主要適用19–59歲；高齡與輪椅體系另有基準。不能因都寫MET就跨體系無聲套同一換算。

$$
E_{gross}\approx MET\times3.5\times m\times t/200
$$

## 公式假設

m為kg、t為分鐘，使用約5kcal/L氧的教學轉換。假設5MET、60kg、30min，gross約157.5kcal；扣標準1MET休息背景後約126kcal。它不是把實測個人休息代謝扣掉，也未涵蓋全部誤差。

## 不能當吃回配額

同活動的真實成本有個體、技術、環境和測量差異，穿戴數字也有模型限制。估出的kcal不精確等於脂肪減少，也不能自動生成某人可吃回多少或應減多少的配額。

## 缺資料怎麼辦

記活動類型、來源代碼、資料版次、MET體系和估計條件；未知就保留未知，不用最相近活動假裝實測。教材用明示5MET情境，不宣稱某個品牌或每位讀者的活動固定如此。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 12_met_arithmetic.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:12_met_arithmetic.py -->

## 練習與解答

**先自己判斷：** 157.5kcal能否當真人精準消耗並全部吃回？

<details><summary>展開理由與驗算</summary>

不能。它是標準模型與假設條件下的gross估計，與個人實測、總能量平衡及飲食規劃不同。

</details>

## 官方來源與研究

- [2024成人身體活動Compendium與年齡範圍](https://pacompendium.com/adult-compendium/)
- [Compendium：標準MET單位](https://pacompendium.com/unite-conversions/)
- [Compendium：高齡者不同的MET基準](https://pacompendium.com/older-adult-compendium/)
- [Compendium：輪椅活動資料體系](https://pacompendium.com/adult-wheelchair-users-compendium/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)

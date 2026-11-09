# 單位、能量與濃度：先把分母寫清楚

分清g、mg、μg、kcal、kJ、IU與百分比，避免千倍和重複計算錯誤。

## 質量換算

1g=1000mg，1mg=1000μg。程式以ug表示μg方便輸入；維生素標籤的IU是活性單位，不能建立一個所有營養素通用的IU到μg係數。維生素D可換，維生素A還需化學型態與來源。

## 能量與能量比例

kcal是食品常用能量單位，1kcal=4.184kJ；不是kg或「一大卡等於一千大卡」。E%是某來源能量/總能量，不是重量百分比。20g脂肪供180kcal，在2000kcal示例中為9E%，不是20%。

## 大項與子項

飽和/反式包含在總脂肪，糖包含在碳水，不能再各自加一份能量。膳食纖維與糖醇的能量處理依計算制度不同；本課能量函式明確使用排除纖維的可利用碳水，再另計纖維係數，避免雙算。

## 寫完再檢查

例如鈉400mg，不是鹽400g；用近似2.5倍換NaCl當量，約鹽1g。mL轉g還需密度，湯匙、杯、掌心也不是固定化驗質量。每次將食物量、組成基準和營養素單位寫在等式旁，可快速發現錯誤。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 03_units.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:03_units.py -->

## 練習與解答

**請先判斷：** 維生素D1000IU可轉25μg，因此維生素A1000IU也可轉25μg嗎？

<details><summary>展開計算與理由</summary>

不行。IU換算依營養素、化學型態和來源；維生素A還有RAE等條件。不得把某一營養素係數複製成通用換算器。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：維生素D](https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/)
- [NIH ODS：維生素A](https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/)
- [TFDA：食品營養標示指引手冊](https://www.fda.gov.tw/tc/includes/GetFile.ashx?cid=42305&id=f639057139719594572)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)

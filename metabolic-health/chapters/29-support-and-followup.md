# 讓預防計畫能持續：家庭、回顧與資源

用可行行動與回饋支持長期改變。

## 把目標變成行動

「改善代謝」太抽象；「工作日午餐多選一份可取得的蔬菜」較容易觀察。行動仍要因個人飲食、資源及醫療限制調整。本課不從合成資料決定每人該吃多少，而是示範把目的、行動、觀察與回顧分欄。

## 家庭支持不是監督

共同採買、讓環境方便選擇、分擔照顧責任，可能比責備有效。先詢問當事人想得到哪種協助，避免把每次吃飯或體重變化變成考核。可近性和心理負擔應是方案品質的一部分。

## 分開缺漏與失敗

沒有填寫某天活動，可能是忘記紀錄，不等於活動為零。程式把未填寫視為unknown，把明確的否保留為False；否則資料表會把「不知道」變成「沒有做」，帶出錯誤結論。

## 回顧而非自行診療

回顧可檢查行動是否負擔太高、資源是否足夠、是否有不適，再把檢驗與藥物問題帶回照護團隊。公費方案資格和實際追蹤計畫不同；本課不以一般代謝症候群定義自動判斷2026或2027計畫資格。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 15_prevention_program.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:15_prevention_program.py -->

## 練習與解答

**先自己判斷：** 問卷沒填睡眠欄，能否視為睡眠不良？

<details><summary>展開驗算與理由</summary>

不能。未填是資訊缺漏，睡眠不良是已觀察或評估的結果；資料結構應分開兩者，後續再詢問，而不是自動補成異常。

</details>

## 官方來源與研究

- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [2027才生效的代謝症候群計畫修正](https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=5002&pid=20463)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)

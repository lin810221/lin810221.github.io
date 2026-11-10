# 排錯：單位、缺漏、輸入與環境

遇到錯誤先找資料條件，不用編造合理數字。

## 執行環境

先在examples目錄執行，確認python版本。下載包保留核心模組與data資料夾，不要只複製單一編號腳本。程式沒有額外pip依賴；若本機預設python不同，可指定正式安裝的執行檔，但不要改全系統路徑來遷就一份範例。

## 輸入被拒絕時

NaN、無限值、布林冒充數字、負濃度、零分母和不支援單位都應明確失敗。不要為了讓程式通過把值改成正常；核對檢體、分析物、單位與原始報告，無法確認就保留未知。

## 平均變成未知

這常是資料不完整而非程式故障。完整窗口的移動平均遇缺漏不輸出值；血壓complete_mean有任一排定缺失就未知。available_mean仍可描述現有資料，但名稱和分母不能換成完整。

## 算出不合理值

HDL大於TC、血小板數量級錯誤、尿肌酸酐mg/L誤當g/L、ABV5誤作0.05，都是先查單位的線索。程式不把負LDL截成0、不將Lp(a)套固定係數，也不將CGM當實驗室診斷。

## 網頁與輸出

修改Markdown後需用專案建置指令更新內嵌資料；直接開HTML可離線閱讀。瀏覽器進度在本機保存，換瀏覽器不會自動同步。報告路徑已存在時換新名稱，不刪除不熟悉的目錄來消除錯誤。

## 練習與解答

**先自己判斷：** 報告拒絕覆寫既有資料夾，應直接刪掉那個資料夾嗎？

<details><summary>展開驗算與理由</summary>

先確認內容與用途；本課建議換新輸出名稱，不需要刪除既有資料。拒絕覆寫是刻意設計，不是應繞過的錯誤。

</details>

## 官方來源與研究

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [NGSP：HbA1c的IFCC主方程式](https://ngsp.org/ifccngsp.asp)
- [NIDDK：尿白蛋白肌酸酐比的單位](https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr)
- [AHA2026血脂臨床摘要：10／30年範圍](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/-/media/731B2098BB23427F9EA8EDDF98E08145.ashx)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)

# 排錯：單位、缺漏、輸入與環境

遇到錯誤先找資料條件，不用編造合理數字。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/47-report-artifacts.svg" target="_blank" rel="noopener" aria-label="放大：資料表、圖與來源應能互相核對"><img src="assets/figures/47-report-artifacts.svg" alt="三種產物代表資料、視覺與說明，並不表示可重現就已證明臨床真實、因果或個人診斷。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 47｜資料表、圖與來源應能互相核對</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>依單位、缺漏、輸入和方法逐項找可能錯誤，說明圖看起來平順或檔案成功產生，為何仍不保證問題定義正確。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.niddk.nih.gov/health-information/professionals/advanced-search/quick-reference-uacr-gfr">NIDDK：UACR與GFR的用途及單位</a> · <a href="https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test">NIDDK：A1C檢驗與紅血球背景</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

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

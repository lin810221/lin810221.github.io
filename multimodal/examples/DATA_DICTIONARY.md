# 合成資料字典與表示契約

## 固定fixture

| 檔案 | 性質 | 主要驗收 |
| --- | --- | --- |
| invoice.pdf | 兩頁數位PDF | 第1頁發票，第2頁左右欄說明 |
| scan.png | 第1頁以144 DPI渲染的RGB影像 | 真實PP-OCRv6推論 |
| scan.pdf | 只有影像的發票PDF | 原生文字為空，主專題拒絕猜值 |
| rotated.pdf | 同發票頁以90度rotation顯示 | 未旋轉座標與顯示變換 |
| form.pdf | AcroForm文字欄vendor | 值為Harbor Labs，和OCR不同來源 |
| tones.wav | 單聲道、16000Hz、16-bit、48000 frames | 3秒純音，不是語音 |
| transcript.json | 明列人工編寫origin | 兩段半開時間區間，不是ASR輸出 |
| timeline.gif | 四個合成影格，每格500ms | 2秒動畫，不是MP4解碼測試 |
| expected.json | 人工設計欄位真值 | 不以模型輸出自動當真值 |

## 發票

發票號DW-2026-001，日期2026-11-20，廠商Harbor Labs，幣別USD。Cable數量2、單價12.50、金額25.00；Adapter數量1、單價20.00、金額20.00。小計45.00、稅額2.25、總額47.25。標準化輸出為4500、225、4725整數美分；此fixture沒有折扣、運費或多幣別。

Terms包含Net 30，銀行資料明列未提供；不應以總額回答銀行帳號問題。demo@example.test是合成聯絡資料，用於指定文字redaction示範。所有內容由本課程式建立，沒有真實客戶或受版權保護的外部文件。

## 座標

IR使用未旋轉頁面的左上座標，單位point，page_index零起算。頁面尺寸612×792 point。words保存bbox、text、block和line。引用含document_sha256、page_index、bbox、quote；bbox必須正面積且落在該頁，quote需實際出現在該框文字中。144 DPI影像是1224×1584 pixel；不要把pixel框直接當point框。

## 時間

人工片段A從0到1500毫秒，B從1500到3000毫秒，包含起點、不含終點。GIF各格從0、500、1000、1500毫秒開始，總長2000毫秒。音訊與動畫是兩份獨立fixture，不假裝有已驗證的聲畫同步。

## 產物

版本由來源hash與recipe建立，包含source.pdf、invoice.json、pages.json、tables.json、page-0.png、review.html。manifest保存必要檔案集合、來源和recipe；current只指向通過驗證的版本。完整schema與例外條件以contracts和pipeline程式為準。

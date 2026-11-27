# AcroForm、checkbox與可見內容

數位欄位有結構，但仍需要確認實際顯示與語意。

## 欄位物件

互動PDF可帶field name、型別、目前值、預設值與顯示外觀。pypdf可讀出這些結構，和從頁面抽印刷文字是兩條不同路線。某些文件有階層欄名、重複widget、radio group或特殊匯出值，不能假設每個欄位都是普通字串。

## 外觀可能不同步

欄位值和畫面外觀有時不一致，或需要重新產生appearance。checkbox也可能以自訂名稱表示勾選，不能只看是否非空。表單驗收應比較物件值、可見狀態與欄位定義；PDF數位簽章則需要另一套簽章與信任驗證。

## 本課實作

合成form fixture有vendor文字欄位，程式讀出Harbor Labs，讓讀者看到和OCR配對不同的資料來源。這個測試不代表XFA、所有互動控制或簽章都已支援。輸入類型應先分流，必要時保留物件與原頁雙重證據。

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大AcroForm、checkbox與可見內容示意圖"><img src="assets/figures/12.svg" alt="比較視覺鍵值配對和PDF互動欄位，指出為何不能因為欄位物件有值，就省略可見頁面核對。" loading="lazy"></a><figcaption>數位簽章、checkbox與XFA不能直接當作普通文字框。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「AcroForm、checkbox與可見內容」讀圖：比較視覺鍵值配對和PDF互動欄位，指出為何不能因為欄位物件有值，就省略可見頁面核對。本單元請再回答：get_fields讀到欄位值，就一定和讀者看到的畫面相同嗎？</p></div>

## 自我檢查與解析

**問題：**get_fields讀到欄位值，就一定和讀者看到的畫面相同嗎？

<details><summary>展開解析</summary><p>不一定。表單值和appearance可能不同步，勾選欄也可能用特殊狀態名稱。應核對欄位型別、語意與實際渲染。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab12.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab12.py -->

## 官方與原始來源

[本單元對應來源](https://pypdf.readthedocs.io/en/stable/user/forms.html)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。

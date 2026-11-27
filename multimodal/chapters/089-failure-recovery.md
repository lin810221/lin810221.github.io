# 故障注入、重跑與損壞處理

先證明失敗後能回到一致狀態，再談自動化。

## 指定中斷點

本課在產物與manifest完成、current替換前注入例外。此時沒有新公開指標，版本產物可供下次驗證重用。移除故障旗標重跑，程式核對來源與recipe，重新驗證檔案和引用，再完成切換，不重複建立另一份相同版本。

## 損壞不自動掩蓋

若invoice或其他產物被修改，雜湊檢查會拒絕；若路徑或必要檔案集合不符合，也停止。程式不在讀取失敗時偷偷重建並宣稱原版本一直正常。保留診斷後，由操作手冊決定重建或還原，來源與錯誤紀錄都維持可追溯。

## 鎖與硬中斷

一般例外會清理自己的writer lock，程序被強制終止可能留下鎖。先確認該workspace沒有仍在執行的寫入者，再按手冊處理殘留；不能只看鎖很舊就刪除。斷電持久性與遠端多寫入者要另外驗收。

## 操作步驟

```powershell
python pipeline.py --input data/invoice.pdf --workspace .runtime/harbor --fault after_artifacts
python pipeline.py --input data/invoice.pdf --workspace .runtime/harbor
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/30.svg" target="_blank" rel="noopener" aria-label="放大故障注入、重跑與損壞處理示意圖"><img src="assets/figures/30.svg" alt="在manifest已驗證但current尚未替換時中斷，說明讀者仍看到舊狀態以及重跑如何完成切換。" loading="lazy"></a><figcaption>原子替換是本機程序層的邊界，不等同跨服務或斷電保證。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「故障注入、重跑與損壞處理」讀圖：在manifest已驗證但current尚未替換時中斷，說明讀者仍看到舊狀態以及重跑如何完成切換。本單元請再回答：故障後同版本資料夾已存在，重跑可以直接信任它嗎？</p></div>

## 自我檢查與解析

**問題：**故障後同版本資料夾已存在，重跑可以直接信任它嗎？

<details><summary>展開解析</summary><p>不能。要重新核對manifest、必要檔案、雜湊、來源與引用，確認完整後才能切換；存在不等於正確。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab30.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab30.py -->

## 官方與原始來源

[本單元對應來源](https://docs.python.org/3.14/library/os.html#os.replace)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。

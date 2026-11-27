# 驗證紀錄

日期：2026-11-27（Asia/Taipei）。本機Windows CPU、Python3.14.10可攜隔離環境。套件：PyMuPDF2.2、pypdf7.2.0、Pillow13.0.0、Pydantic2.14.4、RapidOCR3.10.0、ONNX Runtime1.32.0。完整33依賴版本保存在requirements-lock。

## 相容性已實際檢查

Python3.15.2環境無法解析最新PyMuPDF2.2的依賴，原因是ONNX Runtime1.32.0沒有CPython3.15 wheel。本課改用受支援3.14分支的最新修補版3.14.10，並維持當日穩定的文件處理套件。官方變更紀錄和PyPI上傳日期可能不同，版本索引保留各自來源，不把查核日期當發布日期。

## 已執行

58個unittest通過，包括所有32個入口、真實PDF與pypdf文字對照、框線表格、AcroForm、文字redaction、嚴格schema、金額、來源區域引用、幾何與指標、租戶過濾、WAV／動畫GIF、不可變產物、重跑、指標前故障和損壞拒絕。全部入口在Python HTTP請求被封鎖的測試下執行，沒有使用API金鑰。

RapidOCR使用隨3.10.0 wheel提供的PP-OCRv6_det_small、PP-OCRv6_rec_small與ch_ppocr_mobile_v2.0_cls_mobile，實際在合成英文發票上辨識出總額47.25，並輸出22個文字區域。本次模型SHA-256列在學習包versions.json；分數不是校準正確率，不把這一張樣本推成繁中或所有版型的準確度。

DocWeave確實輸出原始PDF、頁面IR、表格、4725美分總額、區域quote、PNG疊框預覽與manifest。主線是固定數位發票規則，不是VLM推論；掃描可跑OCR，但不通過相同契約前不自動發布。

## API契約與未執行項目

OpenAI Responses、Gemini穩定Interactions v1、Claude Messages依當日官方文件建構請求並離線測試。沒有呼叫正式付費API、選擇或測試使用者帳號模型，也沒有上傳真實文件。輸出完成、拒答、截斷與schema解析有本地契約測試，服務端行為仍需實際驗收。

手工向量只演算cosine、對比損失與MaxSim，沒有訓練CLIP或下載大型VLM。逐字稿明列人工fixture，WAV為純音，未跑ASR。動畫GIF確實解碼，但MP4、聲畫同步、GPU、容器、雲端、多使用者覆核與正式安全稽核未執行。網頁DOM、SVG預覽與真實瀏覽器版面分開記錄。

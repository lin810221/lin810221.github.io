# 官方來源、原始論文與查核範圍

查核日2026-11-27（Asia/Taipei）。當日軟體穩定版和經典研究年份分開；查核不表示所有引用平台都已部署。每個單元另附對應來源。

## Python3.14.10

[Python3.14.10](https://www.python.org/downloads/release/python-31410/)：相容分支的最新修補版；不是把3.14稱為最新主線。

## PyMuPDF版本

[PyMuPDF版本](https://pymupdf.readthedocs.io/en/latest/changes.html)：2.2變更與來源日期。

## PyMuPDF安裝

[PyMuPDF安裝](https://pymupdf.readthedocs.io/en/latest/installation.html)：ONNX Runtime與Python ABI相容性。

## pypdf

[pypdf](https://pypi.org/pypi/pypdf/json)：7.2.0套件中繼資料。

## Pillow

[Pillow](https://pypi.org/pypi/pillow/json)：13.0.0版本。

## Pydantic

[Pydantic](https://pypi.org/pypi/pydantic/json)：2.14.4版本。

## RapidOCR

[RapidOCR](https://pypi.org/pypi/rapidocr/json)：3.10.0與實際安裝套件。

## ONNX Runtime

[ONNX Runtime](https://pypi.org/pypi/onnxruntime/json)：1.32.0與可用wheel。

## PDF文字

[PDF文字](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)：原生文字與OCR差異。

## PDF頁面

[PDF頁面](https://pymupdf.readthedocs.io/en/latest/page.html)：座標、表格、渲染與redaction。

## AcroForm

[AcroForm](https://pypdf.readthedocs.io/en/stable/user/forms.html)：表單與可見內容。

## RapidOCR參數

[RapidOCR參數](https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/parameters/)：偵測、辨識、模型與資源。

## OCR整合

[OCR整合](https://pymupdf.readthedocs.io/en/latest/ocr/index.html)：不同OCR路線與模型條件。

## 嚴格驗證

[嚴格驗證](https://docs.pydantic.dev/latest/concepts/strict_mode/)：轉型與JSON差異。

## CLIP原論文

[CLIP原論文](https://arxiv.org/abs/2103.00020)：2021圖文對比學習，不是當日新模型。

## LayoutLMv3原論文

[LayoutLMv3原論文](https://arxiv.org/abs/2204.08387)：2022文字、版面與影像預訓練。

## Donut原論文

[Donut原論文](https://arxiv.org/abs/2111.15664)：OCR-free研究。

## LLaVA原論文

[LLaVA原論文](https://arxiv.org/abs/2304.08485)：視覺指令學習與架構概念。

## ColPali原論文

[ColPali原論文](https://arxiv.org/abs/2407.01449)：視覺文件檢索與late interaction。

## DocVQA原論文

[DocVQA原論文](https://arxiv.org/abs/2007.00398)：文件影像問答與評估脈絡。

## 信心校準

[信心校準](https://arxiv.org/abs/1706.04599)：分數與正確頻率的區別。

## OpenAI文件輸入

[OpenAI文件輸入](https://developers.openai.com/api/docs/guides/file-inputs)：Responses文件內容。

## OpenAI結構化

[OpenAI結構化](https://developers.openai.com/api/docs/guides/structured-outputs)：格式、拒答與schema限制。

## Gemini文件

[Gemini文件](https://aistudio.google.com/docs/document-processing)：文件內容與處理選項。

## Gemini穩定v1

[Gemini穩定v1](https://aistudio.google.com/api-reference/interactions-api?api-version=v1)：穩定Interactions契約；beta另有revision。

## Gemini結構化

[Gemini結構化](https://aistudio.google.com/docs/structured-output)：response_format。

## Claude PDF

[Claude PDF](https://platform.claude.com/docs/en/build-with-claude/pdf-support)：Messages document來源。

## Claude結構化

[Claude結構化](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)：output_config.format與citations相容限制。

## WAV

[WAV](https://docs.python.org/3.14/library/wave.html)：實際音訊frame與時間。

## GIF

[GIF](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif)：動畫影格和duration。

## FFmpeg

[FFmpeg](https://ffmpeg.org/ffmpeg.html)：選用真實影片路線，未在本次執行。

## Whisper

[Whisper](https://huggingface.co/docs/transformers/main/en/model_doc/whisper)：選用ASR路線，未在本次執行。

## RRF原始論文

[RRF原始論文](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)：2009排名融合定義與常數；不以個別實驗承諾所有任務改善。

## 執行邊界

真實PDF、OCR、表格、表單、redaction、WAV、GIF與DocWeave已本機執行。付費API只有契約測試；大型VLM、語意頁面embedding、ASR、MP4、GPU與雲端未代跑。

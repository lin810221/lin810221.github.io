# 不可變版本、manifest與目前指標

把資料產生和讀者可見的切換分成兩個明確步驟。

## 版本內容

由來源hash與recipe決定版本識別，資料夾保存source、invoice、pages、tables、review與原頁PNG。manifest記錄每個必要檔案的SHA-256，以及來源與recipe。這些檔案構成一個一致產物，不能讓讀者自行掃資料夾挑最新檔名。

## 發布順序

先寫產物，再驗證schema、引用、來源和雜湊，完成manifest後才原子替換current。讀者跟著current取得一個版本。單機writer lock避免同一workspace的同時寫入；它不是跨主機租約，也不會依時間自動刪除可能仍有效的鎖。

## 完整性與權限

讀回時檢查版本格式、必要檔案集合、路徑和雜湊，再重新驗證來源及引用。正式存放私人文件還需檔案權限和存取層；manifest本身不是授權機制。本課本機替換處理程序層中斷，不宣稱已驗證斷電、遠端儲存或分散式一致性。

## 完整專案中的實作

以下節錄 `examples/pipeline.py` 的 `process`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def process(source,workspace,fault=None):
    source=Path(source);root=Path(workspace).resolve();document=inspect_pdf(source)
    page=document['pages'][0]
    if page['width']*page['height']*(RECIPE['render_dpi']/72)**2>8_000_000:raise ValueError('Rendered page exceeds pixel budget')
    version=digest(canonical({'document':document['sha256'],'recipe':RECIPE}))[:24]
    with writer_lock(root):
        folder=root/'versions'/version;folder.mkdir(parents=True,exist_ok=True);manifest_path=folder/'manifest.json'
        if manifest_path.exists():
            manifest=json.loads(manifest_path.read_bytes());verify_version(root,manifest)
            if manifest['document_sha256']!=document['sha256'] or manifest['recipe']!=RECIPE:raise ValueError('Cached recipe mismatch')
        else:
            invoice,tables=extract(source,document)
            (folder/'source.pdf').write_bytes(source.read_bytes());(folder/'invoice.json').write_bytes(canonical(invoice));(folder/'pages.json').write_bytes(canonical(document));(folder/'tables.json').write_bytes(canonical(tables))
            with pymupdf.open(source) as doc:
                pix=doc[0].get_pixmap(dpi=RECIPE['render_dpi'],alpha=False);pix.save(folder/'page-0.png')
            highlights=''.join(f'<rect x="{e["bbox"][0]}" y="{e["bbox"][1]}" width="{e["bbox"][2]-e["bbox"][0]}" height="{e["bbox"][3]-e["bbox"][1]}" fill="none" stroke="#9b1c31"><title>{html.escape(k)}</title></rect>' for k,e in invoice['evidence'].items())
            review=f'<!doctype html><html lang="en"><meta charset="utf-8"><title>DocWeave evidence review</title><style>body{{font:18px system-ui;background:#101713;color:#e5eee8;margin:30px}}svg{{max-width:700px;width:100%;background:white}}pre{{white-space:pre-wrap}}</style><h1>Synthetic invoice: evidence review</h1><p>Rule-based extraction; no VLM inference. Red outlines identify cited regions on page 1.</p><svg viewBox="0 0 612 792" role="img" aria-label="Invoice with extracted field regions"><image href="page-0.png" width="612" height="792"/>{highlights}</svg><pre>{html.escape(json.dumps(invoice,ensure_ascii=False,indent=2))}</pre><a href="source.pdf">Immutable source PDF</a></html>'
            (folder/'review.html').write_text(review,encoding='utf-8')
            names=['source.pdf','invoice.json','pages.json','tables.json','review.html','page-0.png']
            manifest={'version':version,'document_sha256':document['sha256'],'recipe':RECIPE,'files':{n:digest((folder/n).read_bytes()) for n in names}}
            atomic_json(manifest_path,manifest);verify_version(root,manifest)
        if fault=='after_artifacts':raise RuntimeError('Injected failure before current pointer')
        atomic_json(root/'current.json',manifest)
        return manifest
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/30.svg" target="_blank" rel="noopener" aria-label="放大不可變版本、manifest與目前指標示意圖"><img src="assets/figures/30.svg" alt="在manifest已驗證但current尚未替換時中斷，說明讀者仍看到舊狀態以及重跑如何完成切換。" loading="lazy"></a><figcaption>原子替換是本機程序層的邊界，不等同跨服務或斷電保證。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「不可變版本、manifest與目前指標」讀圖：在manifest已驗證但current尚未替換時中斷，說明讀者仍看到舊狀態以及重跑如何完成切換。本單元請再回答：產物已寫到versions目錄但current還沒切換，讀者應讀哪一個版本？</p></div>

## 自我檢查與解析

**問題：**產物已寫到versions目錄但current還沒切換，讀者應讀哪一個版本？

<details><summary>展開解析</summary><p>應依目前指標，不能掃目錄猜最新。版本資料夾存在不代表已完成發布；這個區別讓中斷後仍可恢復。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab30.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab30.py -->

## 官方與原始來源

[本單元對應來源](https://docs.python.org/3.14/library/os.html#os.replace)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。

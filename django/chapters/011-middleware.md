# Middleware的順序與責任

請求向內、回應向外，順序會影響可用資訊。

## 進入與返回路徑

Middleware包住後面的處理。請求依設定順序向內傳，回應反向經過；某一層可提前回應，後面的View不一定被執行。SessionMiddleware需先於需要session的認證層，不能任意依字母重排。

StudyHub有request ID middleware，為每次回應附可追蹤識別；它不信任用戶任意提供的識別值，也不把密碼與完整附件寫進日誌。request ID幫你連接事件，並不直接指出錯誤原因。

## 延遲分項的定義

若在同步、無重疊計時下，把總耗時拆成不重複的middleware、View、資料庫與呈現時間，可寫成

$$
T_{total}=T_{middleware}+T_{view}+T_{db}+T_{render}.
$$

例如四項分別為 $2,3,10,5$ 毫秒，總計 $20$ 毫秒。View計時若已包含資料庫，就不能再相加一次；非同步重疊工作也不能直接套用此分解。先定義量測邊界，再談優化。

## 專案中的實作

以下節錄 `examples/desk/middleware.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
import uuid
class RequestIDMiddleware:
    def __init__(self,get_response):self.get_response=get_response
    def __call__(self,request):
        request.request_id=uuid.uuid4().hex
        response=self.get_response(request);response['X-Request-ID']=request.request_id
        return response
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大Middleware的順序與責任圖解"><img src="assets/figures/04.svg" alt="Middleware的順序與責任：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Middleware的順序與責任」讀圖：依序讀middleware進入與返回路徑，指出本單元的檢查點。再回答：把View總耗時與其中資料庫耗時相加，會有什麼問題？</p></div>

## 自我檢查與解析

**題目：**把View總耗時與其中資料庫耗時相加，會有什麼問題？

<details><summary>展開解析</summary><p>重複計算。需要互不重疊的分項或清楚的包含關係，才能解釋延遲來源。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 03_request_response.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:03_request_response.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/http/middleware/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。

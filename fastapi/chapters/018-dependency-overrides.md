# 測試替換依賴與 app factory

以明確替換縮小測試範圍，同時保留真實認證測試。

## 替換在邊界上進行

`app.dependency_overrides[principal]`可以提供固定測試身分，讓某個測試只關注路由或序列化。測試結束要在finally清除；否則下一個本來應該401的案例可能被偷偷放行。

## factory提供隔離

每個測試透過create_app建立自己的app.state、設定與資料庫路徑，不把全域client或使用者留在模組。多個app同時存在時也不互相覆寫，方便並行測試和不同部署設定。

## 不用替換繞過必要驗收

如果所有測試都override principal，就無法證明真實token查找、撤銷、角色或租戶隔離有效。本課另有實際隨機token與資料庫測試；mock的價值在於明確界定測試目標，而不是降低安全行為的覆蓋。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `editor`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def editor(user: Annotated[dict, Depends(principal)]):
    if user['role'] != 'editor':
        raise DomainError(403, 'write_forbidden')
    return user
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大測試替換依賴與 app factory圖解"><img src="assets/figures/06.svg" alt="function scope在串流前關閉，request scope在回應後關閉。" loading="lazy"></a><figcaption>yield 依賴的清理時機。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「測試替換依賴與 app factory」讀圖：指出在第一個chunk前關閉資源時，哪些後續操作會失效。再用本節的條件回答：為何override成功不能當作認證通過？</p></div>

## 自我檢查與解析

**問題：**為何override成功不能當作認證通過？

<details><summary>展開解析</summary><p>因為測試刻意替換了認證。需要另一組不替換依賴的測試來驗證真實憑證、撤銷和權限。</p></details>

## 執行與驗收

執行 `python lab03.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab03.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/testing-dependencies/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。

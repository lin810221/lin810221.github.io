# 測試依賴與 lifespan 隔離

在正確的邊界替換，並確認測試結束後狀態完全恢復。

## 使用context manager

`with TestClient(app)`執行lifespan，才能取得已建立的store與共享client。只建立client物件而不進入context，可能讓測試沒有經過正式啟動與關閉流程，掩蓋資源管理錯誤。

## 測試替換的清理

override principal後驗證目標行為，在finally清除，再送無憑證請求確認重新回401。每個測試建立新的app，而不是依賴先前測試留下的token或資料；執行順序改變不應影響結果。

## 不把測試捷徑帶到部署

測試身分不應成為環境變數開關，一旦設定就跳過正式認證。若需要開發便利，提供明確本機佈建命令和合成資料，而不是把所有使用者都當admin。發布前搜尋override與測試憑證是否只出現在測試路徑。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `principal`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def principal(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], store: Annotated[Store, Depends(get_store)]):
    if credentials is None or credentials.scheme.lower() != 'bearer' or len(credentials.credentials) > 512:
        raise DomainError(401, 'unauthorized')
    return store.identity(credentials.credentials)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大測試依賴與 lifespan 隔離圖解"><img src="assets/figures/23.svg" alt="純函式、ASGI、真實TCP、外部服務與正式環境有不同邊界。" loading="lazy"></a><figcaption>測試層次各自證明什麼。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「測試依賴與 lifespan 隔離」讀圖：替每一種測試寫出一個仍無法驗證的條件。再用本節的條件回答：為何清除override後還要再測一次401？</p></div>

## 自我檢查與解析

**問題：**為何清除override後還要再測一次401？

<details><summary>展開解析</summary><p>它證明替換沒有外洩到後續操作，能抓出忘記清理造成的假陽性。</p></details>

## 執行與驗收

執行 `python lab03.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab03.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/testing-dependencies/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。

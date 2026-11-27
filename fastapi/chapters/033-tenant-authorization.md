# 角色與租戶隔離：防止物件層越權

能猜到ID不是存取權，每次查詢都要保留授權條件。

## 身分、操作與資源三層

principal識別租戶和角色；editor決定可否新增或取消；store查詢用tenant與資源ID一起限制。reader能讀自己租戶資料，但不能建立文件或工作。這些規則即使ID看起來隨機也必須存在。

## 檢索前先套權限

本課selected只接受呼叫者租戶的文件ID，任何一筆不屬於自己就回404。不能先把全站文件送進模型，再從答案裡刪除他人引用；秘密此時已被傳送。錯誤回應也不要告知「這筆屬於哪個別的租戶」。

## 所有入口都要檢查

查工作、取消、事件回放、下載與背景worker都可能成為越權入口。SSE在送200前由依賴授權；游標只決定已授權工作內的續讀位置，不擴大權限。本課以不同租戶token測試文件、工作、事件和取消。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `selected`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def selected(self, tenant, identifiers):
        with Session(self.engine) as session:
            rows = list(session.scalars(select(Document).where(Document.tenant == tenant, Document.id.in_(identifiers), Document.deleted == 0).order_by(Document.id)))
            if len(rows) != len(identifiers):
                raise DomainError(404, 'document_not_found')
            return [self._document(row) for row in rows]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大角色與租戶隔離：防止物件層越權圖解"><img src="assets/figures/11.svg" alt="憑證映射租戶與角色，每次查詢加入租戶條件。" loading="lazy"></a><figcaption>認證與資源授權分開。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「角色與租戶隔離：防止物件層越權」讀圖：找出角色檢查與資源歸屬檢查各自的位置。再用本節的條件回答：UUID足夠長是否就不需要租戶條件？</p></div>

## 自我檢查與解析

**問題：**UUID足夠長是否就不需要租戶條件？

<details><summary>展開解析</summary><p>仍然需要。不可猜測性只降低發現機會，不能替代授權；ID也可能從紀錄、分享或其他漏洞取得。</p></details>

## 執行與驗收

執行 `python lab10.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab10.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/security/first-steps/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。

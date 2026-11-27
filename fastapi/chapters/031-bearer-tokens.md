# Bearer token、摘要保存與撤銷

先做好服務憑證的生命週期，再談更複雜的登入整合。

## 本課使用高熵不透明token

管理命令產生隨機token，只在佈建時輸出一次；資料庫保存SHA-256摘要、租戶和角色。每次請求將token摘要後查找。這種方法適用高熵隨機服務金鑰；不能直接拿快速SHA-256當成一般使用者密碼雜湊，密碼需要專用慢雜湊與政策。

## 撤銷是實際行為

刪除摘要後，新請求立即失去驗證資格。已建立串流或正在執行的工作則有自己的生命週期，本課沒有宣稱撤銷會瞬間終止所有現存連線。正式服務應定義token有效期、輪替、稽核與撤銷傳播範圍。

## 不放在URL或前端原始碼

URL可能進入瀏覽歷史、代理與存取紀錄；靜態網頁原始碼與下載包是公開資料。token只放在受保護的傳輸標頭，使用TLS；本機HTTP僅供回環練習。本課log不記錄Authorization或完整body。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `provision`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def provision(self, tenant, role='editor'):
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,31}', tenant) or role not in {'reader', 'editor'}:
            raise ValueError('invalid identity')
        token = secrets.token_urlsafe(32)
        with Session(self.engine) as session, session.begin():
            session.add(Credential(digest=digest(token), tenant=tenant, role=role))
        return token
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大Bearer token、摘要保存與撤銷圖解"><img src="assets/figures/11.svg" alt="憑證映射租戶與角色，每次查詢加入租戶條件。" loading="lazy"></a><figcaption>認證與資源授權分開。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Bearer token、摘要保存與撤銷」讀圖：找出角色檢查與資源歸屬檢查各自的位置。再用本節的條件回答：為何隨機API token能存SHA-256摘要，而使用者密碼不宜？</p></div>

## 自我檢查與解析

**問題：**為何隨機API token能存SHA-256摘要，而使用者密碼不宜？

<details><summary>展開解析</summary><p>高熵隨機token不依賴人類可猜測選擇；密碼容易遭離線字典攻擊，需專用慢雜湊。兩者的威脅模型不同。</p></details>

## 執行與驗收

執行 `python lab11.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab11.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/security/first-steps/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。

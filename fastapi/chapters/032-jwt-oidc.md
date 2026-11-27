# JWT、OAuth 與 OIDC 的正確分工

JWT是承載格式，OAuth是授權框架，OIDC提供登入身分層。

## 簽章不是加密

JWT payload常能被直接解碼，不要把秘密放進claims。驗證時固定允許的演算法，核對簽章、issuer、audience、有效期與必要claims；不能只base64解碼就相信sub，也不能讓token自行決定可接受演算法。

## 登入與API受眾不同

OIDC的ID token提供客戶端確認登入，API通常驗證給本API受眾的access token。現代互動登入應依身分服務採Authorization Code與PKCE，並核對redirect URI、state或nonce等相應機制；本課不把教學用password flow包裝成現代正式登入方案。

## 本課驗證範圍

security.py以隨機本機HS256 key驗證JWT，測試錯受眾、錯issuer、過期與錯演算法；它不是完整OIDC客戶端，也沒有部署身份提供者。正式非對稱驗證還需受信任JWKS來源、key輪替、快取與失敗政策。

## 對照完整專案

以下節錄 `gateway/security.py` 的 `decode_access_token`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def decode_access_token(token, key, *, issuer='https://issuer.example.test', audience='relaydesk'):
    if len(key) < 32:
        raise ValueError('teaching HS256 secret must contain at least 32 bytes')
    claims = jwt.decode(token, key, algorithms=['HS256'], audience=audience, issuer=issuer, options={'require': ['exp', 'iat', 'sub', 'iss', 'aud']})
    if not isinstance(claims['sub'], str) or not claims['sub'].strip():
        raise ValueError('invalid subject')
    return claims
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大JWT、OAuth 與 OIDC 的正確分工圖解"><img src="assets/figures/12.svg" alt="OIDC登入與API接受的access token有不同用途。" loading="lazy"></a><figcaption>外部身分服務與本地 API。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「JWT、OAuth 與 OIDC 的正確分工」讀圖：分辨登入結果、API受眾與資料擁有者三種身分關係。再用本節的條件回答：拿到合法簽章的ID token，就能讓它呼叫任意API嗎？</p></div>

## 自我檢查與解析

**問題：**拿到合法簽章的ID token，就能讓它呼叫任意API嗎？

<details><summary>展開解析</summary><p>不能。要核對token用途與audience，API只接受為自己受眾發出的合適access token，還要執行資源授權。</p></details>

## 執行與驗收

執行 `python lab26.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab26.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.rfc-editor.org/rfc/rfc9700.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。

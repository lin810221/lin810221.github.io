# 正式設定、DEBUG與安全檢查

檢查工具能找部分問題，不能替你確認整個環境。

## 必要環境值

正式模組關閉DEBUG，要求由環境提供夠長的密鑰與明確ALLOWED_HOSTS，並啟用適合HTTPS的cookie與轉向設定。不要將開發密鑰或測試雜湊器沿用到公開網站。

```powershell
python manage.py check --deploy --settings=studyhub.production
```

此命令需在正式環境值齊全時執行，並閱讀警告。沒有HTTP錯誤不代表TLS、DNS、反向代理與備份都已驗證；執行報告必須說明設定模組。

## HSTS、代理與CSP的條件

只有確認所有相關子網域都支援HTTPS後，才考慮對應HSTS範圍與preload。代理轉送標頭也只能信任已配置的可信代理，不能因為一行設定能修好網址就無條件開啟。

本課保留保守的子網域及preload選項，check可能提醒需要按實際網域決策。CSP可先以報告模式觀察再收緊；正式規則需用實際頁面驗證，不以一個標頭宣稱全部防護完成。

## 專案中的實作

以下節錄 `examples/studyhub/production.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
"""Deployment template. No live service or PostgreSQL is provisioned by this file."""
from .settings import *
from django.core.exceptions import ImproperlyConfigured
SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY','')
if len(SECRET_KEY)<50 or len(set(SECRET_KEY))<8:raise ImproperlyConfigured('Set a strong DJANGO_SECRET_KEY in the runtime environment')
DEBUG=False
ALLOWED_HOSTS=[x.strip() for x in os.environ.get('DJANGO_ALLOWED_HOSTS','').split(',') if x.strip()]
if not ALLOWED_HOSTS:raise ImproperlyConfigured('Set explicit DJANGO_ALLOWED_HOSTS')
SECURE_SSL_REDIRECT=True;SESSION_COOKIE_SECURE=True;CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=3600;SECURE_HSTS_INCLUDE_SUBDOMAINS=False;SECURE_HSTS_PRELOAD=False
SECURE_CONTENT_TYPE_NOSNIFF=True;X_FRAME_OPTIONS='DENY'
STORAGES={**STORAGES,'staticfiles':{'BACKEND':'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
if os.environ.get('POSTGRES_DB'):
    DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.environ['POSTGRES_DB'],
        'USER':os.environ['POSTGRES_USER'],'PASSWORD':os.environ['POSTGRES_PASSWORD'],
        'HOST':os.environ['POSTGRES_HOST'],'PORT':os.environ.get('POSTGRES_PORT','5432'),
        'CONN_MAX_AGE':60,'OPTIONS':{'sslmode':os.environ.get('POSTGRES_SSLMODE','require')}}}
# Do not blindly trust forwarded headers. Configure the known reverse proxy separately.
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大正式設定、DEBUG與安全檢查圖解"><img src="assets/figures/23.svg" alt="正式設定、DEBUG與安全檢查：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「正式設定、DEBUG與安全檢查」讀圖：沿反向代理、WSGI及資料庫追蹤請求，指出各服務的責任。再回答：check --deploy沒有ERROR，就能宣稱正式網站安全完成嗎？</p></div>

## 自我檢查與解析

**題目：**check --deploy沒有ERROR，就能宣稱正式網站安全完成嗎？

<details><summary>展開解析</summary><p>不能。它是部分自動檢查，還需處理警告並驗證實際TLS、代理、權限、資料與維運。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。

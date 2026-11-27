# Django完整實作：StudyHub

查核：2026-11-26。Python3.15.2、Django6.1.3、DRF3.18.3；完整鎖版見requirements-lock.txt。

## 第一次啟動

在本資料夾執行：

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo --username 你建立的帳號
python manage.py runserver 127.0.0.1:8000
```

若無法啟動PowerShell腳本，可直接用`.venv\Scripts\python.exe`取代python。Linux與macOS用python3建立環境，啟動`.venv/bin/activate`。第一次安裝相依需網路，其後核心練習不連外部服務。

網站提供任務CRUD、登入、註冊、密碼重設本地郵件、私人UTF-8文字附件、Admin與REST API。沒有共用預設密碼。`seed_demo`只加入既有帳號的合成任務，不建立帳號或重設密碼。

## 測試與24個獨立入口

```powershell
python -m unittest -v test_examples.py
python manage.py test desk --settings=studyhub.testing
python 01_environment.py
python 14_ownership.py
python 21_tasks.py
python 24_fetch_mode.py
```

獨立入口使用記憶體SQLite與合成資料；完整網站預設資料保存於db.sqlite3。不要將私人資料庫、private-media、密鑰或環境檔加入公開repo。

01–06：環境、路由、回應、跳脫、關係、DB約束。07–12：QuerySet、額外查詢、聚合、交易、表單與PRG。13–18：Session、owner、CSRF、私人附件及API。19–24：分頁、快取、Tasks、冪等、async與6.1 fetch modes。

## 正式環境支線

`studyhub.production`要求由程序環境提供強密鑰及明確hosts，關閉DEBUG；本程式不自動讀.env。環境值參考`environment.example`，密鑰應由你的作業系統或平台注入。

```powershell
python manage.py check --deploy --settings=studyhub.production
python manage.py collectstatic --noinput --settings=studyhub.production
waitress-serve --listen=127.0.0.1:8000 studyhub.wsgi:application
```

啟動正式模組前，需設定DJANGO_SETTINGS_MODULE；HTTPS與可信代理按真實環境配置。HSTS子網域與preload保留保守設定，部署檢查的相關警告需依你控制的網域決定，不能直接忽略。

PostgreSQL可選相依在requirements-postgres.txt，另需資料庫服務與POSTGRES環境值；migrate不會自動搬移SQLite資料。外部郵件、共享快取、真正queue與worker也需各自整合驗收。ImmediateBackend在同程序立即執行，不是背景程序。

## 部署與教材的差別

GitHub Pages可以提供本課的靜態教材，不能執行此Django專案。動態網站需Python服務與保存資料的位置。runserver是開發工具，不是正式服務器。驗證範圍與尚未測試項目見VERIFICATION.md。

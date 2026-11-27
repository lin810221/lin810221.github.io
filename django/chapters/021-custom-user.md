# 在第一個migration前決定User

可擴充帳號模型的決策要及早做。

## 使用AbstractUser起步

本課User繼承AbstractUser，保留Django既有帳號與密碼能力，只增加顯示名稱。設定 `AUTH_USER_MODEL='desk.User'`，其他模型透過 `settings.AUTH_USER_MODEL` 建立關聯，執行時用 `get_user_model()` 取得模型。

這個決策應在第一次建立migration與套用資料庫之前完成。已經有使用者與關聯資料後更換User，涉及schema、外鍵、migration依賴與資料搬移，不是改一行設定就結束。

## 不自行重寫密碼系統

使用 `create_user`、UserCreationForm與內建登入流程，避免把明文密碼存進CharField。密碼雜湊、登入session、重設token與權限是相關但不同元件；自訂User不表示需要全部重寫。

本課測試設定為加速使用較快的雜湊器，正式設定保留框架預設安全策略。不要把測試環境的速度選擇直接複製到正式網站，版本與環境都要清楚標記。

## 專案中的實作

以下節錄 `examples/desk/models.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
class User(AbstractUser):
    display_name=models.CharField('顯示名稱',max_length=60,blank=True)
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大在第一個migration前決定User圖解"><img src="assets/figures/07.svg" alt="在第一個migration前決定User：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「在第一個migration前決定User」讀圖：數清楚一對多與多對多的方向，指出外鍵與中介表的角色。再回答：已經migrate並有真實帳號後，能直接修改AUTH_USER_MODEL嗎？</p></div>

## 自我檢查與解析

**題目：**已經migrate並有真實帳號後，能直接修改AUTH_USER_MODEL嗎？

<details><summary>展開解析</summary><p>不能只改設定。需規劃完整migration與資料搬移，先備份並在副本驗證；新專案則應先決定User再開始。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/auth/customizing/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。

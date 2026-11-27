# 備份、還原與恢復目標

有備份檔不代表能還原，也不代表符合容許的資料損失。

## 先定義目標

RPO描述可接受的資料損失時間範圍，RTO描述恢復服務所需時間目標。它們不是備份頻率和某次copy成功的別名；要配合工作、事件、文件與秘密的實際保存位置定義。

## 一致性快照

SQLite運作中可能涉及journal或WAL，不能只任意複製一個檔案就宣稱一致備份。使用資料庫支援的backup方式或經驗證的停機流程，還原到新位置，執行schema與資料完整性檢查，再以API讀取工作和事件。

## 演練恢復而不是只寫文件

本課的當機恢復測試重開同一資料庫，沒有冒稱已完成備份平台。正式應定期將備份還原至隔離環境，核對資料、ACL、模型配方與秘密輪替；加密備份也要確保解密能力在事故時可取得。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `job`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def job(self, tenant, identifier):
        with Session(self.engine) as session:
            row = session.scalar(select(Job).where(Job.id == identifier, Job.tenant == tenant))
            if row is None:
                raise DomainError(404, 'job_not_found')
            return self._job(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大備份、還原與恢復目標圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「備份、還原與恢復目標」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：看到每天都產生備份檔，能直接宣稱RTO達標嗎？</p></div>

## 自我檢查與解析

**問題：**看到每天都產生備份檔，能直接宣稱RTO達標嗎？

<details><summary>展開解析</summary><p>不能。需要實際還原與服務恢復演練，量測耗時並核對完整性；檔案存在只證明有輸出。</p></details>

## 執行與驗收

執行 `python lab29.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab29.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。

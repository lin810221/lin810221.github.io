# 經濟學 · 可獨立執行實驗

42個Python入口、4個共用模組、3份虛構資料/metadata及86項數值與資料驗收。**僅標準函式庫，不需pip、API key或網路。** 閱讀網站也不需安裝Python。

## 版本與開始方式

2026-11-09查核正式穩定版 **Python 3.15.2**，本機實測Windows x64官方可攜版，已核對官方SHA-256；一般使用者可安裝官方標準版。程式也避免依賴第三方套件版本。

```powershell
py -3.15 --version
cd economics/examples
py -3.15 04_supply_and_demand.py
py -3.15 33_is_mp_pc.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 42_policy_report.py --output my-report
```

macOS/Linux可使用自己的`python3.15`命令；ZIP解壓後在`examples`內執行。沒有`--output`時，交付程式使用暫存目錄並清理；指定的目錄必須不存在，避免覆蓋既有資料。

## 檔案與實驗

| 入口 | 主要觀察 |
|---|---|
| `01_opportunity_cost.py` | 生產可能邊界與機會成本 |
| `02_ppf_and_models.py` | 可行集合、斜率與效率 |
| `03_units_and_rates.py` | 百分比與百分點 |
| `04_supply_and_demand.py` | 競爭均衡與位移 |
| `05_elasticity.py` | 中點法與反向對照 |
| `06_tax_and_controls.py` | 稅楔、無交易、價格上/下限 |
| `07_consumer_budget.py` | Cobb–Douglas需求與預算 |
| `08_hicks_decomposition.py` | 固定效用的所得/替代分解 |
| `09_labor_leisure.py` | 工作、休閒與角點 |
| `10_production.py` | 生產函數、MP與Euler關係 |
| `11_cost_curves.py` | 固定/變動/邊際成本 |
| `12_competition_and_exit.py` | 生產不等於獲正利潤 |
| `13_monopoly.py` | MR=MC與獨占福利 |
| `14_cournot.py` | 寡占數量與廠商數 |
| `15_games.py` | 純Nash、內部混合、平手 |
| `16_welfare.py` | CS、PS、稅收與DWL對帳 |
| `17_externalities.py` | 社會成本與Pigou稅 |
| `18_abatement.py` | 低成本減排與容量限制 |
| `19_labor_market.py` | 競爭勞動市場基準，非最低工資實證 |
| `20_insurance.py` | 期望log效用與保險 |
| `21_behavioral_discounting.py` | 指數/準雙曲權重 |
| `22_gdp_accounting.py` | 名目支出恆等與附加價值 |
| `23_price_indexes.py` | 定基實質、CPI與平減指數 |
| `24_labor_statistics.py` | 勞參退出與失業分母 |
| `25_growth_and_compounding.py` | CAGR、複利與倍增時間 |
| `26_solow_transition.py` | 精確離散遞推與穩態 |
| `27_growth_accounting.py` | 投入貢獻與非因果TFP殘差 |
| `28_bank_balance_sheet.py` | 貸款資產與存款負債同增 |
| `29_fisher_rates.py` | 名/實質率與近似誤差 |
| `30_bond_prices.py` | 固定現金流現值、duration |
| `31_ad_as.py` | 靜態需求/供給衝擊 |
| `32_multiplier.py` | 稅與進口漏出 |
| `33_is_mp_pc.py` | 三方程靜態政策模型 |
| `34_fiscal_scenarios.py` | 購買與定額減稅對照 |
| `35_debt_dynamics.py` | 淨債務比、名目利率/成長 |
| `36_policy_tradeoffs.py` | 通膨與缺口的供給衝擊取捨 |
| `37_comparative_advantage.py` | 機會成本、價格與交易量 |
| `38_tariff.py` | 小國關稅與禁止性邊界 |
| `39_exchange_and_bop.py` | 匯率報價、CIP與金融帳符號 |
| `40_evidence_and_identification.py` | OLS與四格DID算術/假設 |
| `41_data_vintages.py` | 以發布日作as-of選取 |
| `42_policy_report.py` | CSV、獨立SVG與JSON交付 |

共用模組：`microeconomics.py`、`macroeconomics.py`、`evidence.py`、`policy_report.py`。測試在`test_examples.py`。

## 單位與模型契約

- 供需、稅、獨占採明確線性逆需求/成本，價格為教學代幣、數量每期；無交易時價格回`None`，不創造負成交量。
- 價格管制剩餘採**有效率配給假設**，沒有模擬排隊/黑市；稅收入是移轉，不整筆當DWL。
- Cobb–Douglas是偏好特例，效用是序數，不能跨人比較或把數字倍數當幸福倍數。Hicks保持舊效用，與Slutsky有限變動補償不同。
- 2×2賽局保留平手純均衡，僅回孤立內部混合；沒有列出退化賽局全部連續混合均衡。
- Solow使用`(1+n)(1+g)`精確離散分母，所以replacement為`delta+n+g+n*g`。A為固定尺度，g為有效勞動技術成長。
- Fisher/折現/債務利率用小數（5%=.05）；**IS–MP–PC用百分點**（2%=2）。該模型預期外生、無動態學習、無有效下限；phi是事前實質利率對通膨的反應，名目率近似為r＋預期通膨。不能和另含當期通膨的名目Taylor係數直接對號。
- 銀行示範完整兩邊分錄，不用機械準備乘數。權益/貸款比只是100%風險權重教具，非完整法規資本比。
- 債務模型追**淨債務/GDP**，可為負表示淨資產；名目利率配名目成長，初級盈餘以當期GDP比，不含其他存量流量調整。
- FA定義為金融資產淨取得−負債淨發生，含準備資產，故`CA+KA-FA+SD=0`。不同來源另列準備或用不同符號時先對metadata。
- OLS/DID函式只示範估計算術，不提供完整標準誤或識別證明；不能拿模型情境當真實政策因果效果。

## 資料與最新統計口徑

`data/synthetic_basket.csv`、`synthetic_vintages.csv`及`metadata.json`均為虛構。年份不代表任何國家觀測，也沒有自動下載官方數列。

價格實驗是**固定基期教具**；官方chain-linked實質細項一般不可直接相加。2025 SNA／BPM7已發布，但各國實作處於過渡，資料必須標實際採用方法；不要將所有2026資料自動改標新標準。觀察期、發布日、修訂日與下載日分開，避免前視。

## 交付與驗收

`my-report`包含15組敏感度CSV、可獨立分享的`market.svg`、`report.json`（Python版本、資料hash、模型、檢查與限制）。改需求斜率也改原均衡，故情境名為flatter/steeper，是結構敏感度，非保持其他條件的純彈性實證比較。

86項測試涵蓋市場清算、稅負、福利、無交易、消費預算、Hicks分解、停工、MR=MC、賽局、Pigou、減排容量、風險、分配、貿易、國民帳、價格指數、勞動分母、Solow/黃金律、銀行、現值、三方程、債務、BOP符號、資料版本與SVG/JSON交付。這些驗證算術與契約，不會證明虛構模型已符合某國現實。

## 官方參考

[Python3.15.2](https://www.python.org/downloads/release/python-3152/) · [CORE Econ2.0](https://books.core-econ.org/the-economy/index.html) · [OpenStax3e](https://openstax.org/details/books/principles-economics-3e) · [2025統計標準](https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats) · [主計總處連鎖值](https://www.stat.gov.tw/News_Content.aspx?n=2679&s=103006) · [銀行貨幣創造](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy)

# 肌肉骨骼健康與人體工學：離線實作

本套範例把課程中的任務、單位、假設、缺漏和模型變成可核對的算術。共48個編號入口、80項測試、5份合成資料，**沒有真實員工、病人、影像或個人健康輸入**。閱讀網頁不用安裝Python。

## 第一次執行

1. 從[Python官方](https://www.python.org/downloads/)安裝正式版。本課於2026-11-13查核並以 **CPython 3.15.2** 執行；只用標準函式庫，不需pip、API Key、模型或連線。
2. 解壓整份`examples.zip`，保留`examples`中的核心、資料和測試，不能只取一個編號檔。
3. 在`examples`資料夾開啟終端機，依序執行：

```powershell
python --version
python 01_task_person_environment.py
python 07_external_moment.py
python 28_rnle_factors.py
python -m unittest discover -s . -p test_examples.py -v
python 48_complete_project.py --output my-ergo-report
```

Windows若`python`指向其他安裝，可用`py -3.15`取代。最後一行的`my-ergo-report`必須是**尚不存在的新資料夾**。前47個入口和第48個不加參數的預覽可直接依序執行；預覽使用臨時資料夾，結束會清理。需要保留成果，請使用`--output`。

也可從LearningNote根目錄驗證：

```powershell
py -3.15 -m unittest discover -s ergonomics/examples -p test_examples.py -v
py -3.15 ergonomics/examples/48_complete_project.py --output my-ergo-report
```

## 先不用程式也能學

每個閱讀單元都有原理解說、情境和練習解答；奇數單元附一份入口。先手算、預測或說出未知，再執行程式比對。文字輸出中的`None`和JSON的`null`表示未知或不適用，不能自動轉成0。

建議先跑07、08、17、28、35和48，分別看力矩、接觸面積、視線、搬抬、振動與報告。完整路線依編號01–48，對應16章各3個入口。

## 檔案與資料契約

| 檔案 | 一列／項的意義 | 必須保留的限制 |
| --- | --- | --- |
| `data/observations.csv` | 組裝A的12個排定10分鐘觀察窗 | B01–B12、有序；11段已知，最後一段未觀察；已知活動分鐘不超過觀察窗 |
| `data/workers.csv` | 12名虛構使用者的兩項尺寸 | 伸取能力、淨空需求單位cm；F11、F12各有一個未知；兩條條件同時成立才符合 |
| `data/lift_cases.json` | 近距離、遠距離、適用未知的三個搬抬案例 | 原始參數與適用狀態；未知FM不可填1；皆為教學假設 |
| `data/metadata.json` | 合成來源、用途與日期 | 不是研究、現場調查或病歷 |
| `data/references.json` | 方法版本與正式來源 | 網頁日期、正式方法修訂及地區範圍分開 |

所有觀察數據皆為合成。資料讀取器檢查識別碼、狀態和數值，空字串轉`None`；拒絕NaN、Infinity、負值、非整數動作數、矛盾觀察狀態，以及活動時間超過觀察窗。核心不把布林值當數字。

可用觀察110分鐘，共990次，因此**已觀察時段**頻率9次／分鐘；完整120分鐘的動作總量和頻率未知。尺寸已知10人中3人符合，另外2人未知；這不是人口代表性、完整適配或健康結果。

## 核心與單位

| 函式／模型 | 算式或結果 | 用途邊界 |
| --- | --- | --- |
| `mass_force` | kg×9.80665 → N | 指定重力假設的重量力，不是個人限重 |
| `moment` | F[N]×r[m]×sinθ → N·m | 外力矩大小，不是肌肉或關節內力 |
| `contact_pressure` | N÷(cm²×10⁻⁴)÷1000 → kPa | 假設均勻接觸，非局部峰值、神經或皮膚門檻 |
| `normal_stress` | N/mm² → MPa | 單軸材料模型，非人體組織實際受力 |
| `engineering_strain` | 長度變化／原長 | 無因次；不推傷害或個人活動限制 |
| `relaxation_analogy` | 平衡值＋差值×exp(−t/τ) | 任意時間與單位、未校準，不預測癒合或疲勞 |
| `view_geometry` | hypot、atan2 | 點到點距離與相對水平角，不是完美姿勢 |
| `angular_size` | 2 atan(h/2d) | 同單位幾何，不等於視力、CSS字級或處方 |
| `repetition` | 次數／觀察分鐘；活動分鐘／觀察分鐘 | 不是ART分數或RNLE完整頻率觀察程序 |
| `population_fit` | 兩條幾何條件的交集、已知樣本比例 | 不推人口覆蓋率、個人健康或全部功能 |
| `horizontal_work` | F×cosθ×d → J；J/s → W | 外功模型，非代謝熱量或安全推拉限力 |

## RNLE：只實作透明倍率算術

`rnle`使用metric公式`RWL=23×HM×VM×DM×AM×FM×CM`，負重/RWL為LI。條件不明、FM／CM未知時RWL與LI保留未知；RWL為0時LI無定義。**LI不是傷害機率，23kg不是通用或個人的法定限重。**

- H：內踝中點至手握點中點的地面投影距離；H≤25cm用25，H>63cm本課拒絕。不是腰椎到箱子的距離。
- V：手部距地高度0–175cm；VM=1−0.003|V−75|。
- D：起終端手部垂直高度的絕對差；D<25cm用25；D>175cm拒絕。DM=0.82+4.5/D。
- A：負重位置相對正中矢狀面的不對稱位置角0–135°；AM=1−0.0032A。不是脊柱扭轉角。
- FM與CM**由使用者依正式方法提供**，程式不內建完整查表或自動工時判定。範例FM=.94、CM=1對應明示的1次/分鐘、短工時、充分恢復及正式良好抓握等教學假設；有把手不自動等於良好。
- 2021更正短工時恢復需至少工作時間1.0倍，舊1.2倍是已更正誤字；這是分類條件，不是通用醫療休息處方。其他工時、連續工作及恢復安排需正式重判。
- 需顯著目的端控制時評兩端；多任務CLI不能平均LI。此核心不實作CLI、完整適用性稽核或所有頻率和抓握表。
- 不直接評單手、坐跪、推拉、不穩物體或搬人等不適用工作。`conditions_verified=True`只是案例聲明，沒有替你調查現場。

正式來源：[NIOSH入口](https://www.cdc.gov/niosh/ergonomics/about/rnle.html)、[2021修訂紀錄](https://stacks.cdc.gov/view/cdc/110725)、[94-110完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)。2026入口更新不代表公式改為2026新版。

## 振動與風險工具

HAV輸入必須已是正式頻率加權的三軸合成`a_hv`，與每段**實際觸發分鐘**。算式為`A(8)=sqrt(sum(a_hv²×minutes)/480)`；多段時間不重疊且不超過一天。8小時是參考時間，不強制所有暴露時間≤8小時。4m/s²×120分鐘得到2m/s² A(8)；加2m/s²×120分鐘，合計√5。

部分段未知或整日未完整時，只給完整輸入段的已知小計，完整日值未知。振動幅度未知但觸發時間已知，時間仍列已知並用於檢查一天的總時間上限，不因幅度未知而丟掉。明示整日完整而確實無暴露，才可是0。此處不測振動、不處理原始手機加速度、不實作WBV，亦不把英國行動值當台灣合規線。

ART、MAC、RAPP、RULA、REBA與KIM在教材介紹用途及限制，本套**沒有重建完整正式評分表**。ART不適合鍵盤滑鼠DSE；搬抬、推拉、照護與不同KIM版本須選合適方法。再用授權和改編後方法效度是不同問題。

## 交付與核對

`48_complete_project.py --output 新資料夾`產生：

- `task_observations.csv`：保留各段已知數字與未知狀態。
- `task_observations.svg`：12段動作次數；?代表未知，沒有疾病色帶或傷害機率。
- `report.json`：摘要、搬抬假設、尺寸結果、來源、Python版本及5個資料檔SHA-256。

三個checks驗證觀察缺漏、未知適用、尺寸缺漏被保留。它們為True表示遵守教學契約，**不表示真實性、個人健康、工作安全或合規已證明**。目的地存在即拒絕，不覆寫舊報告。

80項測試涵蓋單位、角度、幾何範圍、未知及0、資料契約、HAV多段及幅度缺漏時的已知時間、RNLE拒絕上限外輸入、來源與交付。測試通過不擴張模型範圍。

## 常見問題

- `ModuleNotFoundError`：確認解壓整包，核心檔與編號檔同層；不要只下載一個檔案。
- `FileExistsError`：輸出換新名稱，程式不會替你刪報告。
- RNLE沒有LI：先核對適用與倍率是否未知、RWL是否0；不要填最佳值完成報告。
- 輸入被拒絕：核對cm、mm、m、N、kg、分鐘與秒；超方法上限不能截斷偽裝有效。
- 圖中出現?：先對照原始觀察，未知本來就應保留。
- 編輯課文後沒變：在專案根目錄重跑`python tools/build.py ergonomics`；讀者不用安裝編譯依賴。

## 正式來源與範圍

[OpenStax解剖生理](https://openstax.org/details/books/anatomy-and-physiology-2e)、[IASP疼痛定義](https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/)、[OSHA電腦工作參考](https://www.osha.gov/etools/computer-workstations/positions)、[HSE ART FAQ](https://www.hse.gov.uk/msd/uld/art/faq.htm)、[HAV手冊](https://www.hse.gov.uk/pubns/priced/l140.pdf)、[台灣第324-1條](https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060009&flno=324-1)。來源查核2026-11-13；正式方法年分及地區背景另列，不把網站更新當方法改版。

所有範例為教育與工作設計討論，不診斷、不推個人承重、不出復健處方、不認定職業病，也不發工作安全或法規認證。真實場域需完整觀察、參與及適當專業協作。

## 48份入口對照

| 入口 | 執行方式 |
| --- | --- |
| 01 | `python 01_task_person_environment.py` |
| 02 | `python 02_hazard_exposure_outcome.py` |
| 03 | `python 03_version_audit.py` |
| 04 | `python 04_bone_context.py` |
| 05 | `python 05_muscle_action.py` |
| 06 | `python 06_nerve_observation.py` |
| 07 | `python 07_external_moment.py` |
| 08 | `python 08_pressure_and_area.py` |
| 09 | `python 09_relaxation_analogy.py` |
| 10 | `python 10_pain_description.py` |
| 11 | `python 11_imaging_context.py` |
| 12 | `python 12_help_context.py` |
| 13 | `python 13_observation_windows.py` |
| 14 | `python 14_sample_geometry.py` |
| 15 | `python 15_action_frequency.py` |
| 16 | `python 16_seat_desk_context.py` |
| 17 | `python 17_monitor_geometry.py` |
| 18 | `python 18_mouse_reach.py` |
| 19 | `python 19_laptop_configuration.py` |
| 20 | `python 20_visual_angle.py` |
| 21 | `python 21_activity_change_schedule.py` |
| 22 | `python 22_shoulder_reach.py` |
| 23 | `python 23_wrist_context.py` |
| 24 | `python 24_repeated_task_record.py` |
| 25 | `python 25_back_task_context.py` |
| 26 | `python 26_lower_limb_support.py` |
| 27 | `python 27_daily_variation.py` |
| 28 | `python 28_rnle_factors.py` |
| 29 | `python 29_rnle_endpoints.py` |
| 30 | `python 30_rnle_applicability.py` |
| 31 | `python 31_repetition_blocks.py` |
| 32 | `python 32_tool_grip_context.py` |
| 33 | `python 33_method_selection.py` |
| 34 | `python 34_pushing_work.py` |
| 35 | `python 35_vibration_a8.py` |
| 36 | `python 36_environment_context.py` |
| 37 | `python 37_control_hierarchy.py` |
| 38 | `python 38_before_after_arithmetic.py` |
| 39 | `python 39_participatory_followup.py` |
| 40 | `python 40_population_scope.py` |
| 41 | `python 41_shared_workstation.py` |
| 42 | `python 42_accommodations.py` |
| 43 | `python 43_original_discomfort_observations.py` |
| 44 | `python 44_matched_observations.py` |
| 45 | `python 45_uncertainty_and_versions.py` |
| 46 | `python 46_report_audit.py` |
| 47 | `python 47_report_preview.py` |
| 48 | `python 48_complete_project.py` |

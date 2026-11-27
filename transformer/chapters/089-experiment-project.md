# 專題建立公平的實驗報告

<figure class="tf-figure"><a href="assets/figures/29-tiny-lm-artifact.svg" target="_blank" rel="noopener"><img src="assets/figures/29-tiny-lm-artifact.svg" alt="原創語料到tokenizer模型訓練checkpoint生成設定評估證據六張卡沿環狀串接，各卡列保存欄位。" loading="lazy"></a><figcaption>從語料到可重現的Tiny LM交付。讓另一個人只用交付資料，就能重建token IDs、載入模型並核對同一個測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依本頁專題追蹤資料、模型、固定輸入、數值比較與交付檔，寫出可重現的命令與限制。 本頁主題：專題建立公平的實驗報告。</p></div>

## 先寫一句可回答的問題

「哪個模型比較好」太寬；「在同一個byte詞表、25句訓練與7句驗證、同樣更新次數下，把MLP中間維度從96改為192，valid NLL如何改變」就可以執行。問題裡要寫資料、比較因素、預算和主要指標，讓讀者知道結論適用的範圍。

先保存基準版，再一次改一個因素。若同時改tokenizer、層數、學習率和訓練句子，結果即使改善，也無法判斷是哪個改動造成。這類整體系統比較仍可做，但報告要稱為系統比較，而不是單一機制的因果效果。

## 同樣step不一定同樣計算量

在本課預設全批次訓練中，每step看到固定25句，所以同一詞表與資料下，140步與280步代表不同的重複曝光量。改成更大模型，即使step相同，每步運算、參數量與時間也不同。固定更新次數、固定token曝光量、固定wall time是在回答不同的資源問題，不能混在一張排名裡不說明。

實驗表至少記錄資料hash、train/valid句數、有效目標token數、更新次數、batch或微批次規則、模型設定、參數量、optimizer、學習率、seed、裝置及套件版本。時間測量另寫暖機和起訖事件；使用GPU時還需處理非同步計時，不能把CPU計時習慣直接移植。

## 指標必須有共同分母

執行`27_perplexity.py`觀察一個手算案例：批次A有2個有效目標、平均 $\mathrm{NLL}=1$ ；B有8個有效目標、平均 $\mathrm{NLL}=3$ 。總NLL為$2\times1+8\times3=26$，除以10得到2.6，PPL約13.4637。直接平均兩批loss得到2，或平均兩批PPL，都是另一種加權方式，不能冒充逐token平均。

PPL比較還要求tokenizer、文字正規化、context切法和loss mask一致。byte模型與BPE模型把同一段文字拆成不同數目的token，PPL不能直接當成相同單位。若要跨分詞器比較，可另定義相同原始文字上的總負對數、bits per byte等指標，並處理前綴、邊界與正規化；不是只換一個欄位名稱。

推論比較也要區分原始模型分數與採樣策略。降低temperature可能讓輸出較固定，但沒有修改模型的原始logits，也不能直接宣稱保留資料的next-token建模能力改善。NLL、生成品質、格式成功率、延遲與記憶體應分欄記錄。

## 配對案例與變異來源

每個模型都對同一批驗證句子產生逐句有效token數與NLL總和，才能定位差異集中在哪些例子。不同句長時，先說明你關心逐token平均還是逐句平均；兩種統計量可以並列，但不能相互替代。例子很少時，直接展示每個案例通常比一個過度精細的顯著性數字更有用。

隨機初始化和訓練順序可能改變結果。若時間允許，用相同的seed清單做多次配對比較，報告平均與分散程度；不要只從十次裡挑最好一次當代表。固定seed協助重現，不等於所有平台都逐bit一致，也不能增加資料的獨立來源數。

本課 $\frac{25}{7}$ 切分只有train與valid；如果反覆用7句valid選設定，它們已參與模型選擇，不能再稱為最終未見test。擴充正式專題時，另留來源獨立的測試資料，待設計決定後才打開一次主要報告；修改後仍保留版本和變更原因。

## 建立可重算的報告

建議交付四份核心資料：設定manifest、每次run摘要、逐案例結果與失敗案例說明。主表列出主要指標、分母、資源與限制；附錄連回原始IDs和artifact hash。測得的數值、由公式估算的容量、尚未執行的硬體功能，使用不同欄位標示。

若比較cache與非cache，先附上logits一致性結果，再提供prefill和decode時間。如果數值不同，先定位正確性，不把更快的錯誤輸出列為性能勝出。若比較框架版本，固定模型設定、權重、輸入和attention implementation，避免把預設值改變當成單純版本差異。

## 練習與解析

**題目：** A模型token  $\mathrm{PPL}=10$ ，B模型 $\mathrm{PPL}=8$ ，但A用byte、B用BPE，B又多訓練一倍時間。可以寫「B架構提高20%」嗎？

**解析：** 不可以。token分母不同，計算預算也不同；百分比更不能直接代表架構造成的改善。先固定共同資料與可比較指標，說明要控制token曝光量還是時間，再設計僅改架構的對照。若保留目前設定，就誠實報成不同tokenizer與預算的系統結果，列出各自條件。

## 參考與日期

查核日期：2026-11-24；數值例與報告設計為原創。

- [PyTorch可重現性說明](https://docs.pytorch.org/docs/2.15/notes/randomness.html)
- [CrossEntropyLoss的sum／mean與ignore_index](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)
- [計算預算與語言模型訓練的原始研究](https://arxiv.org/abs/2203.15556)

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 13_gradient_accumulation.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:13_gradient_accumulation.py -->


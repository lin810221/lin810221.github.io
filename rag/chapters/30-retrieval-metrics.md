## 一個分數無法描述全部品質

Recall 反映有多少需要的證據被找到，Precision 反映送入結果的相關比例，MRR 看第一個相關結果的位置，nDCG 同時考慮位置與相關等級。選指標前先決定你在驗收哪個階段：候選召回、最終 context，或使用者看到的來源。

令 $R$ 是相關文件集合，前 k 名為 $D_k$，常見定義為：

$$
P@k=\frac{|D_k\cap R|}{k},\qquad Recall@k=\frac{|D_k\cap R|}{|R|}
$$

教材 precision 固定除以 k，沒有補足的名次視為未命中。若使用其他定義，報告中要說明。沒有相關標註的無答案題不適合用同一 recall 分母，應另測誤答或無根據檢索行為。

## MRR 看第一個相關結果

$$
MRR=\frac{1}{|Q|}\sum_{q\in Q}\frac{1}{\operatorname{rank}_{first}(q)}
$$

若前 k 名沒有相關結果，本課程的截斷 MRR 貢獻為 0。只有一題、第一個相關結果在第 2 名，reciprocal rank 就是 0.5。MRR 不評估後續是否還找齊其他必要文件，因此多證據題還需 recall 或覆蓋指標。

## nDCG 看分級相關與位置

$$
DCG@k=\sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)},\qquad nDCG@k=\frac{DCG@k}{IDCG@k}
$$

IDCG 使用所有已標註相關文件的理想排序，不是只把系統已找回的結果重新排好。若系統漏掉最相關文件，分母仍要包含它，否則會高估品質。nDCG 也有不同 gain 慣例，此處明確選用指數 gain。

## 手算與程式對照

排名是 X、A、B；A 等級 2、B 等級 1，k=3。Precision=2/3，Recall=1，MRR=1/2。DCG 為 $3/\log_2 3+1/\log_2 4$，IDCG 為 $3+1/\log_2 3$。你可以逐項核對範例。

<!-- example:11_evaluation.py -->

## 重複與聚合要小心

重疊片段不能在文件級評估重複計分。範例先按 doc ID 去重，再計算文件排名。核心函式也防止同一 ID 重複取得 gain，但會保留它占用的位置，避免重複結果虛增成績。

跨題平均時，macro average 讓每題權重相同；若採使用量加權，需保存權重來源。報告除了平均還應列出分組與失敗例，避免少數高頻簡單題蓋過重要錯誤。

## 練習與參考答案

**題目：**前 3 名都是同一相關文件的不同 chunk，已標註兩份必要文件，Recall 是多少？

**參考答案：**若以文件級評估，只找到一份，Recall=1/2。不能把三個 chunk 算成三份相關文件。指標定義與評估單位應固定在報告中。

延伸閱讀：[Stanford IR evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)

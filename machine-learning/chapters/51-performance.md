# 效能與資源：稀疏、batch、平行與量測

用相同工作量比較延遲與吞吐，避免把資源開關當加速保證。

## 先分解時間

解析raw record、前處理、模型運算、序列化與網路各有成本。小模型可能前處理比predict慢；高維文字可能稀疏矩陣轉換佔主體。先量分段與全流程，再決定改模型、批次或資料管線，不只看fit時間。

## 單筆延遲與batch吞吐

一次predict一筆容易重複Python／轉換成本，batch可分攤，但需等待湊批且記憶體增加。比較時同樣筆數、schema、dtype與前處理，記錄暖機、重複分布與p50／p95等。CPU小例可以用perf_counter，避免把第一次import時間當模型推論。

## 稀疏表示與dense膨脹

one-hot或TF-IDF可能百萬欄但每列少量非零。toarray後N×F全部配置可能OOM，with_mean中心化也常不適合。估記憶體需包含indices／indptr等結構與轉換中間量。小課程設sparse_output=False只為容易觀察，不能無條件照搬大型資料。

## 平行的兩層

GridSearchCV的n_jobs與森林n_jobs，再加NumPy／BLAS內部threads，可能產生巢狀過量平行。先選外層或內層主要平行，控制threadpool，量實際CPU與RAM。n_jobs=-1使用可用資源，不等於分散式叢集，也不保證小模型比較快。

```python
from threadpoolctl import threadpool_limits
with threadpool_limits(limits=1):
    # 在此比較固定小型CPU工作，避免BLAS執行緒噪音。
    pass
```

本課入口對小工作限制threads，這是測試條件，不是所有生產模型最佳設定。

## 練習與解答

方案B速度快一倍但只處理半筆數，不能稱相同工作加速。解答：固定資料、feature、預測介面與結果一致性，再記吞吐及資源。若要模型壓縮或ONNX，先在目標runtime驗證數值與任務品質，再量速度；本課沒有憑套件名稱報未測倍數。

## 官方來源與延伸閱讀

- [Computational performance](https://scikit-learn.org/1.9/computing/computational_performance.html)
- [Parallelism](https://scikit-learn.org/1.9/computing/parallelism.html)

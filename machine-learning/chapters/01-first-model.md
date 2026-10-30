# 機器學習全貌：從資料到可以驗證的預測

先跑一個完整模型，再逐步拆開資料、規則、損失與泛化。

## 讓規則從資料學出來

傳統程式由人明確列規則；機器學習先選一類可調函數，再用樣本調整參數。例如根據使用量、使用年資與客服次數預測某事件是否發生。你仍需定義問題、蒐集標籤與安排評估，模型不會替你決定哪些答案值得相信。

本課以2026-10-30查核的最新穩定版scikit-learn 1.9.1實作，先從表格資料與經典方法完整學起。它提供一致的fit、predict與transform介面，讓你將重點放在學習流程與方法假設。深度學習架構、PyTorch操作及數理統計完整推導另有獨立課程，本課補足理解演算法所需的數學。

## 五個基本角色

X是特徵矩陣[N,F]，y是答案[N]，模型f有參數，loss衡量預測誤差，訓練程序尋找較合適的參數。驗證及測試資料用來判斷對未見樣本的表現。訓練分數很高，可能只是記住資料；真正目標是你所關心分布上的可靠預測。

$$
\hat y=f_\theta(x),\qquad \hat\theta=\arg\min_\theta\frac1N\sum_{i=1}^N\ell(f_\theta(x_i),y_i)
$$

## 第一個可執行流程

範例生成固定合成資料，先切分，再將StandardScaler與LogisticRegression包成Pipeline，只在train fit；在保留資料上計算分數，並與DummyClassifier比較。這些數字只描述合成問題，不是任何真實業務的準確率。

閱讀輸出時先看正例比例與dummy，再看模型的precision、recall及average precision。不要只因accuracy大於0.8就說模型好，因為只猜多數類也可能很高。多個指標各有目的，會在評估篇逐步解釋。

## 學習方式與路線

1–12章建立資料與問題契約；13–24章學主要演算法；25–36章學如何比較與決策；37–48章進入非監督與不同應用；49–60章完成交付、專題與練習。每章先預測結果，再執行與修改一個因素。網站實驗使用JavaScript數學；Python範例才是真正scikit-learn。

## 練習與解答

模型只學會train樣本算不算成功？解答：尚不足，需要保留資料、合理切分及任務指標。若模型分數低於dummy，先查資料訊號、標籤時間與前處理，再考慮複雜模型。預測與因果不同：某特徵能預測事件，不代表改變它一定改變事件。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/01_first_pipeline.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:01_first_pipeline.py -->

## 官方來源與延伸閱讀

- [官方入門](https://scikit-learn.org/1.9/getting_started.html)
- [最新正式發布](https://github.com/scikit-learn/scikit-learn/releases/tag/1.9.1)

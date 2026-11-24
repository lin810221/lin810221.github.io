# GreedyBeam與停止政策

<figure class="tf-figure"><a href="assets/figures/16-sampling-truncation.svg" target="_blank" rel="noopener"><img src="assets/figures/16-sampling-truncation.svg" alt="原分布五條機率長條與topk2重正規化0.643 0.357、topp0.8保留前三項重正規化0.529 0.294 0.176並排。" loading="lazy"></a><figcaption>Temperature、top-k與top-p。截斷改變採樣分布；低溫、少候選與輸出正確不是同一件事。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>分開模型分布與解碼政策，指出本頁改變的是機率、候選集合、搜尋還是停止條件。 本頁主題：GreedyBeam與停止政策。</p></div>

Greedy逐步選最高分，beam保留多條候選；兩者都需要明確的長度與完成條件。

## 局部最高不保證整段最高

第一步A機率.6、B機率.4；下一步最佳續接分別.1與.9，兩段機率為.06與.36。greedy會走A，但整段最佳可能是B。Beam寬度2可以暫留兩條，再依累積log機率篩選；這是有限搜尋，不保證找到所有長度中的全域最佳。

## 為什麼長度需要政策

機率連乘通常隨序列增長而降低，直接比較不同長度的總log機率可能偏好較短輸出。length penalty、完成候選的排名和early stopping會改搜尋目標，必須明列。不能把一種校正係數叫作普遍正確的「真實機率」。

開放式文字中，機率最高的字串也不一定最有資訊或最符合人類偏好。Beam常見於某些結構化或序列到序列任務，並非聊天品質的通用升級鍵。

## EOS與文字停止不同

EOS是token層級的特殊ID；stop string可能跨多個token，甚至跨輸出chunk。比較解碼後文字時要留意UTF8碎片、空白與是否把停止字串包含在回應。若設定多個EOS ID，也需對應該tokenizer及模板。

max_new_tokens只限制新增數量，context還包含prompt。達到上限的截斷應列為長度停止；模型選出EOS則是模型停止。兩者對完整性與評估的意義不同，不把所有終止都算成功回答。

## 課程實作範圍

手寫generate支援單一無padding前綴、greedy或取樣、EOS及長度預算，沒有默默實作beam。Beam本章以算例和官方介面解釋，讀者可在已知API及合適任務中擴充，新增前先保留基準測試。

## 練習與解析

某回答因max_new_tokens停止，最後沒有句點，是否要提高上限就好？先檢查context餘量與任務限制，再觀察是否陷入重複或沒有學到EOS。無限制延長會增加延遲與cache，不保證解決原因。

另一個模型在第一步就選EOS，可能是資料或特殊ID錯誤，也可能是prompt與訓練模板不符；先追查token IDs、生成prompt末端和標籤，再調搜尋。保存停止原因有助於定位，而不是把所有空字串當網路問題。

## 原始資料與查核

[Beam與取樣策略](https://huggingface.co/docs/transformers/en/generation_strategies)；[生成設定類別](https://huggingface.co/docs/transformers/en/main_classes/text_generation)

查核：2026-11-24。算例與合成語料為本課原創；小模型結果不代表大型預訓練模型的能力。

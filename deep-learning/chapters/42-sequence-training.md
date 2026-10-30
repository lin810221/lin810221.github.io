# 變長序列完整專案：Embedding到GRU分類

真正處理collate、pack、train/val/test與最後有效state。

## 可知答案的任務

生成240筆，長度2..7，token1..8，答案為最後token>=5。144train、48val、48test。直接看最後ID已有完美規則，所以此專題不是為GRU證明優勢，而是讓你核對變長資料、表示與更新是否正確。

## Collate與模型

collate回tokens[N,T]、lengths[N]與labels[N]。Embedding9×8，GRU hidden12，head12→2。pack_padded_sequence使用lengths CPU、enforce_sorted=False，讓每筆最後有效state對齊，不讓額外PAD參與遞迴。回傳h_n[-1]再分類。

## 資料與模式

raw sequence拒絕空與ID0，0只作PAD；length不可超過T。train shuffle、workers0，eval使用不記錄模式並還原training。保存val最低loss weights，固定預算結束才test。這些都是與影像／表格相同的學習邊界，只是batch契約不同。

## 測試關鍵行為

對[1,2]與[1,2,0,0]、相同有效length2，model輸出應相同。若使用普通RNN直到T最後，PAD可能改state；若length排序與label錯位，也可能看到學不會。先單筆核對，再看整體loss，不只反覆增加hidden。

## 銜接更真實任務

自然語言需tokenizer、詞表與未知規則，時間序列需真實時間切分與可用特徵；整段分類可雙向，線上逐步預測不能偷用未來。這些問題不因pack API成功就自動解決。模型及資料卡應說清任務與基準。

## 練習與解答

把label改成第一token>=5，再比較長度增加後GRU是否較難學；解答：它改變信用分配距離，需新的受控實驗與直接基準，不能沿用前任務test成績。切換LSTM時forward state型態也要調整，並保留padding不變性測試。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/29_sequence_project.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:29_sequence_project.py -->

## 原始論文與官方來源

- [Packed sequences](https://docs.pytorch.org/docs/2.15/generated/torch.nn.utils.rnn.pack_padded_sequence.html)
- [GRU](https://docs.pytorch.org/docs/2.15/generated/torch.nn.GRU.html)

# 參數量初始化與訓練模式

<figure class="tf-figure"><a href="assets/figures/31-tensor-complexity-map.svg" target="_blank" rel="noopener"><img src="assets/figures/31-tensor-complexity-map.svg" alt="五列表格將token hidden QKV dense scores cache對應形狀，dense scores平方長度，cache線性長度再乘dtypebytes。" loading="lazy"></a><figcaption>張量形狀、密集注意力與cache對照。估算時先確認物件：注意力工作矩陣、歷史KV與模型權重不是同一筆記憶體。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿殘差與主路徑追蹤shape，區分逐Token運算與跨Token混合，並核對本頁的參數或正規化。 本頁主題：參數量初始化與訓練模式。</p></div>

## 參數量必須帶架構假設

同樣叫小型Transformer，可以有不同bias、Norm、FFN寬度、位置方法與權重共享。只拿「層數×寬度平方」估算，容易漏掉詞彙表與輸出頭，或把共享表算兩次。先畫完整運算圖，再列每個Parameter shape，才有可核對的總數。

本單元使用獨立玩具設定： $V=259$ 、$D=8$、 $F=16$ 、$L=2$、$H=2$，learned absolute位置上限16；所有Linear無bias，基本兩矩陣FFN，每區塊兩個LayerNorm含gamma/beta，最後另有一個LayerNorm，輸入輸出權重綁定。這不是聲稱本課每個範例都固定此尺寸。

## 逐項手算總數

Embedding共 $259\times 8=2072$ ；位置表 $16\times 8=128$ 。每區塊Attention四個 $8\times 8$ 矩陣共256，FFN兩矩陣共 $2\times 8\times 16=256$ ，兩個LayerNorm共 $4\times 8=32$ ，所以每區塊544，兩區塊1088。最後Norm有16，無bias共享輸出頭不再新增一套表。

總數為 $2072+128+1088+16=3304$ 。若改成獨立輸出頭，加2072，總數5376。若改RMSNorm、SwiGLU、無位置表或加入bias，都需要重算；不能只因最後模型寬度相同，就沿用3304。

## 參數bytes不等於訓練記憶體

3304個float32權重原始資料約13216 bytes，但訓練還有梯度、最佳化器狀態、activation與框架管理成本。Adam類最佳化器常有兩份動量狀態，低精度訓練也可能有高精度主權重等安排。只用權重檔大小推論能否訓練，是忽略主要記憶體來源。

Attention的中間量又受B、T、H與後端影響；參數數不隨T增加，不代表長序列沒有額外記憶體。實際量測須交代裝置、dtype、批次與是否保留計算圖，不能把一個數字跨環境搬用。

## 初始化決定起點，不代表已經學會

隨機初始化讓不同單元不完全對稱，尺度也影響訊號與梯度。Norm的gamma、beta與殘差投影可能有專門設定，具體依架構。固定種子方便比較，但不能因初始loss剛好低就宣稱有語言能力；在近似均勻詞彙分布時，平均CE約ln(V)可作粗略尺度參考，不是任何初始化必定精確等於它。

初始化與權重綁定要在建立最佳化器前完成。若之後換掉Parameter或整個head，舊最佳化器可能仍管理舊物件；程式能forward不代表新參數真的被更新。以參數ID、梯度與更新前後差異驗證，比只看optimizer建立成功可靠。

## 模組註冊與共享

堆疊區塊應使用ModuleList、Sequential等正確註冊容器，或其他明確的PyTorch模組方式；普通Python list不會自動讓其中所有子模組成為父模組註冊參數。若parameters、state_dict或device搬移漏掉層，可能訓練表面上有loss，部分權重卻沒更新。

同一個block物件放進list多次，和建立多個獨立block不同。前者共享參數，計數與模型容量都不同；如果本意是L層獨立，需每次建立新實例。權重共享可以是合法設計，但不能是未察覺的迴圈寫法錯誤。

## 模式與驗證

訓練用train模式、反向與optimizer更新；驗證用eval搭配適當無梯度模式。state_dict通常保存參數與buffer，不包含所有訓練流程狀態；若要精確恢復，還要最佳化器、排程、步數、隨機狀態與資料進度等。這與單純載入權重做推論是不同交付。

練習：手算3304，程式卻只有2760，差544，最先查什麼？可能少註冊或意外共享一個完整block；應列出named_parameters與每層物件，而不直接把手算改成程式值。官方介面見[ModuleList](https://docs.pytorch.org/docs/stable/generated/torch.nn.ModuleList.html)、[Module.parameters](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html)與[初始化工具](https://docs.pytorch.org/docs/stable/nn.init.html)。

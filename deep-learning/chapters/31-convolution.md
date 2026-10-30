# 卷積運算：局部感受、權重共享與cross-correlation

用3×3影像與2×2kernel手算每個位置，理解CNN的結構偏好。

## 為何局部與共享

全連接將所有位置各自連接，卷積則讓同一局部kernel滑過空間，減少參數並偏好平移一致的模式。這是資料結構假設，對影像等常有用，但任意表格欄位未必具有相同鄰接語意。

## 技術上常是cross-correlation

深度學習Conv一般不先翻轉kernel，與純數學某些卷積定義有別。API仍稱convolution。本章手算以實作的cross-correlation一致，不讓符號翻轉差異成為疑似bug。

$$
Y_{n,o,i,j}=b_o+\sum_{c,u,v}W_{o,c,u,v}\,X_{n,c,i+u,j+v}
$$

## 四個輸出的手算

輸入1..9排3×3，kernel[[1,0],[0,-1]]，stride1無padding。左上1-5=-4，其他位置2-6、4-8、5-9也都-4，輸出[1,1,2,2]。第21例直接用F.conv2d核對，沒有依賴下載影像。

## Channel與參數

Conv2d(inC,outC,K)的weight[outC,inC,K,K]，每個out channel聚合所有輸入channel；參數數outC×inC×K²+outC，與影像高寬無關。groups／depthwise會改連接結構，不能仍套一般全channel公式。

## Stride、padding與dilation的尺寸

每個空間維度可獨立計算。設輸入長I、kernel長K、兩側各padding P、stride S、dilation D，dilation讓相鄰kernel元素相隔D個輸入位置。有效kernel跨度為D(K−1)+1；不能把K直接乘D，因為兩端之間只有K−1段間距。

$$
O=\left\lfloor\frac{I+2P-D(K-1)-1}{S}+1\right\rfloor
$$

例如I=8、K=3、P=1、S=2、D=1，得到O=4。padding保留尺寸與真實資訊是不同概念；補的零不是額外觀測到的像素。

## 共享權重怎麼得到梯度

若上游導數為G=∂L/∂Y，一個kernel weight在多個輸出位置被重複使用，其梯度就是各位置「上游G×對應輸入」的加總。反過來，同一輸入像素也可能參與多個視窗，因此input gradient要加總所有相關路徑。這是全連接鏈式法則在共享與局部連接下的展開，不是另一種學習規則。

## 平移等變與邊界

共享kernel提供某些平移等變結構，padding、stride、裁切與邊界會影響精確性；pooling也不自動使任何尺度／角度都不變。不要把CNN叫「天然理解所有位置」；augmentation與資料多樣性仍重要。

## 練習與解答

若將kernel翻轉180度，這個例子結果會變+4，反映定義差異。解答：先核對API與手算的一致定義，再查運算。輸入通道從1變3時，不只reshape，還要改kernel的in_channel與資料語意。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/21_convolution.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:21_convolution.py -->

## 原始論文與官方來源

- [Convolution layers](https://docs.pytorch.org/docs/2.15/nn.html#convolution-layers)
- [卷積原理](https://www.deeplearningbook.org/contents/convnets.html)

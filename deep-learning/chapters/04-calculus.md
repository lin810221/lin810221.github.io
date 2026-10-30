# 導數、梯度與Chain Rule：從局部變化到整個模型

用標量與向量的連鎖關係，理解反向傳播不是神秘黑盒。

## 導數回答局部問題

導數描述輸入小幅變動時輸出的一階近似，梯度收集對每個參數的偏導。它不是整段曲線平均，也不保證一個大步長後仍下降。訓練沿負梯度走，步幅與目標曲率一樣重要。

$$
L(\theta+\Delta)\approx L(\theta)+\nabla L(\theta)^T\Delta
$$

例如L=(w-3)²，w=1時梯度-4；lr=.1更新1.4，loss下降；lr=2更新9，loss反而增加。梯度正確與最佳化穩定是兩項不同檢查。

## 逐段相乘

若a=wx+b、h=σ(a)、ŷ=vh+c、L=.5(ŷ-t)²，對w的導數是各段局部導數的乘積。先算forward中間值，再由L往回傳，避免重複求整個式子。分支時，同一變數透過多條路影響L，梯度要相加。

$$
\frac{\partial L}{\partial w}=(\hat y-t)\,v\,h(1-h)\,x
$$

## 方向與尺度

某個參數gradient很小，可能是局部已接近解，也可能因activation飽和、長鏈乘積縮小或loss縮放。不能只看到0就判斷模型學會。矩陣網路還要看Jacobian方向與奇異值，單一標量範數不能描述所有訊號。

## 高階導數與計算圖

一般backward用於第一階導數；需要對梯度再微分時，必須保留可微分的梯度計算。retain_graph與create_graph目的不同，前者保留同一圖重用，後者建立導數的圖。主線先第一階，不用兩個開關作為所有錯誤的萬用修復。

## 練習與解答

L=(wx-t)²，x=2,w=1,t=3，梯度是2(2-3)×2=-4；若loss前加.5，梯度變-2。解答：記住sum／mean與常數因子會改梯度尺度。第9章會完整手算含sigmoid的兩層，再逐參數與Autograd比對。

## 原始論文與官方來源

- [Autograd mechanics](https://docs.pytorch.org/docs/2.15/notes/autograd.html)
- [數值計算與梯度](https://www.deeplearningbook.org/contents/numerical.html)

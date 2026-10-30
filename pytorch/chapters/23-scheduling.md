# 學習率排程、Early Stopping 與最佳模型

讓停止條件與best checkpoint可解釋，也能在中斷後繼續。

## 排程需要知道更新單位

StepLR可每幾個epoch降低lr；CosineAnnealingLR依設定週期變化；ReduceLROnPlateau依傳入指標決定。先決定scheduler.step以batch還是epoch為單位，T_max或step_size也要使用同一單位。一般參數更新後再呼叫排程；plateau則在完成驗證、取得指標後呼叫。

```python
import torch
model = torch.nn.Linear(4,3)
optimizer = torch.optim.SGD(model.parameters(), lr=.1)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=.5)
for epoch in range(4):
    optimizer.zero_grad(set_to_none=True)
    model(torch.ones(2,4)).square().mean().backward()
    optimizer.step()
    print(epoch+1, optimizer.param_groups[0]['lr'])
    scheduler.step()
```

上例只展示順序，實際是一整個train_epoch結束後再step。AMP若跳過optimizer更新，按更新次數排程的邏輯也要處理對應步數，不只照迴圈計數。

## early stopping的狀態

選定val loss越小越好，定義min_delta、patience與best。改善時清等待次數並保存快照；無改善累積至patience才停止。不要偷看test來重設patience，也不要因單一較差epoch立刻判定過擬合。若恢復訓練，best、wait、scheduler state都需要保存。

## best weights要真的凍結

`best_state=model.state_dict()`可能仍引用正在更新的Tensor。使用逐值detach().cpu().clone，或直接保存到獨立檔案。訓練結束先load best，再評估test；「最後一輪」與「驗證最佳」是不同選擇。課程專題保留current model供resume，另存best_model供最終推論。

## 練習與解答

val losses為[.8,.6,.61,.62,.59]，patience=2且min_delta=0時，會在第4輪停止；第5輪不會發生。若你事後看到.59才調patience，就是用額外資訊做選擇，需要誠實記錄。另一題：只存best weights可以續訓到完全相同結果嗎？答案：不足，仍缺current optimizer、RNG、scheduler與資料位置等狀態。

## 官方來源與延伸閱讀

- [學習率排程與順序](https://docs.pytorch.org/docs/2.15/optim.html#how-to-adjust-learning-rate)
- [模型存取教學](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html)

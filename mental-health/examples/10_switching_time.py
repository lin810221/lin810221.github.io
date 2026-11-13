"""10: switching_time. Original fictional educational example."""
from psych_core import task_switch
for blocks,minutes in [(6,20),(2,60)]:print(task_switch(blocks,minutes,30))
print("兩種假設都工作120分鐘；30秒切換成本是指定值，不是通用實驗常數。")

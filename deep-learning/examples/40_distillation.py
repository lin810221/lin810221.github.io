"""Train a small student from hard labels and detached teacher soft targets."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit
from course_core import MLP,make_loaders,train_epoch,evaluate,distillation_loss

def main(argv=None):
    del argv
    setup()
    loaders,_=make_loaders('tabular');train,validation,test=loaders
    teacher=MLP();teacher_optimizer=torch.optim.AdamW(teacher.parameters(),lr=.02)
    for _ in range(12):train_epoch(teacher,train,teacher_optimizer)
    teacher.eval()
    for p in teacher.parameters():p.requires_grad_(False)
    student=MLP(width=6);optimizer=torch.optim.AdamW(student.parameters(),lr=.02)
    for _ in range(18):
        student.train()
        for x,y in train:
            with torch.no_grad():target=teacher(x)
            optimizer.zero_grad(set_to_none=True)
            loss=distillation_loss(student(x),target,y,temperature=2.,hard_weight=.5)
            loss.backward();optimizer.step()
    result={'teacher_parameters':sum(p.numel() for p in teacher.parameters()),
            'student_parameters':sum(p.numel() for p in student.parameters()),
            'student_validation':evaluate(student,validation),'student_test':evaluate(student,test),
            'scope':'fixed toy distillation configuration; no claim that the student matches or beats the teacher'}
    return emit(result)

if __name__=="__main__":
    main()

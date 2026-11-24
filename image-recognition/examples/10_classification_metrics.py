"""Offline executable teaching example; run from this directory."""
import numpy as np
from vision_core import confusion_matrix,print_json

def main():
    target=[0,0,0,0,1,1];prediction=[0,0,0,0,0,1]
    matrix=confusion_matrix(target,prediction)
    precision=np.divide(np.diag(matrix),matrix.sum(0),out=np.zeros(2),where=matrix.sum(0)!=0)
    recall=np.diag(matrix)/matrix.sum(1)
    print_json({'matrix_true_rows':matrix.tolist(),'accuracy':float(np.trace(matrix)/matrix.sum()),
                'precision':precision.tolist(),'recall':recall.tolist(),'balanced_accuracy':float(recall.mean())})

if __name__=='__main__': main()

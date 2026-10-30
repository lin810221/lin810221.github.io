"""Deep-learning convolution uses cross-correlation without flipping the kernel."""
import torch
from torch import nn
from torch.nn import functional as F
from course_core import setup,emit


def main(argv=None):
    del argv
    setup()
    image=torch.arange(1.,10.).reshape(1,1,3,3)
    kernel=torch.tensor([[[[1.,0.],[0.,-1.]]]])
    output=F.conv2d(image,kernel)
    result={'input':image,'kernel':kernel,'output':output,'output_shape':list(output.shape),
            'manual_first_value':1.-5.}
    return emit(result)

if __name__=="__main__":
    main()

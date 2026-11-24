"""Offline executable teaching example; run from this directory."""
import torch
from vision_core import train_classifier,make_shapes,print_json

def main():
    model,_=train_classifier()
    images,labels,_,_=make_shapes(24,seed=41)
    model.eval()
    with torch.inference_mode():
        features=torch.nn.functional.normalize(model.features(images).flatten(1),dim=1)
        similarities=features[0]@features.T
        similarities[0]=-float('inf') # exclude query identity
        neighbors=similarities.topk(5).indices
    print_json({'query_label':int(labels[0]),'neighbor_indices':neighbors.tolist(),
                'neighbor_labels':labels[neighbors].tolist(),
                'precision_at5':float((labels[neighbors]==labels[0]).float().mean()),
                'scope':'synthetic same-generator retrieval, not semantic search benchmark'})

if __name__=='__main__': main()

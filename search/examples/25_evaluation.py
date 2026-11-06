"""ANN recall measures agreement with exact neighbors, not human relevance."""
from search_core import ann_recall,ndcg

if __name__ == "__main__":
    exact,ann = [1,2,3],[3,1,8]
    qrels = {1:3,2:0,3:1,8:3}
    print("ANN Recall@3",ann_recall(exact,ann,3))
    print("nDCG@3",ndcg(ann,qrels,3))
    print("No eligible exact neighbors",ann_recall([],[],3))

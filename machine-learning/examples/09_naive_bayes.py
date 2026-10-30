"""Tiny original English text fixture; no corpus download."""
import numpy as np
from threadpoolctl import threadpool_limits
from course_core import emit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def main(argv=None):
    del argv
    with threadpool_limits(limits=1):
        texts=['team wins football match','football goal and team','match player scores goal',
               'python code and data','software code fixes bug','python software data tools']
        labels=['sport','sport','sport','software','software','software']
        model=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),MultinomialNB(alpha=1.)).fit(texts,labels)
        query=['python code tools','team scores goal']
        result={'queries':query,'predictions':model.predict(query),'classes':model.classes_,
                'vocabulary_size':len(model[0].vocabulary_),
                'scope':'tiny mechanism example, not text accuracy evaluation'}
    return emit(result)

if __name__ == "__main__":
    main()

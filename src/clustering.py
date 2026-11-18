"""Failure clustering: TF-IDF + k-means (numpy only).

Light fallback for the original sentence-transformers + HDBSCAN/UMAP pipeline;
same idea — group failure texts so recurring modes surface — with no heavy downloads.
"""
import re, math
from collections import Counter
import numpy as np

def _tfidf(texts):
    docs = [re.findall(r"[a-z0-9_]+", t.lower()) for t in texts]
    vocab = sorted({w for d in docs for w in d})
    idx = {w:i for i,w in enumerate(vocab)}
    df = Counter()
    for d in docs: df.update(set(d))
    n = len(docs)
    X = np.zeros((n, len(vocab)))
    for r,d in enumerate(docs):
        for w,c in Counter(d).items():
            X[r, idx[w]] = c * (math.log((1+n)/(1+df[w])) + 1)
    norms = np.linalg.norm(X, axis=1, keepdims=True); norms[norms==0]=1
    return X/norms, vocab

def cluster_failures(texts, n_clusters=3, seed=42, iters=50):
    if not texts: return []
    k = min(n_clusters, len(texts))
    X, _ = _tfidf(texts)
    rng = np.random.default_rng(seed)
    centres = X[rng.choice(len(X), size=k, replace=False)]
    labels = np.zeros(len(X), dtype=int)
    for _ in range(iters):
        labels = np.argmin(((X[:,None,:]-centres[None,:,:])**2).sum(-1), axis=1)
        for j in range(k):
            if (labels==j).any(): centres[j] = X[labels==j].mean(0)
    return labels.tolist()

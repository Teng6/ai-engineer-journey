import numpy as np

def cosine(a, b):
    dot = np.dot(a, b)
    len_a = np.linalg.norm(a)
    len_b = np.linalg.norm(b)
    return dot / (len_a * len_b)

import numpy as np

def cosine(a, b):
    dot = np.dot(a, b)
    len_a = np.linalg.norm(a)
    len_b = np.linalg.norm(b)
    return dot / (len_a * len_b)

print(cosine(np.array([1, 2, 3]), np.array([10, 20, 30])))
print(cosine(np.array([1, 0]), np.array([-1, 0])))
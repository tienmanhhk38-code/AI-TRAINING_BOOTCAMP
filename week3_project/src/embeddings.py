import math
import re
from collections import Counter


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text):
    return TOKEN_PATTERN.findall(text.lower())


def embed_text(text):
    return Counter(tokenize(text))


def cosine_similarity(left, right):
    common_tokens = set(left) & set(right)
    dot = sum(left[token] * right[token] for token in common_tokens)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return dot / (left_norm * right_norm)

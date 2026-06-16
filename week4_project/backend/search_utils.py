import re
import unicodedata
from collections import Counter

TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")

ROLE_TOKENS = {
    "ceo",
    "cfo",
    "coo",
    "cto",
    "director",
    "head",
    "manager",
    "president",
    "vp",
}
WHO_TOKENS = {"ai", "who", "whom"}
PERSON_CONTEXT_TOKENS = {
    "appointment",
    "appointed",
    "position",
    "mr",
    "mrs",
    "ms",
}

BRANCH_ALIASES = {
    "hn": {"hn", "hanoi", "ha", "noi"},
    "hcm": {"hcm", "hcmc", "saigon", "sai", "gon", "ho", "chi", "minh"},
    "vinh": {"vinh"},
    "japan": {"japan", "jp"},
    "singapore": {"singapore", "sg"},
}


def normalize_search_text(text):
    lowered = text.lower().replace("đ", "d")
    decomposed = unicodedata.normalize("NFD", lowered)
    without_marks = "".join(
        char for char in decomposed
        if unicodedata.category(char) != "Mn"
    )
    ascii_text = re.sub(r"[^a-z0-9_]+", " ", without_marks)
    return re.sub(r"\s+", " ", ascii_text).strip()


def tokenize(text):
    normalized = normalize_search_text(text)
    tokens = TOKEN_PATTERN.findall(normalized)
    expanded = list(tokens)

    if re.search(r"\bha\s+noi\b", normalized) or "hanoi" in tokens or "hn" in tokens:
        expanded.extend(["hn", "hanoi", "ha", "noi"])

    if (
        re.search(r"\bho\s+chi\s+minh\b", normalized)
        or re.search(r"\bsai\s+gon\b", normalized)
        or "hcm" in tokens
        or "hcmc" in tokens
        or "saigon" in tokens
    ):
        expanded.extend(["hcm", "hcmc", "saigon", "sai", "gon", "ho", "chi", "minh"])

    return expanded


def branch_keys(tokens):
    token_set = set(tokens)
    return {
        branch
        for branch, aliases in BRANCH_ALIASES.items()
        if token_set & aliases
    }


def cosine_similarity(left, right):
    common_tokens = set(left) & set(right)
    dot = sum(left[token] * right[token] for token in common_tokens)
    left_norm = sum(value * value for value in left.values()) ** 0.5
    right_norm = sum(value * value for value in right.values()) ** 0.5

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return dot / (left_norm * right_norm)


def relevance_score(question, text):
    query_embedding = Counter(tokenize(question))
    text_embedding = Counter(tokenize(text))
    score = cosine_similarity(query_embedding, text_embedding)

    query_tokens = set(query_embedding)
    text_tokens = set(text_embedding)
    roles = query_tokens & ROLE_TOKENS
    branches = branch_keys(query_tokens)
    normalized_text = normalize_search_text(text)

    if roles and branches:
        for role in roles:
            for branch in branches:
                role_before_branch = re.search(
                    rf"\b{re.escape(role)}\b(?:\s+\w+){{0,5}}\s+\b{re.escape(branch)}\b",
                    normalized_text,
                )
                branch_before_role = re.search(
                    rf"\b{re.escape(branch)}\b(?:\s+\w+){{0,3}}\s+\b{re.escape(role)}\b",
                    normalized_text,
                )

                if role_before_branch or branch_before_role:
                    score += 0.45
                elif role in text_tokens and branch in text_tokens:
                    score += 0.05

    if roles and query_tokens & WHO_TOKENS and text_tokens & PERSON_CONTEXT_TOKENS:
        score += 0.18

    return score

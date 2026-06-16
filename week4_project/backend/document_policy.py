COMPANY_KEYWORDS = {
    "bnk",
    "company",
    "cong ty",
    "công ty",
    "noi quy",
    "nội quy",
    "quy dinh",
    "quy định",
    "chinh sach",
    "chính sách",
    "phuc loi",
    "phúc lợi",
    "nhan su",
    "nhân sự",
    "hr",
    "hanh chinh",
    "hành chính",
    "quy trinh",
    "quy trình",
    "hop dong",
    "hợp đồng",
    "nghi phep",
    "nghỉ phép",
    "bao mat",
    "bảo mật",
    "luong",
    "lương",
    "thuong",
    "thưởng",
    "bao hiem",
    "bảo hiểm",
}

COMPANY_QUESTION_KEYWORDS = {
    "bnk",
    "cong ty",
    "công ty",
    "noi quy",
    "nội quy",
    "quy dinh",
    "quy định",
    "chinh sach",
    "chính sách",
    "nghi phep",
    "nghỉ phép",
    "phuc loi",
    "phúc lợi",
    "luong",
    "lương",
    "thuong",
    "thưởng",
    "hr",
}

def normalize_text(text):
    return " ".join(text.lower().split())

def keyword_hits(text, keywords):
    normalized = normalize_text(text)
    return sorted(keyword for keyword in keywords if keyword in normalized)

def classify_document(filename, text):
    haystack = f"{filename}\n{text[:4000]}"
    hits = keyword_hits(haystack, COMPANY_KEYWORDS)
    score = len(hits)

    if score >= 2 or "bnk" in hits:
        return {
            "status": "approved",
            "score": score,
            "reason": "Document has company-related keywords.",
            "matched_keywords": hits,
        }

    return {
        "status": "needs_review",
        "score": score,
        "reason": "Document does not have enough company-related signals.",
        "matched_keywords": hits,
    }

def is_company_question(question):
    return bool(keyword_hits(question, COMPANY_QUESTION_KEYWORDS))

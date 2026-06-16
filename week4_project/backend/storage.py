import json
from pathlib import Path


def read_json(path, default):
    path = Path(path)
    if not path.exists():
        return default

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def append_conversation(path, question, answer_record):
    conversations = read_json(path, [])
    conversations.append({
        "question": question,
        "answer": answer_record["answer"],
        "sources": answer_record["sources"],
    })
    write_json(path, conversations)
    return conversations[-1]

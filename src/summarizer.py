import re


def generate_simple_summary(
    text: str,
    max_sentences: int = 5,
) -> str:
    """Create a simple extractive summary."""
    clean_text = text.replace("\r", "\n")

    candidates = []

    code_patterns = [
        "import ",
        "from ",
        "def ",
        "return ",
        "st.",
        "reader.",
        "uploaded_file",
        "study_history",
        "page_count",
        "pdf_text",
        "append(",
        "len(",
        "if ",
        "else:",
    ]

    important_words = [
        "目标",
        "完成",
        "功能",
        "知识",
        "学习",
        "表示",
        "用于",
        "作用",
        "意思",
        "文件",
        "页面",
        "读取",
        "上传",
        "判断",
        "提取",
        "保存",
        "结果",
        "需要",
        "可以",
        "如果",
        "因为",
        "所以",
        "负责",
        "流程",
    ]

    lines = clean_text.splitlines()

    for line_number, line in enumerate(lines):
        line = re.sub(
            r"\s+",
            " ",
            line,
        ).strip()

        if not line:
            continue

        sentences = re.split(
            r"(?<=[。！？.!?])\s*",
            line,
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) < 15:
                continue

            if len(sentence) > 250:
                continue

            lower_sentence = sentence.lower()

            is_code = any(
                pattern in lower_sentence
                for pattern in code_patterns
            )

            if is_code:
                continue

            code_symbol_count = sum(
                sentence.count(symbol)
                for symbol in [
                    "(",
                    ")",
                    "[",
                    "]",
                    "{",
                    "}",
                    "=",
                    "_",
                ]
            )

            if code_symbol_count >= 3:
                continue

            score = 0

            for word in important_words:
                if word in sentence:
                    score += 3

            if sentence.endswith(
                ("。", "！", "？", ".", "!", "?")
            ):
                score += 1

            if 25 <= len(sentence) <= 120:
                score += 2

            candidates.append(
                (
                    score,
                    line_number,
                    sentence,
                )
            )

    if not candidates:
        return (
            "要約できる説明文が見つかりませんでした。"
        )

    candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    selected = []
    selected_texts = set()

    for score, line_number, sentence in candidates:
        sentence_key = sentence[:30]

        if sentence_key in selected_texts:
            continue

        selected.append(
            (
                line_number,
                sentence,
            )
        )

        selected_texts.add(sentence_key)

        if len(selected) >= max_sentences:
            break

    selected.sort(
        key=lambda item: item[0]
    )

    summary_sentences = [
        sentence
        for line_number, sentence in selected
    ]

    return "\n\n".join(summary_sentences)
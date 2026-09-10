import re


def generate_quiz(
    text: str,
    max_questions: int = 5,
) -> list[dict]:
    """Generate simple fill-in-the-blank questions."""
    lines = text.replace("\r", "\n").splitlines()
    questions = []

    ignored_words = {
        "streamlit",
        "localhost",
        "http",
        "https",
    }

    for line in lines:
        sentence = re.sub(
            r"\s+",
            " ",
            line,
        ).strip()

        if len(sentence) < 20 or len(sentence) > 150:
            continue

        words = re.findall(
            r"[A-Za-z][A-Za-z0-9_-]{3,}|"
            r"[\u4e00-\u9fff]{2,}|"
            r"[\u30a0-\u30ff]{3,}",
            sentence,
        )

        if not words:
            continue

        possible_answers = [
            word
            for word in words
            if word.lower() not in ignored_words
        ]

        if not possible_answers:
            continue

        answer = max(
            possible_answers,
            key=len,
        )

        question_text = sentence.replace(
            answer,
            "＿＿＿＿",
            1,
        )

        questions.append(
            {
                "question": question_text,
                "answer": answer,
            }
        )

        if len(questions) >= max_questions:
            break

    return questions
import re


def generate_flashcards(
    text: str,
    max_cards: int = 5,
) -> list[dict]:
    """Generate simple flashcards from text."""
    lines = text.replace("\r", "\n").splitlines()
    flashcards = []

    ignored_words = {
        "streamlit",
        "localhost",
        "http",
        "https",
    }

    used_terms = set()

    for line in lines:
        sentence = re.sub(
            r"\s+",
            " ",
            line,
        ).strip()

        if len(sentence) < 20 or len(sentence) > 180:
            continue

        words = re.findall(
            r"[A-Za-z][A-Za-z0-9_-]{3,}|"
            r"[\u4e00-\u9fff]{2,}|"
            r"[\u30a0-\u30ff]{3,}",
            sentence,
        )

        possible_terms = [
            word
            for word in words
            if word.lower() not in ignored_words
        ]

        if not possible_terms:
            continue

        term = max(
            possible_terms,
            key=len,
        )

        term_key = term.lower()

        if term_key in used_terms:
            continue

        flashcards.append(
            {
                "front": term,
                "back": sentence,
            }
        )

        used_terms.add(term_key)

        if len(flashcards) >= max_cards:
            break

    return flashcards
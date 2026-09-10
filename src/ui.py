import streamlit as st

from src.pdf_utils import (
    extract_pdf_text,
    get_pdf_page_count,
)
from src.quiz_generator import generate_quiz
from src.summarizer import generate_simple_summary


def show_home(
    title: str,
    description: str,
) -> None:
    """Display the home page."""
    st.title(title)
    st.write(description)

    with st.sidebar:
        st.header("学習メニュー")

        study_mode = st.selectbox(
            "機能を選択してください",
            [
                "学習記録",
                "要約",
                "Quiz",
                "Flashcards",
            ],
        )

    st.info(
        f"選択中の機能：{study_mode}"
    )

    if study_mode == "学習記録":
        show_study_history()

    elif study_mode == "要約":
        show_summary()

    elif study_mode == "Quiz":
        show_quiz()

    elif study_mode == "Flashcards":
        st.info(
            "Flashcards機能は今後追加する予定です。"
        )


def show_study_history() -> None:
    """Display the study history feature."""
    if "study_history" not in st.session_state:
        st.session_state.study_history = []

    study_topic = st.text_input(
        "今日学習した内容を入力してください"
    )

    if st.button("記録する"):
        if study_topic:
            st.session_state.study_history.append(
                study_topic
            )

            st.success(
                f"「{study_topic}」を記録しました。"
            )
        else:
            st.warning(
                "学習内容を入力してください。"
            )

    if st.session_state.study_history:
        st.subheader("学習履歴")

        for topic in reversed(
            st.session_state.study_history
        ):
            st.write(f"- {topic}")


def show_summary() -> None:
    """Display the PDF summary feature."""
    uploaded_file = st.file_uploader(
        "要約するPDFをアップロードしてください",
        type=["pdf"],
        key="summary_pdf",
    )

    if uploaded_file is None:
        st.info(
            "PDFをアップロードすると要約できます。"
        )
        return

    st.success(
        f"「{uploaded_file.name}」をアップロードしました。"
    )

    st.write(
        f"ファイルサイズ：{uploaded_file.size} bytes"
    )

    page_count = get_pdf_page_count(
        uploaded_file
    )

    st.write(
        f"ページ数：{page_count}ページ"
    )

    pdf_text = extract_pdf_text(
        uploaded_file
    )

    if not pdf_text:
        st.warning(
            "PDFからテキストを抽出できませんでした。"
        )
        return

    with st.expander(
        "抽出したテキストを確認する"
    ):
        st.text_area(
            "PDFの内容",
            value=pdf_text[:2000],
            height=250,
        )

    if st.button("要約を作成する"):
        summary = generate_simple_summary(
            pdf_text,
            max_sentences=5,
        )

        st.session_state.summary = summary

    if "summary" in st.session_state:
        st.subheader("要約結果")

        st.write(
            st.session_state.summary
        )

        st.caption(
            "この要約は原文から重要な文を選択した"
            "無料の簡易要約です。"
        )


def show_quiz() -> None:
    """Display the PDF quiz feature."""
    uploaded_file = st.file_uploader(
        "Quizを作成するPDFをアップロードしてください",
        type=["pdf"],
        key="quiz_pdf",
    )

    if uploaded_file is None:
        st.info(
            "PDFをアップロードするとQuizを作成できます。"
        )
        return

    st.success(
        f"「{uploaded_file.name}」をアップロードしました。"
    )

    st.write(
        f"ファイルサイズ：{uploaded_file.size} bytes"
    )

    page_count = get_pdf_page_count(
        uploaded_file
    )

    st.write(
        f"ページ数：{page_count}ページ"
    )

    pdf_text = extract_pdf_text(
        uploaded_file
    )

    if not pdf_text:
        st.warning(
            "PDFからテキストを抽出できませんでした。"
        )
        return

    if st.button("Quizを作成する"):
        st.session_state.quiz_questions = (
            generate_quiz(
                pdf_text,
                max_questions=5,
            )
        )

    if "quiz_questions" not in st.session_state:
        return

    questions = st.session_state.quiz_questions

    if not questions:
        st.warning(
            "Quizに使用できる文章が見つかりませんでした。"
        )
        return

    st.subheader("Quiz")

    user_answers = []

    for index, quiz in enumerate(questions):
        st.write(
            f"問題 {index + 1}："
            f"{quiz['question']}"
        )

        user_answer = st.text_input(
            "答えを入力してください",
            key=f"quiz_answer_{index}",
        )

        user_answers.append(
            user_answer
        )

    if st.button("答え合わせ"):
        score = 0

        for index, quiz in enumerate(questions):
            correct_answer = quiz["answer"]

            user_answer = (
                user_answers[index]
                .strip()
            )

            if (
                user_answer.lower()
                == correct_answer.lower()
            ):
                st.success(
                    f"問題 {index + 1}：正解です！"
                )

                score += 1
            else:
                st.error(
                    f"問題 {index + 1}：不正解です。"
                    f" 正解は「{correct_answer}」です。"
                )

        st.info(
            f"結果：{score} / "
            f"{len(questions)} 問正解"
        )
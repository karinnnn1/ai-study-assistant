import streamlit as st


def show_home(title: str, description: str) -> None:
    """Display the home page."""
    st.title(title)
    st.write(description)

    with st.sidebar:
        st.header("学習メニュー")
        study_mode = st.selectbox(
            "機能を選択してください",
            ["学習記録", "要約", "Quiz", "Flashcards"],
        )

    st.info(f"選択中の機能：{study_mode}")

    if "study_history" not in st.session_state:
        st.session_state.study_history = []

    study_topic = st.text_input(
        "今日学習した内容を入力してください"
    )

    if st.button("記録する"):
        if study_topic:
            st.session_state.study_history.append(study_topic)
            st.success(
                f"「{study_topic}」を記録しました。"
            )
        else:
            st.warning(
                "学習内容を入力してください。"
            )

    if st.session_state.study_history:
        st.subheader("学習履歴")

        for topic in reversed(st.session_state.study_history):
            st.write(f"- {topic}")
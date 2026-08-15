import streamlit as st

from src.app.chatbot import HybridRAGBot


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Hybrid RAG Policy Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #777;
        margin-bottom: 1.5rem;
    }

    .source-box {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 12px;
        margin-top: 8px;
    }

    .source-title {
        font-weight: 600;
    }

    .status-box {
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "bot" not in st.session_state:

    st.session_state.bot = None


# ============================================================
# BOT INITIALIZATION
# ============================================================

@st.cache_resource(
    show_spinner=False
)
def load_bot():

    return HybridRAGBot()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Hybrid RAG")

    st.markdown(
        """
        **Architecture**

        🔎 FAISS Vector Search  
        🕸️ Neo4j Knowledge Graph  
        🤖 OpenAI Generation  
        🛡️ Input/Output Guardrails  
        📊 DeepEval Evaluation
        """
    )

    st.divider()

    st.subheader("System")

    st.success(
        "Hybrid RAG enabled"
    )

    st.info(
        "Python 3.14 environment"
    )

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "Answers are generated only "
        "from retrieved knowledge-base "
        "content."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 Hybrid RAG Policy Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about organizational policies, '
    'procedures and internal documents.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# LOAD BOT
# ============================================================

if st.session_state.bot is None:

    with st.spinner(
        "Initializing Hybrid RAG system..."
    ):

        try:

            st.session_state.bot = load_bot()

        except Exception as exc:

            st.error(
                "Unable to initialize the RAG system."
            )

            st.exception(exc)

            st.stop()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                "📚 Retrieved sources"
            ):

                for source in message[
                    "sources"
                ]:

                    st.markdown(
                        f"""
                        <div class="source-box">

                        <div class="source-title">
                        {source["chunk_id"]}
                        </div>

                        <b>Source:</b>
                        {source["source"]}

                        <br>

                        <b>Pages:</b>
                        {source["page_start"]}
                        -
                        {source["page_end"]}

                        <br>

                        <b>Retrieved by:</b>
                        {source["retrieval_source"]}

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a policy question..."
)


if question:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching policies and generating answer..."
        ):

            try:

                result = (
                    st.session_state.bot.ask(
                        question
                    )
                )

                answer = result.get(
                    "answer",
                    "No answer generated.",
                )

                retrieval = result.get(
                    "retrieval"
                )

                merged_chunks = []

                if retrieval:

                    merged_chunks = (
                        retrieval.get(
                            "merged_chunks",
                            [],
                        )
                    )

                st.markdown(
                    answer
                )

                # ------------------------------------------------
                # Sources
                # ------------------------------------------------

                if merged_chunks:

                    with st.expander(
                        "📚 Retrieved sources"
                    ):

                        for index, chunk in enumerate(
                            merged_chunks,
                            start=1,
                        ):

                            st.markdown(
                                f"""
                                <div class="source-box">

                                <div class="source-title">
                                [{index}] {
                                    chunk.get(
                                        "chunk_id",
                                        "Unknown chunk"
                                    )
                                }
                                </div>

                                <b>Source:</b>
                                {
                                    chunk.get(
                                        "source",
                                        "Unknown"
                                    )
                                }

                                <br>

                                <b>Pages:</b>
                                {
                                    chunk.get(
                                        "page_start",
                                        ""
                                    )
                                }
                                -
                                {
                                    chunk.get(
                                        "page_end",
                                        ""
                                    )
                                }

                                <br>

                                <b>Retrieval:</b>
                                {
                                    chunk.get(
                                        "retrieval_source",
                                        "Unknown"
                                    )
                                }

                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                # ------------------------------------------------
                # Save assistant message
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": [
                            {
                                "chunk_id": chunk.get(
                                    "chunk_id",
                                    "Unknown",
                                ),
                                "source": chunk.get(
                                    "source",
                                    "Unknown",
                                ),
                                "page_start": chunk.get(
                                    "page_start",
                                    "",
                                ),
                                "page_end": chunk.get(
                                    "page_end",
                                    "",
                                ),
                                "retrieval_source": chunk.get(
                                    "retrieval_source",
                                    "Unknown",
                                ),
                            }
                            for chunk
                            in merged_chunks
                        ],
                    }
                )

            except Exception as exc:

                st.error(
                    "The chatbot encountered "
                    "an error while processing "
                    "your question."
                )

                st.exception(exc)
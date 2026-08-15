import { useState } from "react";

import "./App.css";


function App() {

    const [question, setQuestion] =
        useState("");

    const [messages, setMessages] =
        useState([]);

    const [loading, setLoading] =
        useState(false);


    async function sendQuestion() {

        const trimmedQuestion =
            question.trim();


        if (
            !trimmedQuestion ||
            loading
        ) {
            return;
        }


        // --------------------------------------------------
        // Add user message
        // --------------------------------------------------

        setMessages(
            previous => [
                ...previous,
                {
                    role: "user",
                    content: trimmedQuestion,
                },
            ]
        );


        setQuestion("");

        setLoading(true);


        try {

            const response =
                await fetch(
                    "/api/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body: JSON.stringify({
                            question:
                                trimmedQuestion,
                        }),
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `HTTP ${response.status}`
                );
            }


            const data =
                await response.json();


            // --------------------------------------------------
            // Add assistant response
            // --------------------------------------------------

            setMessages(
                previous => [
                    ...previous,
                    {
                        role: "assistant",

                        content:
                            data.answer ||
                            "No answer was generated.",

                        citations:
                            data.citations ||
                            [],
                    },
                ]
            );

        } catch (error) {

            console.error(
                "Chat request failed:",
                error
            );


            setMessages(
                previous => [
                    ...previous,
                    {
                        role: "assistant",

                        content:
                            "Unable to connect to the Hybrid RAG backend.",
                    },
                ]
            );

        } finally {

            setLoading(false);
        }
    }


    function handleKeyDown(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();
        }
    }


    function clearChat() {

        setMessages([]);
    }


    return (

        <div className="app">

            {/* ==================================================
                HEADER
            ================================================== */}

            <header className="header">

                <div>

                    <h1>
                        Hybrid RAG Assistant
                    </h1>

                    <p>
                        FAISS + Neo4j + OpenAI
                    </p>

                </div>


                <button
                    className="clear-button"
                    onClick={clearChat}
                >
                    Clear
                </button>

            </header>


            {/* ==================================================
                CHAT
            ================================================== */}

            <main className="chat-container">

                {messages.length === 0 && (

                    <div className="welcome">

                        <h2>
                            Welcome
                        </h2>

                        <p>
                            Ask a question about
                            your organization's
                            policies and documents.
                        </p>

                        <div className="example-question">

                            Try:

                            <br />

                            <strong>
                                What is the process
                                for laptop request?
                            </strong>

                        </div>

                    </div>

                )}


                {messages.map(
                    (message, index) => (

                        <div
                            key={index}
                            className={
                                `message ${message.role}`
                            }
                        >

                            <div
                                className="message-content"
                            >

                                {message.content}

                            </div>


                            {/* ==================================================
                                SOURCES
                            ================================================== */}

                            {
                                message.citations &&
                                message.citations.length > 0 && (

                                    <details>

                                        <summary>
                                            Sources
                                        </summary>

                                        <div
                                            className="sources"
                                        >

                                            {
                                                message
                                                    .citations
                                                    .map(
                                                        (
                                                            citation,
                                                            sourceIndex
                                                        ) => (

                                                            <div
                                                                key={
                                                                    sourceIndex
                                                                }
                                                                className="source"
                                                            >

                                                                {
                                                                    typeof citation ===
                                                                    "string"
                                                                        ? citation
                                                                        : JSON.stringify(
                                                                            citation
                                                                        )
                                                                }

                                                            </div>

                                                        )
                                                    )
                                            }

                                        </div>

                                    </details>

                                )
                            }

                        </div>

                    )
                )}


                {/* ==================================================
                    LOADING
                ================================================== */}

                {loading && (

                    <div
                        className="message assistant"
                    >

                        <div
                            className="message-content loading"
                        >

                            Searching FAISS and Neo4j...

                        </div>

                    </div>

                )}

            </main>


            {/* ==================================================
                INPUT
            ================================================== */}

            <footer className="input-area">

                <textarea
                    value={question}
                    onChange={
                        event =>
                            setQuestion(
                                event.target.value
                            )
                    }
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a policy question..."
                    rows={2}
                    disabled={loading}
                />


                <button
                    onClick={sendQuestion}
                    disabled={
                        loading ||
                        !question.trim()
                    }
                >

                    {loading
                        ? "Searching..."
                        : "Send"
                    }

                </button>

            </footer>

        </div>
    );
}


export default App;
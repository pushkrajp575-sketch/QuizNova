import streamlit as st
import random
import time
from questions import QUESTIONS
from streamlit_autorefresh import st_autorefresh

# ------------------------------------------------------------
# PAGE
# ------------------------------------------------------------
st.set_page_config(
    page_title="QuizNova",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------
# STYLE
# No HTML cards are used in the application body. This avoids
# raw <div> / HTML code appearing in the UI.
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

:root {
    --yellow: #ffd21a;
    --yellow2: #ffb300;
    --blue: #2563eb;
    --blue2: #0ea5e9;
    --navy: #17306b;
    --text: #17306b;
    --muted: #64748b;
    --line: #dbe6f4;
    --white: #ffffff;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(255,210,26,.24), transparent 27%),
        radial-gradient(circle at 92% 8%, rgba(37,99,235,.13), transparent 24%),
        linear-gradient(135deg, #fffdf1 0%, #fff8cf 43%, #f3f8ff 100%);
    color: var(--text);
}

header, footer, #MainMenu, [data-testid="stToolbar"] {
    visibility: hidden;
    display: none;
}

.block-container {
    max-width: 1180px;
    padding-top: 28px;
    padding-bottom: 60px;
}

/* Typography */
h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] {
    font-family: Inter, sans-serif !important;
    color: var(--text) !important;
}

h1 {
    font-family: "Space Grotesk", sans-serif !important;
    text-align: center;
    font-size: clamp(2.8rem, 6vw, 5rem) !important;
    font-weight: 800 !important;
    letter-spacing: -3px !important;
    margin-bottom: 0 !important;
    background: linear-gradient(90deg, #ffd600 0%, #ffad00 45%, #2563eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2 {
    font-family: "Space Grotesk", sans-serif !important;
    font-size: 1.55rem !important;
}

h3 {
    font-family: "Space Grotesk", sans-serif !important;
}

/* Native Streamlit bordered containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.88);
    border: 1px solid rgba(37,99,235,.12);
    border-radius: 22px;
    box-shadow: 0 16px 45px rgba(37,99,235,.08);
}

/* Text input */
.stTextInput input {
    background: #fff !important;
    color: #17306b !important;
    border: 1.5px solid #d4dfef !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    padding: 12px 14px !important;
}
.stTextInput input:focus {
    border-color: #ffd21a !important;
    box-shadow: 0 0 0 3px rgba(255,210,26,.18) !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: #fff !important;
    color: #17306b !important;
    border: 1.5px solid #d4dfef !important;
    border-radius: 14px !important;
}
div[data-baseweb="select"] span {
    color: #17306b !important;
}

/* Radio */
.stRadio label {
    color: #17306b !important;
    background: #fff !important;
    border: 1px solid #dbe6f4 !important;
    border-radius: 12px !important;
    padding: 9px 13px !important;
}
.stRadio label p, .stRadio label span {
    color: #17306b !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 13px !important;
    border: 1.5px solid #d5e0ee !important;
    background: #fff !important;
    color: #17306b !important;
    font-weight: 700 !important;
    transition: .18s ease !important;
}
.stButton > button:hover {
    border-color: #ffd21a !important;
    background: #fff9df !important;
    color: #17306b !important;
    transform: translateY(-1px);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #ffd600, #ffb300) !important;
    color: #172554 !important;
    border: 0 !important;
    box-shadow: 0 8px 25px rgba(255,185,0,.22);
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #ffe13b, #ffc21a) !important;
}

/* Progress */
.stProgress > div {
    background: #e7edf6 !important;
    border-radius: 20px !important;
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #ffd600, #2563eb) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,.78);
    border: 1px solid #dbe6f4;
    border-radius: 16px;
    padding: 12px;
}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    color: #17306b !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Small helper text */
.helper {
    color: #64748b;
    text-align: center;
    margin-top: 4px;
}
.badge {
    display: inline-block;
    background: #fff5b8;
    color: #8a5a00;
    border: 1px solid #ffd21a;
    border-radius: 999px;
    padding: 5px 12px;
    font-size: .78rem;
    font-weight: 800;
}


/* Question Map */
.question-map-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 10px;
    margin: 10px 0 14px 0;
}

.qmap-box {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 48px;
    border-radius: 12px;
    border: 1.5px solid #d7e1ef;
    background: #ffffff;
    color: #17306b !important;
    text-decoration: none !important;
    font-size: 1.05rem;
    font-weight: 800;
    transition: all .16s ease;
    box-sizing: border-box;
}

.qmap-box:hover {
    transform: translateY(-1px);
    text-decoration: none !important;
}

.qmap-box.answered {
    background: #dcfce7;
    border-color: #22c55e;
    color: #15803d !important;
    box-shadow: 0 4px 12px rgba(34, 197, 94, .12);
}

.qmap-box.answered:hover {
    background: #bbf7d0;
}

.qmap-box.current {
    background: #dbeafe;
    border: 2px solid #2563eb;
    color: #1d4ed8 !important;
    box-shadow: 0 5px 16px rgba(37, 99, 235, .20);
}

.qmap-box.current:hover {
    background: #bfdbfe;
}

.qmap-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 12px 16px;
    align-items: center;
    color: #475569;
    font-size: .82rem;
    font-weight: 600;
}

.qmap-legend span {
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.legend-dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    display: inline-block;
}

.answered-dot {
    background: #22c55e;
}

.current-dot {
    background: #2563eb;
}

.unanswered-dot {
    background: #cbd5e1;
    border: 1px solid #94a3b8;
}

@media (max-width: 600px) {
    .question-map-grid {
        gap: 7px;
    }

    .qmap-box {
        min-height: 42px;
        font-size: .95rem;
        border-radius: 10px;
    }

    .qmap-legend {
        gap: 8px 12px;
        font-size: .76rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# STATE
# ------------------------------------------------------------
defaults = {
    "page": "home",
    "name": "",
    "category": "Python",
    "difficulty": "Easy",
    "mode": "Practice",
    "duration": 10,
    "questions": [],
    "current": 0,
    "answers": {},
    "score": 0,
    "start_time": None,
    "quiz_id": 0,
    "submitted": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Keep the selected question in the URL so the custom question map
# can jump directly to any question.
if st.session_state.page == "quiz" and "question" in st.query_params:
    try:
        requested_question = int(st.query_params["question"]) - 1
        if 0 <= requested_question < len(st.session_state.questions):
            st.session_state.current = requested_question
    except (ValueError, TypeError):
        pass

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def start_quiz():
    available = [
        q for q in QUESTIONS
        if q["category"] == st.session_state.category
        and q["difficulty"] == st.session_state.difficulty
    ]

    if len(available) < 10:
        st.error("This category and difficulty needs at least 10 questions.")
        return

    st.session_state.questions = random.sample(available, 10)
    st.session_state.current = 0
    st.session_state.answers = {}
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.quiz_id += 1
    st.session_state.submitted = False
    st.session_state.page = "quiz"
    st.query_params.clear()
    st.rerun()


def calculate_score():
    return sum(
        1
        for i, q in enumerate(st.session_state.questions)
        if st.session_state.answers.get(i) == q["answer"]
    )


def submit_quiz():
    st.session_state.score = calculate_score()
    st.session_state.submitted = True
    st.session_state.page = "result"
    st.rerun()


def choose_answer(index, option):
    st.session_state.answers[index] = option
    st.rerun()


def question_status(index):
    if index == st.session_state.current:
        return "🔵"
    if index in st.session_state.answers:
        return "🟢"
    return "⚪"


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------
def home_page():
    st.title("QUIZNOVA")
    st.markdown(
        "<p class='helper'>Challenge your knowledge. Learn something new.</p>",
        unsafe_allow_html=True
    )

    st.write("")

    with st.container(border=True):
        # Name first
        st.markdown("### Let's see what you can do! 👋")
        name = st.text_input(
            "Your name",
            value=st.session_state.name,
            placeholder="Enter your name",
            label_visibility="collapsed"
        )

        if name.strip():
            st.info(f"Ready, {name.strip()}? Let's see what you can do! ⚡")

        st.write("")

        c1, c2 = st.columns(2)

        with c1:
            category = st.selectbox(
                "📚 Category",
                ["Python", "DBMS", "Computer Networks", "Artificial Intelligence"],
                index=["Python", "DBMS", "Computer Networks", "Artificial Intelligence"].index(
                    st.session_state.category
                )
            )

        with c2:
            difficulty = st.selectbox(
                "🎯 Difficulty",
                ["Easy", "Medium", "Hard"],
                index=["Easy", "Medium", "Hard"].index(
                    st.session_state.difficulty
                )
            )

        st.write("")

        st.markdown("### ⏱ Quiz mode")

        mode = st.radio(
            "Choose how you want to play",
            ["Practice — No timer", "Timed — Countdown"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if mode.startswith("Timed"):
            duration = st.select_slider(
                "Time limit",
                options=[5, 10, 15, 20, 30],
                value=10,
                format_func=lambda x: f"{x} minutes"
            )
        else:
            duration = 10

        st.caption("10 random questions will be selected from your chosen category and difficulty.")

        st.write("")

        if st.button("⚡ START QUIZ", type="primary", use_container_width=True):
            if not name.strip():
                st.warning("Please enter your name first.")
            else:
                st.session_state.name = name.strip()
                st.session_state.category = category
                st.session_state.difficulty = difficulty
                st.session_state.mode = "Timed" if mode.startswith("Timed") else "Practice"
                st.session_state.duration = duration
                start_quiz()

    st.write("")
    st.subheader("Explore Categories")

    category_info = [
        ("🐍", "Python", "Programming & coding"),
        ("🗄️", "DBMS", "Databases & SQL"),
        ("🌐", "Networks", "Computer networking"),
        ("🤖", "Artificial Intelligence", "AI & machine learning"),
    ]

    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, category_info):
        with col:
            with st.container(border=True):
                st.markdown(f"### {icon}")
                st.markdown(f"**{title}**")
                st.caption(desc)

    st.write("")
    st.markdown(
        "<p class='helper'>QUIZNOVA • Python-powered quiz platform</p>",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# TIMER
# ------------------------------------------------------------
def timer_block():
    if st.session_state.mode != "Timed":
        return

    st_autorefresh(
        interval=1000,
        key=f"timer_{st.session_state.quiz_id}"
    )

    elapsed = int(time.time() - st.session_state.start_time)
    total_seconds = st.session_state.duration * 60
    remaining = max(0, total_seconds - elapsed)

    mins = remaining // 60
    secs = remaining % 60

    if remaining <= 30:
        st.error(f"⏰ Time remaining: {mins:02d}:{secs:02d}")
    elif remaining <= 60:
        st.warning(f"⏰ Time remaining: {mins:02d}:{secs:02d}")
    else:
        st.info(f"⏱ Time remaining: {mins:02d}:{secs:02d}")

    if remaining == 0:
        submit_quiz()


# ------------------------------------------------------------
# QUESTION MAP
# ------------------------------------------------------------
def question_map():
    with st.container(border=True):
        st.subheader("🧭 Question Map")
        st.caption("Jump to any question.")

        total = len(st.session_state.questions)
        answered = len(st.session_state.answers)
        current = st.session_state.current

        # Custom clickable boxes give us proper green/blue/grey states.
        boxes = []
        for i in range(total):
            if i == current:
                status = "current"
            elif i in st.session_state.answers:
                status = "answered"
            else:
                status = "unanswered"

            boxes.append(
                f'<a class="qmap-box {status}" href="?question={i + 1}" '
                f'title="Go to question {i + 1}">{i + 1}</a>'
            )

        st.markdown(
            '<div class="question-map-grid">' + "".join(boxes) + "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="qmap-legend">
                <span><i class="legend-dot answered-dot"></i> Answered</span>
                <span><i class="legend-dot current-dot"></i> Current</span>
                <span><i class="legend-dot unanswered-dot"></i> Unanswered</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Answered", f"{answered}/{total}")
        with m2:
            st.metric("Unanswered", total - answered)


# ------------------------------------------------------------
# QUIZ
# ------------------------------------------------------------
def quiz_page():
    timer_block()

    questions = st.session_state.questions
    current = st.session_state.current
    total = len(questions)
    q = questions[current]

    left, right = st.columns([2.6, 1], gap="large")

    with left:
        st.caption(
            f"{st.session_state.category.upper()}  •  "
            f"{st.session_state.difficulty.upper()}  •  "
            f"QUESTION {current + 1} / {total}"
        )

        st.progress((current + 1) / total)

        with st.container(border=True):
            st.subheader(q["question"])

            selected = st.session_state.answers.get(current)

            # Answer buttons, 2 x 2
            option_cols = st.columns(2)

            for i, option in enumerate(q["options"]):
                with option_cols[i % 2]:
                    prefix = "✓  " if selected == option else ""
                    if st.button(
                        f"{prefix}{option}",
                        key=f"option_{st.session_state.quiz_id}_{current}_{i}",
                        use_container_width=True
                    ):
                        choose_answer(current, option)

        st.write("")

        nav1, nav2, nav3 = st.columns([1, 1, 1])

        with nav1:
            if current > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.current -= 1
                    st.rerun()

        with nav2:
            if current < total - 1:
                if st.button("Next →", type="primary", use_container_width=True):
                    st.session_state.current += 1
                    st.rerun()

        with nav3:
            if st.button("🏁 Final Submit", type="primary", use_container_width=True):
                submit_quiz()

        if len(st.session_state.answers) < total:
            st.warning(
                f"{total - len(st.session_state.answers)} question(s) are unanswered. "
                "You can still submit, or jump back using the Question Map."
            )

    with right:
        question_map()


# ------------------------------------------------------------
# RESULT
# ------------------------------------------------------------
def result_page():
    total = len(st.session_state.questions)
    score = calculate_score()
    answered = len(st.session_state.answers)
    unanswered = total - answered
    percentage = int(score / total * 100)

    st.title("QUIZ COMPLETE")
    st.markdown(
        "<p class='helper'>Here's how you performed.</p>",
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown(f"### 👤 {st.session_state.name}")
        st.metric("Score", f"{score} / {total}")
        st.metric("Percentage", f"{percentage}%")

        if percentage == 100:
            st.success("🏆 Perfect score!")
        elif percentage >= 80:
            st.success("🔥 Excellent performance!")
        elif percentage >= 60:
            st.info("👏 Great job!")
        elif percentage >= 40:
            st.warning("💪 Keep practicing!")
        else:
            st.error("📚 Keep learning and try again!")

    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Answered", answered)
    with c2:
        st.metric("Unanswered", unanswered)
    with c3:
        st.metric("Quiz Mode", st.session_state.mode)

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("📋 Review Answers", type="primary", use_container_width=True):
            st.session_state.page = "review"
            st.rerun()

    with c2:
        if st.button("🔄 New Quiz", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


# ------------------------------------------------------------
# REVIEW
# ------------------------------------------------------------
def review_page():
    st.title("ANSWER REVIEW")
    st.markdown(
        "<p class='helper'>See your answer, the correct answer, and your result.</p>",
        unsafe_allow_html=True
    )

    for i, q in enumerate(st.session_state.questions):
        selected = st.session_state.answers.get(i)

        with st.container(border=True):
            st.caption(f"QUESTION {i + 1}")

            st.markdown(f"### {q['question']}")

            if selected is None:
                st.warning("⚪ Not answered")
                st.markdown(f"**Correct answer:** {q['answer']}")
            elif selected == q["answer"]:
                st.success(f"✅ Correct — {selected}")
            else:
                st.error(f"❌ Your answer — {selected}")
                st.info(f"Correct answer — {q['answer']}")

    st.write("")

    if st.button("⚡ TAKE ANOTHER QUIZ", type="primary", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


# ------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "quiz":
    quiz_page()
elif st.session_state.page == "result":
    result_page()
elif st.session_state.page == "review":
    review_page()

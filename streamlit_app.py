"""
Signal Integrity Assessment™
Streamlit Application - Main Entry Point
"""
import streamlit.components.v1 as components
import streamlit as st
from datetime import date
import json
from pathlib import Path
def render_brand_header(title: str, subtitle: str | None = None):
    """Quiet-luxury header: small logo top-left, title to the right."""
    left, right = st.columns([1, 6], vertical_alignment="center")

    with left:
        if LOGO_MONO_PATH.exists():
            st.image(str(LOGO_MONO_PATH), width=95)
        else:
            st.markdown("")

    with right:
        st.markdown(f"# {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")

def render_footer(show_prepared_by: bool = False):
    """Discreet footer on every screen."""
    extra = f"<br><span style='font-size:9px;'>{FOOTER_SUBTEXT}</span>" if show_prepared_by else ""
    st.markdown(
        f"""
        <style>
          .sw-footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            padding: 8px 0;
            text-align: center;
            color: #9ca3af;
            font-size: 10px;
            background: rgba(255,255,255,0.85);
            border-top: 1px solid #e5e7eb;
            z-index: 999;
          }}
        </style>
        <div class="sw-footer">{FOOTER_TEXT}{extra}</div>
        """,
        unsafe_allow_html=True
    )

LOGO_MONO_PATH = Path("assets/southwind_logo_mono_navy.png")

FOOTER_TEXT = "Southwind Planning • Readiness Is Not a Plan. It’s a Capability."
FOOTER_SUBTEXT = "Prepared by Mike McCracken • 2026"

APP_VERSION = "2026-01-28b"

st.set_page_config(
    page_title="Signal Integrity Assessment™",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# --- Session state initialization (must run before any page renders) ---
if "page" not in st.session_state:
    st.session_state.page = "metadata"

if "org_name" not in st.session_state:
    st.session_state.org_name = ""

if "assessment_date" not in st.session_state:
    from datetime import date
    st.session_state.assessment_date = date.today()

if "current_lifeline" not in st.session_state:
    st.session_state.current_lifeline = 0

if "responses" not in st.session_state:
    st.session_state.responses = {}

# ✅ GLOBAL TAGLINE (safe, top-level, not inside any function)
st.markdown(
    "<p class='tagline'>Readiness Is Not a Plan. It's a Capability.</p>",
    unsafe_allow_html=True
)

# Optional debug/version markers (temporary)
st.sidebar.caption(f"Version: {APP_VERSION}")
st.sidebar.error("MARKER: 2026-01-28b")

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    h1 {
        font-weight: 300;
        letter-spacing: 2px;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .tagline {
        font-style: italic;
        color: #475569;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    h1 {
        font-weight: 300;
        letter-spacing: 2px;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h2 {
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .tagline {
        font-size: 1.1rem;
        color: #1e293b;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-style: italic;
    }
    .stButton > button {
        background-color: #1e293b;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #334155;
    }
    .lifeline-header {
        background-color: #f8fafc;
        padding: 1rem;
        border-left: 4px solid #64748b;
        margin-bottom: 1rem;
    }
    .question-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        border-radius: 4px;
        animation: fadeIn 0.3s ease-in;
    }
    .progress-text {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    a[href*="mailto"]:hover {
        background-color: #334155 !important;
    }
</style>
<script>
    // Scroll to top when navigating between lifelines
    window.parent.document.querySelector('.main').scrollTo(0, 0);
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'metadata'
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'current_lifeline' not in st.session_state:
    st.session_state.current_lifeline = 0

# Assessment questions structure
LIFELINES = {
    0: {
        'name': 'Leadership Awareness',
        'questions': [
            'How do you currently know what is working and what is under strain across critical operations?',
            'When priorities compete, how do you know which dependencies will fail first?',
            'What would become visible only under sustained pressure or resource constraints?',
            'How do leaders verify that operational assumptions are still valid?',
            'What information do you rely on that has not been independently confirmed in the past 6 months?'
        ]
    },
    1: {
        'name': 'Operational Dependencies',
        'questions': [
            'What critical processes depend on specific individuals to function properly?',
            'Which vendor or supplier relationships have not been stress-tested in the past 12 months?',
            'What workarounds have become standard operating procedure?',
            'What happens if your top three operational experts are unavailable for two weeks?',
            'Which systems or processes lack documented backup procedures?'
        ]
    },
    2: {
        'name': 'Decision Clarity',
        'questions': [
            'When urgent decisions are needed, how do you verify you\'re working from current information?',
            'What decisions are currently being delayed due to incomplete information or competing priorities?',
            'Where do informal channels override formal decision-making processes?',
            'How do you know when a decision is based on accurate versus assumed information?',
            'What percentage of major decisions are made with verified data versus historical assumptions?'
        ]
    },
    3: {
        'name': 'Resource Resilience',
        'questions': [
            'Which resources (people, systems, suppliers) operate with no viable backup or alternative?',
            'What capabilities exist primarily because of individual expertise rather than documented process?',
            'Where is organizational capacity being sustained through overtime, heroics, or goodwill?',
            'What critical resources are operating at or above sustainable capacity?',
            'Which resource constraints are currently being managed through workarounds?'
        ]
    },
    4: {
        'name': 'Information Flow',
        'questions': [
            'How do you know when critical information is not reaching decision-makers?',
            'What signals of emerging problems currently go unnoticed or unreported?',
            'Where does "everything is fine" actually mean "someone is handling it quietly"?',
            'How is bad news communicated upward in your organization?',
            'What information do you wish you had real-time visibility into?'
        ]
    }
}

SIGNAL_TYPES = [
    'Observed - Direct, current evidence',
    'Assumed - Believed but not verified',
    'Historical - Once true, not recently tested',
    'Compensated - Held together by people/workarounds'
]


def show_metadata_page():
    """Metadata collection page"""

    render_brand_header(
        "Signal Integrity Assessment™",
        "A structured executive diagnostic on decision information reliability."
    )
    render_footer(show_prepared_by=False)

    st.markdown(
        "*A structured executive diagnostic that reveals where leadership decisions are supported by verified information—and where they depend on assumptions, workarounds, or individual effort.*"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        org_name = st.text_input(
            "Organization Name",
            value=st.session_state.get("org_name", ""),
            help="Enter your organization or company name"
        )

    with col2:
        assessment_date = st.date_input(
            "Assessment Date",
            value=st.session_state.get("assessment_date", date.today())
        )

    st.session_state["org_name"] = org_name
    st.session_state["assessment_date"] = assessment_date

    
    st.markdown('---')
    
    st.markdown("""
    ### What to Expect
    
    This assessment examines 5 critical business lifelines:
    - **Leadership Awareness** - Quality of operational visibility
    - **Operational Dependencies** - Key process and resource dependencies
    - **Decision Clarity** - Information quality for decisions
    - **Resource Resilience** - Backup capacity and sustainability
    - **Information Flow** - Communication and signal detection
    
    **Time required:** Approximately 15 minutes
    
    **Output:** A single-page executive artifact showing where your decisions rest on verified information versus assumptions.
    """)
    
    st.markdown('---')
    
    if st.button('Begin Assessment', use_container_width=True):
        if org_name.strip():
            st.session_state.org_name = org_name
            st.session_state.assessment_date = assessment_date
            st.session_state.page = 'assessment'
            st.session_state.current_lifeline = 0
            st.session_state.force_scroll_top = True
            st.rerun()
        else:
            st.error('Please enter an organization name to continue.')

def scroll_to_top():
    components.html(
        """
        <script>
          // Try a few targets Streamlit uses, then fall back to window
          const targets = [
            window,
            document.documentElement,
            document.body,
            window.parent,
            window.parent?.document?.documentElement,
            window.parent?.document?.body,
            window.parent?.document?.querySelector('section.main'),
            window.parent?.document?.querySelector('[data-testid="stAppViewContainer"]'),
            window.parent?.document?.querySelector('[data-testid="stApp"]'),
          ].filter(Boolean);

          targets.forEach(t => {
            try {
              if (t.scrollTo) t.scrollTo(0, 0);
              if (t.scrollTop !== undefined) t.scrollTop = 0;
            } catch(e) {}
          });
        </script>
        """,
        height=0,
    )

def show_assessment_page():
    lifeline_idx = st.session_state.get("current_lifeline", 0)

    # keep index in range
    if lifeline_idx < 0:
        lifeline_idx = 0
        st.session_state.current_lifeline = 0
    if lifeline_idx >= len(LIFELINES):
        lifeline_idx = len(LIFELINES) - 1
        st.session_state.current_lifeline = lifeline_idx

    # Force scroll-to-top AFTER rerun (on new render)
    if st.session_state.get("force_scroll_top", False):
        scroll_to_top()
        st.session_state.force_scroll_top = False

    lifeline = LIFELINES[lifeline_idx]
    # Header
    st.title("Signal Integrity Assessment™")
    st.markdown(f"**{st.session_state.org_name}** • {st.session_state.assessment_date}")

    # Progress indicator
    progress = (lifeline_idx + 1) / len(LIFELINES)
    st.progress(progress)
    st.markdown(
    f"Business Lifeline {lifeline_idx + 1} of {len(LIFELINES)} • {int(progress * 100)}% Complete"
    )

    st.markdown("---")

    # Lifeline header
    st.subheader(f"🎯 {lifeline.get('name', 'Business Lifeline')}")

    # Questions
    lifeline_idx = st.session_state.get("current_lifeline", 0)
    lifeline = LIFELINES[lifeline_idx]
    questions = lifeline.get("questions", [])

    questions = lifeline.get("questions", [])

    for q_idx, question in enumerate(questions):
        key_base = f"{lifeline_idx}_{q_idx}"

        st.markdown("---")
        st.markdown(f"**Question {q_idx + 1} of {len(questions)}**")
        st.markdown(f"*{question}*")

        response = st.text_area(
        "Your Response",
        value=st.session_state.responses.get(f"{key_base}_response", ""),
        key=f"{key_base}_response_input",
        height=110,
    )

        signal_type = st.selectbox(
        "Signal Classification",
        options=SIGNAL_TYPES,
        index=SIGNAL_TYPES.index(
            st.session_state.responses.get(f"{key_base}_signal", SIGNAL_TYPES[0])
        ),
        key=f"{key_base}_signal_input",
    )

        # Save to session state
        st.session_state.responses[f"{key_base}_response"] = response
        st.session_state.responses[f"{key_base}_signal"] = signal_type

    
    st.markdown("---")

     # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("← Previous Lifeline", use_container_width=True):
            st.session_state.current_lifeline -= 1
            st.session_state.force_scroll_top = True
            st.rerun()

    with col2:
        if st.button("Save Progress", use_container_width=True):
            st.success("Progress saved!")

    with col3:
        if lifeline_idx < len(LIFELINES) - 1:
            if st.button("Next Lifeline →", use_container_width=True):
                st.session_state.current_lifeline += 1
                st.session_state.force_scroll_top = True
                st.rerun()
        else:
            if st.button("Generate Assessment →", use_container_width=True, type="primary"):
                st.session_state.page = "results"
                st.session_state.force_scroll_top = True
                st.rerun()


def main():
    """Main application router"""
    if st.session_state.page == 'metadata':
        show_metadata_page()
    elif st.session_state.page == 'assessment':
        show_assessment_page()
    elif st.session_state.page == 'results':
        # Import and show results page
        from results import show_results_page
        show_results_page()


if __name__ == '__main__':
    main()


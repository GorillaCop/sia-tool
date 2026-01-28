"""
Signal Integrity Assessment™
Streamlit Application - Main Entry Point
"""

import streamlit as st
from datetime import date
import json

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Signal Integrity Assessment™",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APP_VERSION = "2026-01-28a"
st.sidebar.error("MARKER: 2026-01-28a")
st.sidebar.caption(f"Version: {APP_VERSION}")
st.sidebar.write("RUNNING COMMIT MARKER: LIFELINES_SINGLE_2026-01-28")

# Page configuration
st.set_page_config(
    page_title="Signal Integrity Assessment™",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.sidebar.error("MARKER: 2026-01-28a")

st.sidebar.caption(f"Version: {APP_VERSION}")
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
    }
    .progress-text {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
</style>
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
            'When urgent decisions are needed, how do you verify you're working from current information?',
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
    st.title('Signal Integrity Assessment™')
    st.markdown('*A structured executive diagnostic that reveals where leadership decisions are supported by verified information—and where they depend on assumptions, workarounds, or individual effort.*')
    
    st.markdown('---')
    
    col1, col2 = st.columns(2)
    
    with col1:
        org_name = st.text_input(
            'Organization Name',
            value=st.session_state.get('org_name', ''),
            help='Enter your organization or company name'
        )
    
    with col2:
        assessment_date = st.date_input(
            'Assessment Date',
            value=st.session_state.get('assessment_date', date.today())
        )
    
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
            st.rerun()
        else:
            st.error('Please enter an organization name to continue.')


def show_assessment_page():
    """Main assessment page with questions"""
    lifeline_idx = st.session_state.current_lifeline
    lifeline = LIFELINES[lifeline_idx]
    
    # Header
    st.title('Signal Integrity Assessment™')
    st.markdown(f"**{st.session_state.org_name}** • {st.session_state.assessment_date}")
    
    # Progress indicator
    progress = (lifeline_idx + 1) / len(LIFELINES)
    st.progress(progress)
    st.markdown(f'<p class="progress-text">Business Lifeline {lifeline_idx + 1} of {len(LIFELINES)} • {int(progress * 100)}% Complete</p>', unsafe_allow_html=True)
    
    st.markdown('---')
    
    # Lifeline header
    st.markdown(f'<div class="lifeline-header"><h2>🎯 {lifeline["name"]}</h2></div>', unsafe_allow_html=True)
    
    # Questions
    for q_idx, question in enumerate(lifeline['questions']):
        key_base = f'{lifeline_idx}_{q_idx}'
        
        st.markdown(f'<div class="question-container">', unsafe_allow_html=True)
        st.markdown(f'**Question {q_idx + 1} of {len(lifeline["questions"])}**')
        st.markdown(f'*{question}*')
        
        # Response text area
        response = st.text_area(
            'Your Response',
            value=st.session_state.responses.get(f'{key_base}_response', ''),
            key=f'{key_base}_response_input',
            height=100,
            help='Provide a specific, operational response'
        )
        
        # Signal classification
        signal_type = st.selectbox(
            'Signal Classification',
            options=SIGNAL_TYPES,
            index=SIGNAL_TYPES.index(st.session_state.responses.get(f'{key_base}_signal', SIGNAL_TYPES[0])) if f'{key_base}_signal' in st.session_state.responses else 0,
            key=f'{key_base}_signal_input',
            help='How would you classify the quality of information behind this response?'
        )
        
        # Save to session state
        st.session_state.responses[f'{key_base}_response'] = response
        st.session_state.responses[f'{key_base}_signal'] = signal_type
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('---')
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if lifeline_idx > 0:
            if st.button('← Previous Lifeline', use_container_width=True):
                st.session_state.current_lifeline -= 1
                st.rerun()
    
    with col2:
        if st.button('Save Progress', use_container_width=True):
            st.success('Progress saved!')
    
    with col3:
        if lifeline_idx < len(LIFELINES) - 1:
            if st.button('Next Lifeline →', use_container_width=True):
                st.session_state.current_lifeline += 1
                st.rerun()
        else:
            if st.button('Generate Assessment →', use_container_width=True, type='primary'):
                st.session_state.page = 'results'
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

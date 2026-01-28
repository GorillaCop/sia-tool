"""
Signal Integrity Assessment™
Results Page with Signal Map Visualization
"""

import streamlit as st
import plotly.graph_objects as go
from collections import Counter
import json


def analyze_responses():
    """Analyze responses and generate insights"""
    lifeline_analysis = {}
    
    # Define lifeline names
    lifelines = {
        0: 'Leadership Awareness',
        1: 'Operational Dependencies',
        2: 'Decision Clarity',
        3: 'Resource Resilience',
        4: 'Information Flow'
    }
    
    for lifeline_idx, lifeline_name in lifelines.items():
        signals = []
        
        # Count each signal type for this lifeline
        for q_idx in range(5):  # 5 questions per lifeline
            key = f'{lifeline_idx}_{q_idx}_signal'
            if key in st.session_state.responses:
                signal = st.session_state.responses[key].split(' - ')[0]  # Get just "Observed", etc.
                signals.append(signal)
        
        if signals:
            signal_counts = Counter(signals)
            total = len(signals)
            
            # Calculate percentages
            observed_pct = (signal_counts.get('Observed', 0) / total) * 100
            compensated_pct = (signal_counts.get('Compensated', 0) / total) * 100
            fragile_pct = ((signal_counts.get('Assumed', 0) + signal_counts.get('Historical', 0)) / total) * 100
            
            # Determine status
            if observed_pct >= 60:
                status = 'SOLID'
                description = 'Largely supported by observed signals with current evidence.'
            elif compensated_pct >= 40:
                status = 'FRAGILE'
                description = 'Stability depends on individual effort and informal fixes.'
            elif fragile_pct >= 60:
                status = 'CONDITIONAL'
                description = 'Confidence appears to rest on belief or outdated verification.'
            else:
                status = 'MIXED'
                description = 'Shows varied signal patterns requiring attention.'
            
            lifeline_analysis[lifeline_name] = {
                'signals': signal_counts,
                'status': status,
                'description': description,
                'observed_pct': observed_pct,
                'compensated_pct': compensated_pct,
                'fragile_pct': fragile_pct
            }
    
    return lifeline_analysis


def create_signal_map(analysis):
    """Create Plotly signal map visualization"""
    
    # Prepare data for radial chart
    lifelines = list(analysis.keys())
    
    # Map status to numeric strength (for visualization)
    status_strength = {
        'SOLID': 100,
        'CONDITIONAL': 60,
        'MIXED': 40,
        'FRAGILE': 20
    }
    
    # Map status to colors
    status_colors = {
        'SOLID': '#10b981',      # Green
        'CONDITIONAL': '#f59e0b', # Amber
        'MIXED': '#6b7280',       # Gray
        'FRAGILE': '#ef4444'      # Red
    }
    
    # Get values and colors for each lifeline
    values = [status_strength[analysis[lf]['status']] for lf in lifelines]
    colors = [status_colors[analysis[lf]['status']] for lf in lifelines]
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=lifelines,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.2)',
        line=dict(color='rgb(99, 102, 241)', width=2),
        marker=dict(
            size=12,
            color=colors,
            line=dict(color='white', width=2)
        ),
        name='Signal Strength',
        hovertemplate='<b>%{theta}</b><br>Status: %{r}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                ticks='',
                showline=False
            ),
            angularaxis=dict(
                direction='clockwise',
                rotation=90
            )
        ),
        showlegend=False,
        title={
            'text': 'Signal Integrity Map',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial, sans-serif'}
        },
        height=500,
        margin=dict(l=80, r=80, t=80, b=80),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig


def create_network_signal_map(analysis):
    """Create network-style signal map (alternative visualization)"""
    import numpy as np
    
    # Central node at origin
    center_x, center_y = 0, 0
    
    # Calculate positions for lifeline nodes in a circle
    lifelines = list(analysis.keys())
    n = len(lifelines)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 2
    
    node_x = [center_x] + [radius * np.cos(angle) for angle in angles]
    node_y = [center_y] + [radius * np.sin(angle) for angle in angles]
    
    # Map status to line styles
    status_styles = {
        'SOLID': dict(width=4, dash='solid', color='#10b981'),
        'CONDITIONAL': dict(width=3, dash='dot', color='#f59e0b'),
        'MIXED': dict(width=2, dash='dash', color='#6b7280'),
        'FRAGILE': dict(width=2, dash='dash', color='#ef4444')
    }
    
    # Create figure
    fig = go.Figure()
    
    # Add edges (lines from center to each lifeline)
    for i, lifeline in enumerate(lifelines, 1):
        status = analysis[lifeline]['status']
        style = status_styles[status]
        
        fig.add_trace(go.Scatter(
            x=[center_x, node_x[i]],
            y=[center_y, node_y[i]],
            mode='lines',
            line=style,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add central node
    fig.add_trace(go.Scatter(
        x=[center_x],
        y=[center_y],
        mode='markers+text',
        marker=dict(size=30, color='#1e293b', line=dict(width=2, color='white')),
        text=['Leadership<br>Confidence'],
        textposition='middle center',
        textfont=dict(color='white', size=10),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add lifeline nodes
    for i, lifeline in enumerate(lifelines, 1):
        status = analysis[lifeline]['status']
        style = status_styles[status]
        
        fig.add_trace(go.Scatter(
            x=[node_x[i]],
            y=[node_y[i]],
            mode='markers+text',
            marker=dict(
                size=25,
                color=style['color'],
                line=dict(width=2, color='white')
            ),
            text=[lifeline.replace(' ', '<br>')],
            textposition='top center',
            textfont=dict(size=9),
            showlegend=False,
            hovertemplate=f'<b>{lifeline}</b><br>Status: {status}<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Signal Network Map',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis=dict(visible=False, range=[-3, 3]),
        yaxis=dict(visible=False, range=[-3, 3]),
        height=600,
        showlegend=False,
        hovermode='closest',
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def show_results_page():
    """Display results with visualizations"""
    st.title('Signal Integrity Assessment™')
    st.markdown(f"**{st.session_state.org_name}** • Assessment Date: {st.session_state.assessment_date}")
    
    st.markdown('---')
    
    # Analyze responses
    analysis = analyze_responses()
    
    # Section 1: Executive Observations
    st.header('Executive Observations')
    
    for lifeline_name, data in analysis.items():
        status_color = {
            'SOLID': '🟢',
            'CONDITIONAL': '🟡',
            'MIXED': '⚪',
            'FRAGILE': '🔴'
        }
        
        st.markdown(f"""
        **{status_color[data['status']]} {lifeline_name}**  
        *Status: {data['status']}*  
        {data['description']}
        """)
        st.markdown('---')
    
    # Section 2: Signal Map Visualization
    st.header('Signal Integrity Map')
    
    st.markdown("""
    This visualization shows the relative strength of each business lifeline. 
    Node colors indicate status, and the distance from center represents signal integrity.
    """)
    
    # Choose visualization style
    viz_type = st.radio(
        'Visualization Style',
        ['Radar Chart', 'Network Map'],
        horizontal=True
    )
    
    if viz_type == 'Radar Chart':
        fig = create_signal_map(analysis)
    else:
        fig = create_network_signal_map(analysis)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Section 3: Lifeline Integrity Grid
    st.header('Lifeline Integrity Grid')
    
    # Create table data
    table_data = []
    for lifeline_name, data in analysis.items():
        signals = data['signals']
        signal_pattern = ', '.join([f"{sig}: {count}" for sig, count in signals.items()])
        table_data.append({
            'Lifeline': lifeline_name,
            'Status': data['status'],
            'Signal Pattern': signal_pattern
        })
    
    st.table(table_data)
    
    # Section 4: Key Distinctions
    st.header('Key Distinctions')
    
    st.markdown("""
    **Signal Classifications Defined:**
    
    - **Observed:** Direct, current evidence. Leaders can point to specific, recent verification.
    
    - **Assumed:** Believed to be true but not recently confirmed. Often legacy knowledge.
    
    - **Historical:** Once verified but not tested under current conditions. May no longer hold.
    
    - **Compensated:** Stability depends on individual effort, workarounds, or heroics rather than documented process.
    """)
    
    # Section 5: Reflection Prompts
    st.header('Questions for Leadership Reflection')
    
    st.markdown("""
    - Which of these lifelines would matter most under sustained pressure or resource constraint?
    
    - Where is operational continuity currently dependent on specific individuals rather than documented process?
    
    - What information would you want independently verified before your next major decision?
    
    - Where might historical assumptions be vulnerable to current market or operational changes?
    """)
    
    st.markdown('---')
    
    # Closing Statement
    st.info("""
    **Note:** This assessment identifies where decision confidence is well supported by current evidence 
    and where additional verification may be needed. It does not prescribe solutions or evaluate leadership capability.
    
    For shared organizational clarity, this assessment is often reviewed in a facilitated mirror session.
    """)
    
    # Export options
    st.markdown('---')
    st.header('Export Options')
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('📄 Download PDF Report', use_container_width=True):
            st.info('PDF generation coming soon!')
    
    with col2:
        # Export data as JSON
        export_data = {
            'organization': st.session_state.org_name,
            'assessment_date': str(st.session_state.assessment_date),
            'analysis': {k: {
                'status': v['status'],
                'description': v['description'],
                'signals': dict(v['signals'])
            } for k, v in analysis.items()}
        }
        
       st.download_button(
    label='💾 Download Data (JSON)',
    data=json.dumps(export_data, indent=2),
    file_name=f'signal_integrity_{st.session_state.org_name}_{st.session_state.assessment_date}.json',
    mime='application/json',
    use_container_width=True
)

    
    # Restart option
    st.markdown('---')
    if st.button('← Start New Assessment', use_container_width=False):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

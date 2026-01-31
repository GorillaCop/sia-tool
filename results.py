"""
House of Cards Assessment™
Results Page with Signal Map Visualization
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from collections import Counter
import json
from pathlib import Path
import base64
from jinja2 import Template

def scroll_to_top():
    """Injects JavaScript to scroll the main content area to the top."""
    components.html(
        """
        <script>
            var mainSection = window.parent.document.querySelector('section.main');
            if (mainSection) {
                mainSection.scrollTo({ top: 0, behavior: 'auto' });
            }
        </script>
        """,
        height=0,
    )
    
LOGO_COLOR_PATH = Path("assets/southwind_logo_color_tuned.png")
TAGLINE = "Readiness Is Not a Plan. It’s a Capability."
CONTACT_LINE = "Southwind Planning • mike@southwindplanning.com • " + TAGLINE

def file_to_base64(path: Path) -> str | None:
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode("utf-8")

def fig_to_png_base64(fig) -> str | None:
    try:
        import plotly.io as pio
        png_bytes = pio.to_image(fig, format="png", width=1400, height=820, scale=2)
        return base64.b64encode(png_bytes).decode("utf-8")
    except Exception:
        return None

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
    
    # Prepare hover text with detailed information
    hover_texts = []
    for lf in lifelines:
        data = analysis[lf]
        signals = data['signals']
        hover_text = (
            f"<b>{lf}</b><br>"
            f"Status: <b>{data['status']}</b><br>"
            f"<br>Signal Breakdown:<br>"
            f"• Observed: {signals.get('Observed', 0)}<br>"
            f"• Assumed: {signals.get('Assumed', 0)}<br>"
            f"• Historical: {signals.get('Historical', 0)}<br>"
            f"• Compensated: {signals.get('Compensated', 0)}<br>"
            f"<br>{data['description']}"
        )
        hover_texts.append(hover_text)
    
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
        text=hover_texts,
        hovertemplate='%{text}<extra></extra>'
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
        plot_bgcolor='white',
        hovermode='closest',
        dragmode='pan'
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
    
    # Add lifeline nodes with enhanced hover
    for i, lifeline in enumerate(lifelines, 1):
        status = analysis[lifeline]['status']
        style = status_styles[status]
        signals = analysis[lifeline]['signals']
        
        # Create detailed hover text
        hover_text = (
            f"<b>{lifeline}</b><br>"
            f"Status: {status}<br>"
            f"<br>Signals:<br>"
            f"Observed: {signals.get('Observed', 0)}<br>"
            f"Assumed: {signals.get('Assumed', 0)}<br>"
            f"Historical: {signals.get('Historical', 0)}<br>"
            f"Compensated: {signals.get('Compensated', 0)}"
        )
        
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
            hovertext=hover_text,
            hoverinfo='text'
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
def build_executive_brief_html(org_name: str, assessment_date: str, analysis: dict, map_png_b64: str | None):
    logo_b64 = file_to_base64(LOGO_COLOR_PATH)

    strength = {"SOLID": 4, "CONDITIONAL": 3, "MIXED": 2, "FRAGILE": 1}
    strongest = max(analysis.items(), key=lambda kv: strength.get(kv[1]["status"], 0))
    weakest = min(analysis.items(), key=lambda kv: strength.get(kv[1]["status"], 9))
    strong_name, strong_data = strongest
    weak_name, weak_data = weakest

    framing = (
        f"In this assessment for <b>{org_name}</b>, the strongest signal integrity appears in "
        f"<b>{strong_name}</b> (<b>{strong_data['status']}</b>), while <b>{weak_name}</b> shows the highest fragility "
        f"(<b>{weak_data['status']}</b>)."
    )

    grid_rows = []
    for lf, data in analysis.items():
        sig = data["signals"]
        grid_rows.append({
            "lifeline": lf,
            "status": data["status"],
            "pattern": f"Observed {sig.get('Observed',0)} • Assumed {sig.get('Assumed',0)} • Historical {sig.get('Historical',0)} • Compensated {sig.get('Compensated',0)}"
        })

    template = Template(r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page { size: Letter; margin: 0.65in; }
  body { font-family: Arial, sans-serif; color: #111827; }
  .header { border-bottom: 1px solid #e5e7eb; padding-bottom: 10px; margin-bottom: 12px; }
  .logo { height: 44px; }
  .title { font-size: 22px; font-weight: 700; margin-top: 8px; }
  .subtitle { font-size: 12px; color: #374151; margin-top: 2px; }
  .meta { font-size: 11px; color: #6b7280; margin-top: 8px; }
  .framing { margin: 12px 0; font-size: 12.5px; line-height: 1.45; }
  .section-title { margin-top: 14px; font-weight: 700; font-size: 12.5px; }
  table { width: 100%; border-collapse: collapse; margin-top: 8px; }
  th, td { border: 1px solid #e5e7eb; padding: 7px; font-size: 11px; vertical-align: top; }
  th { background: #f9fafb; }
  .badge { font-weight: 700; }
  .SOLID { color: #065f46; }
  .CONDITIONAL { color: #92400e; }
  .MIXED { color: #374151; }
  .FRAGILE { color: #991b1b; }
  .map img { width: 100%; border: 1px solid #e5e7eb; border-radius: 6px; margin-top: 8px; }
  .ref { background: #f8fafc; border-left: 3px solid #111827; padding: 10px; margin-top: 10px; font-size: 11.5px; }
  .footer {
    position: fixed; bottom: 0.35in; left: 0.65in; right: 0.65in;
    font-size: 9px; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 6px;
  }
  .watermark {
    position: fixed; top: 38%; left: 8%;
    font-size: 40px; color: rgba(17,24,39,0.05);
    transform: rotate(-20deg);
  }
</style>
</head>
<body>
  <div class="watermark">CONFIDENTIAL • SOUTHWIND PLANNING</div>

  <div class="header">
    {% if logo_b64 %}
      <img class="logo" src="data:image/png;base64,{{ logo_b64 }}" />
    {% endif %}
    <div class="title">Signal Integrity Assessment™</div>
    <div class="subtitle">A structured executive diagnostic on decision information reliability</div>
    <div class="meta">Prepared for <b>{{ org_name }}</b> • {{ assessment_date }}</div>
  </div>

  <div class="framing">{{ framing | safe }}</div>

  <div class="section-title">Lifeline Integrity Grid</div>
  <table>
    <thead>
      <tr><th>Lifeline</th><th>Status</th><th>Signal Pattern</th></tr>
    </thead>
    <tbody>
    {% for r in grid_rows %}
      <tr>
        <td>{{ r.lifeline }}</td>
        <td class="badge {{ r.status }}">{{ r.status }}</td>
        <td>{{ r.pattern }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>

  {% if map_png_b64 %}
    <div class="section-title">Signal Map</div>
    <div class="map"><img src="data:image/png;base64,{{ map_png_b64 }}" /></div>
  {% endif %}

  <div class="section-title">Reflection Prompts</div>
  <div class="ref">
    <ul>
      <li>Which lifeline would matter most under pressure—and why?</li>
      <li>Where is continuity dependent on people rather than visibility?</li>
      <li>What would you verify before your next major decision?</li>
      <li>Where might stability be subsidized by heroics?</li>
    </ul>
  </div>

  <div class="footer">
    {{ contact_line }}<br>
    Confidential diagnostic prepared for internal leadership use. This instrument highlights decision visibility and information integrity; it does not prescribe solutions.
  </div>
</body>
</html>
""")

    return template.render(
        logo_b64=logo_b64,
        org_name=org_name,
        assessment_date=assessment_date,
        framing=framing,
        grid_rows=grid_rows,
        map_png_b64=map_png_b64,
        contact_line=CONTACT_LINE
    )
def show_results_page():
    responses = st.session_state.get("responses", {})
    if not responses:
        st.error("No responses found. Please complete the assessment first.")
        return

    # Force scroll to top upon loading results
    scroll_to_top()

    st.title("Signal Integrity Assessment™")
    st.markdown(
        f"**{st.session_state.org_name}** | Assessment Date: {st.session_state.assessment_date}"
    )
    st.markdown("---")

    # Analyze responses
    analysis = analyze_responses()
    if not isinstance(analysis, dict) or not analysis:
        st.error("Assessment analysis could not be generated. Please complete all questions.")
        return

    # Store for later export / other pages
    st.session_state["analysis"] = analysis

    # Section 1: Executive Observations
    st.header("Executive Observations")

    status_color = {
        "SOLID": "🟢",
        "CONDITIONAL": "🟡",
        "MIXED": "⚪",
        "FRAGILE": "🔴",
    }

    for lifeline_name, data in analysis.items():
        status = (data.get("status") or "MIXED").upper()
        desc = data.get("description", "")

        icon = status_color.get(status, "⚪")
        st.subheader(f"{icon} {lifeline_name} — {status}")

        if desc:
            st.write(desc)

    # Section 2: Signal Map Visualization
    st.header("Signal Integrity Map")
    st.markdown(
        "Node colors indicate status, and distance from center represents signal integrity."
    )

    viz_type = st.radio(
        "Visualization Style",
        ["Radar Chart", "Network Map"],
        horizontal=True,
    )

    if viz_type == "Radar Chart":
        fig = create_signal_map(analysis)
    else:
        fig = create_network_signal_map(analysis)

    st.plotly_chart(fig, use_container_width=True)

    # Section 3: Lifeline Integrity Grid
    st.header("Lifeline Integrity Grid")
    table_data = []
    for lifeline_name, data in analysis.items():
        signals = data.get("signals", {})
        signal_pattern = ", ".join([f"{sig}: {count}" for sig, count in signals.items()])
        table_data.append(
            {
                "Lifeline": lifeline_name,
                "Status": data.get("status", ""),
                "Signal Pattern": signal_pattern,
            }
        )
    st.table(table_data)

    # Section 4: Key Distinctions
    st.header("Key Distinctions")
    st.info(
        """
**Signal Classifications Defined:**
* **Observed:** Direct, current evidence.
* **Assumed:** Believed to be true but not recently confirmed.
* **Historical:** Once verified but not tested under current conditions.
* **Compensated:** Stability depends on individual effort or workarounds.
"""
    )

    # Section 5: Reflection Prompts
    st.header("Questions for Leadership Reflection")
    st.markdown(
        """
* Which of these lifelines would matter most under sustained pressure?
* Where is operational continuity dependent on people rather than process?
* What information should be verified before your next major decision?
* Where might historical assumptions be vulnerable to current changes?
"""
    )

    st.markdown("---")

    # Section 6: Restart Option (quick)
    if st.button("Start New Assessment", use_container_width=False):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Closing Statement
    st.info(
        """
**Note:** This assessment identifies where decision confidence is well supported by current evidence
and where additional verification may be needed. It does not prescribe solutions or evaluate leadership capability.

For shared organizational clarity, this assessment is often reviewed in a facilitated mirror session.
"""
    )

    # Professional CTA Footer
    st.markdown("---")
    st.markdown(
        """
<div style='text-align: center; padding: 2rem; background-color: #f8fafc; border-radius: 8px; margin-top: 2rem;'>
  <h3 style='color: #1e293b; margin-bottom: 1rem;'>Schedule a Mirror Session</h3>
  <p style='color: #64748b; margin-bottom: 1.5rem; max-width: 600px; margin-left: auto; margin-right: auto;'>
    Gain shared organizational clarity by reviewing this assessment in a facilitated discussion
    with your leadership team.
  </p>
  <a href='mailto:contact@southwindplanning.com?subject=Mirror Session Request&body=I just completed the Signal Integrity Assessment and would like to schedule a mirror session.%0D%0A%0D%0AOrganization: {org_name}%0D%0AAssessment Date: {date}'
     style='display: inline-block; background-color: #1e293b; color: white; padding: 0.875rem 2rem;
            text-decoration: none; border-radius: 6px; font-weight: 500; transition: background-color 0.2s;'>
    Schedule Mirror Session →
  </a>
  <p style='color: #94a3b8; font-size: 0.875rem; margin-top: 1.5rem;'>
    <strong>Southwind Planning</strong> • Readiness Is Not a Plan. It's a Capability.
  </p>
</div>
""".format(
            org_name=st.session_state.org_name,
            date=st.session_state.assessment_date,
        ),
        unsafe_allow_html=True,
    )

    # Export options
    st.markdown("---")
    st.header("Export Options")
    
    # Add print-to-PDF button
    st.markdown("""
    <div style='background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 1rem; margin-bottom: 1rem;'>
        <strong>📄 Quick PDF Export:</strong> After downloading the HTML brief below, 
        open it in your browser → Press <kbd>Ctrl+P</kbd> (or <kbd>⌘+P</kbd> on Mac) 
        → Select "Save as PDF" → Done!
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ----- Executive Brief (HTML) -----
    with col1:
        st.caption("Generate a board-ready brief (HTML). Download and print to PDF.")

        brief_html = None
        if st.button("📄 Build Executive Brief", use_container_width=True):
            with st.spinner("Building your executive brief..."):
                fig = create_network_signal_map(analysis)
                map_png_b64 = fig_to_png_base64(fig)

                brief_html = build_executive_brief_html(
                    org_name=st.session_state.org_name,
                    assessment_date=str(st.session_state.assessment_date),
                    analysis=analysis,
                    map_png_b64=map_png_b64,
                )

        if brief_html:
            safe_org = st.session_state.org_name.replace(" ", "_")
            st.download_button(
                label="⬇️ Download Executive Brief (HTML)",
                data=brief_html.encode("utf-8"),
                file_name=f"Signal_Integrity_Brief_{safe_org}_{st.session_state.assessment_date}.html",
                mime="text/html",
                use_container_width=True,
            )
        else:
            st.caption("Click **Build Executive Brief** first, then the download button will appear.")

    # ----- Data Export (JSON) -----
    with col2:
        st.caption("Confidential diagnostic • Prepared for internal leadership use")

        export_data = {
            "organization": st.session_state.org_name,
            "assessment_date": str(st.session_state.assessment_date),
            "analysis": {
                k: {
                    "status": v.get("status"),
                    "description": v.get("description"),
                    "signals": dict(v.get("signals", {})),
                }
                for k, v in analysis.items()
            },
        }

        safe_org = st.session_state.org_name.replace(" ", "_")
        st.download_button(
            label="📥 Download Data (JSON)",
            data=json.dumps(export_data, indent=2),
            file_name=f"Signal_Integrity_Data_{safe_org}_{st.session_state.assessment_date}.json",
            mime="application/json",
            use_container_width=True,
        )




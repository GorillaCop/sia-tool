# Signal Integrity Assessment™ - Streamlit Application

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r streamlit_requirements.txt
```

2. **Run the application:**
```bash
streamlit run streamlit_app.py
```

3. **Open browser:**
The app will automatically open at `http://localhost:8501`

---

## Application Structure

```
├── streamlit_app.py          # Main application (metadata + assessment)
├── results.py                # Results page with visualizations
├── streamlit_requirements.txt # Python dependencies
└── README_STREAMLIT.md       # This file
```

---

## Features

### 1. Assessment Flow
- **Metadata collection** - Organization name and date
- **5 Business Lifelines** - 5 questions each (25 total)
- **Signal classification** - Observed, Assumed, Historical, Compensated
- **Progress tracking** - Visual progress bar and save functionality

### 2. Visualizations
- **Radar Chart** - Shows signal strength across lifelines
- **Network Map** - Central node with radiating connections
- **Status-based coloring** - SOLID (green), CONDITIONAL (amber), MIXED (gray), FRAGILE (red)

### 3. Results Page
- **Executive observations** - Plain language per lifeline
- **Interactive visualizations** - Toggle between chart types
- **Lifeline integrity grid** - Tabular status view
- **Key distinctions** - Signal classification definitions
- **Reflection prompts** - Questions for leadership discussion
- **Export options** - JSON data download (PDF coming soon)

---

## Deploy to Render

### Option 1: Direct Deploy

1. **Add files to your repository:**
```bash
git add streamlit_app.py results.py streamlit_requirements.txt
git commit -m "Add Streamlit application"
git push origin main
```

2. **Create new Web Service on Render:**
- Runtime: **Python 3**
- Build Command: `pip install -r streamlit_requirements.txt`
- Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

### Option 2: Using Docker (Alternative)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY streamlit_requirements.txt .
RUN pip install -r streamlit_requirements.txt

COPY streamlit_app.py results.py ./

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## Customization

### Adding Questions

Edit `LIFELINES` dictionary in `streamlit_app.py`:

```python
LIFELINES = {
    0: {
        'name': 'Your Lifeline Name',
        'questions': [
            'Question 1?',
            'Question 2?',
            # Add more...
        ]
    },
    # Add more lifelines...
}
```

### Changing Status Logic

Edit `analyze_responses()` in `results.py`:

```python
# Current logic:
if observed_pct >= 60:
    status = 'SOLID'
elif compensated_pct >= 40:
    status = 'FRAGILE'
# Modify thresholds as needed
```

### Styling

Update CSS in `streamlit_app.py`:

```python
st.markdown("""
<style>
    /* Your custom CSS here */
</style>
""", unsafe_allow_html=True)
```

---

## Session State Management

The app uses Streamlit session state to persist data:

- `st.session_state.page` - Current page (metadata/assessment/results)
- `st.session_state.responses` - All question responses
- `st.session_state.current_lifeline` - Progress through assessment
- `st.session_state.org_name` - Organization name
- `st.session_state.assessment_date` - Assessment date

---

## Troubleshooting

### Port Issues
If port 8501 is already in use:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r streamlit_requirements.txt --upgrade
```

### Visualization Not Showing
Check that Plotly is installed:
```bash
pip install plotly --upgrade
```

### Results Page Error
Ensure `results.py` is in the same directory as `streamlit_app.py`

---

## Next Steps

### Add PDF Generation

Install additional dependencies:
```bash
pip install reportlab weasyprint
```

Add to `results.py`:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(analysis):
    # PDF generation logic
    pass
```

### Add Database Storage

Install SQLAlchemy:
```bash
pip install sqlalchemy psycopg2-binary
```

Store assessments for historical tracking.

### Add Email Delivery

Install SendGrid:
```bash
pip install sendgrid
```

Email PDF reports automatically.

---

## Production Considerations

### Security
- Add authentication (Streamlit supports basic auth)
- Validate all inputs
- Sanitize user responses before display

### Performance
- Cache analysis results with `@st.cache_data`
- Optimize visualization rendering
- Add loading spinners for long operations

### Monitoring
- Add error tracking (Sentry)
- Log assessment completions
- Track user analytics

---

## Support

For issues or questions:
- Check Streamlit docs: https://docs.streamlit.io
- Plotly docs: https://plotly.com/python/
- Render deployment: https://render.com/docs

---

## License

Proprietary - Signal Integrity Assessment™

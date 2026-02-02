def show_metadata_page():
    """Metadata collection page"""
    # Ensure the browser is scrolled to the top when the cover/metadata page loads
    try:
        scroll_to_top()
    except Exception:
        # If JS injection fails in some environments, continue rendering without interrupting the UI.
        pass

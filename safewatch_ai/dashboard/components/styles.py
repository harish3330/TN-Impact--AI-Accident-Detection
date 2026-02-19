"""CSS theme and reusable HTML card renderers for the Streamlit dashboard."""


def get_custom_css() -> str:
    """Full CSS block injected via ``st.markdown(unsafe_allow_html=True)``."""
    return """
    <style>
    /* ===== GLOBAL ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }
    
    /* ===== HEADER BANNER ===== */
    .header-banner {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .header-banner h1 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-banner p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0.3rem 0 0 0;
    }
    .header-banner .accent {
        color: #38bdf8;
    }
    
    /* ===== KPI CARDS ===== */
    .kpi-card {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.3);
    }
    .kpi-card .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }
    .kpi-card .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        margin: 0.2rem 0;
    }
    .kpi-card .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .kpi-critical .kpi-value { color: #ef4444; }
    .kpi-warning .kpi-value { color: #f59e0b; }
    .kpi-success .kpi-value { color: #22c55e; }
    .kpi-info .kpi-value { color: #38bdf8; }
    
    /* ===== STATUS BADGES ===== */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .status-online {
        background: rgba(34,197,94,0.15);
        color: #22c55e;
        border: 1px solid rgba(34,197,94,0.3);
    }
    .status-offline {
        background: rgba(239,68,68,0.15);
        color: #ef4444;
        border: 1px solid rgba(239,68,68,0.3);
    }
    .status-critical {
        background: rgba(239,68,68,0.15);
        color: #ef4444;
        border: 1px solid rgba(239,68,68,0.3);
    }
    .status-warning {
        background: rgba(245,158,11,0.15);
        color: #f59e0b;
        border: 1px solid rgba(245,158,11,0.3);
    }
    
    /* ===== ALERT CARDS ===== */
    .alert-card {
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid;
        background: rgba(15,23,42,0.6);
    }
    .alert-card.critical {
        border-left-color: #ef4444;
        background: rgba(239,68,68,0.08);
    }
    .alert-card.warning {
        border-left-color: #f59e0b;
        background: rgba(245,158,11,0.08);
    }
    .alert-card .alert-title {
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }
    .alert-card.critical .alert-title { color: #ef4444; }
    .alert-card.warning .alert-title { color: #f59e0b; }
    .alert-card .alert-detail {
        font-size: 0.75rem;
        color: #94a3b8;
    }
    .alert-card .alert-time {
        font-size: 0.7rem;
        color: #64748b;
        margin-top: 0.2rem;
    }
    
    /* ===== DETECTION TYPE CARDS ===== */
    .detection-card {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.8rem;
    }
    .detection-card .det-icon { font-size: 1.5rem; }
    .detection-card .det-title {
        font-weight: 700;
        font-size: 0.9rem;
        color: #e2e8f0;
    }
    .detection-card .det-desc {
        font-size: 0.75rem;
        color: #64748b;
    }
    .detection-card .det-status {
        font-size: 0.75rem;
        font-weight: 600;
    }
    .det-active { color: #22c55e; }
    .det-inactive { color: #64748b; }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(56,189,248,0.3);
    }
    
    /* ===== VIDEO CONTAINER ===== */
    .video-container {
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid rgba(56,189,248,0.2);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 500;
    }
    
    /* ===== SYSTEM HEALTH ===== */
    .health-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0;
        font-size: 0.8rem;
    }
    .health-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .health-dot.green { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
    .health-dot.yellow { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
    .health-dot.red { background: #ef4444; box-shadow: 0 0 6px #ef4444; }
    
    /* ===== FEATURE GRID ===== */
    .feature-box {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid rgba(255,255,255,0.06);
        text-align: center;
        height: 100%;
    }
    .feature-box .feat-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .feature-box .feat-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #e2e8f0;
        margin-bottom: 0.3rem;
    }
    .feature-box .feat-desc {
        font-size: 0.78rem;
        color: #64748b;
        line-height: 1.4;
    }
    
    /* ===== TABLE STYLING ===== */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* ===== PULSE ANIMATION ===== */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .pulse { animation: pulse 2s infinite; }
    
    /* ===== MONITORING LIVE TAG ===== */
    .live-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(239,68,68,0.15);
        color: #ef4444;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(239,68,68,0.3);
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background: #ef4444;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    </style>
    """


def render_kpi_card(icon, value, label, color_class="kpi-info"):
    """Render a KPI card HTML."""
    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """


def render_alert_card(alert_type, detail, time_str, severity="warning"):
    """Render an alert card HTML."""
    return f"""
    <div class="alert-card {severity}">
        <div class="alert-title">{alert_type}</div>
        <div class="alert-detail">{detail}</div>
        <div class="alert-time">{time_str}</div>
    </div>
    """


def render_detection_card(icon, title, description, is_active=True):
    """Render a detection capability card."""
    status_class = "det-active" if is_active else "det-inactive"
    status_text = "ACTIVE" if is_active else "INACTIVE"
    return f"""
    <div class="detection-card">
        <span class="det-icon">{icon}</span>
        <span class="det-title">{title}</span>
        <span class="det-status {status_class}"> &bull; {status_text}</span>
        <div class="det-desc">{description}</div>
    </div>
    """


def render_feature_box(icon, title, description):
    """Render a feature box."""
    return f"""
    <div class="feature-box">
        <div class="feat-icon">{icon}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{description}</div>
    </div>
    """

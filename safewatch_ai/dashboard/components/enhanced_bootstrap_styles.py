def get_custom_css(theme: str = "light") -> str:
    theme_class = 'class="dark-theme"' if theme == "dark" else ''
    return """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">

    <style>
    :root {
        --bg-base:       #F8FAFC;
        --bg-gradient:   linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 50%, #F0F9FF 100%);
        --bg-card:       rgba(255, 255, 255, 0.72);
        --bg-card-solid: #FFFFFF;
        --glass-border:  rgba(37, 99, 235, 0.10);
        --glass-shadow:  0 4px 24px rgba(0, 0, 0, 0.06);
        --shadow-lift:   0 8px 32px rgba(37, 99, 235, 0.10);
        --primary:       #2563EB;
        --primary-light: #3B82F6;
        --cyan:          #06B6D4;
        --green:         #16A34A;
        --orange:        #F59E0B;
        --red:           #DC2626;
        --text-primary:  #1E293B;
        --text-secondary:#475569;
        --text-muted:    #94A3B8;
        --font-display:  'Poppins', sans-serif;
        --font-body:     'Inter', sans-serif;
        --radius:        0.75rem;
        --radius-lg:     1rem;
        --blur:          20px;
        --transition:    all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --grid-color:    rgba(37,99,235,0.025);
        --radial-a:      rgba(37,99,235,0.04);
        --radial-b:      rgba(6,182,212,0.04);
        --radial-c:      rgba(37,99,235,0.02);
        --sidebar-bg:    linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        --sidebar-border:rgba(37,99,235,0.08);
        --sidebar-shadow:4px 0 20px rgba(0,0,0,0.04);
        --scrollbar-track:#F1F5F9;
        --scrollbar-thumb:#CBD5E1;
        --input-bg:      rgba(255,255,255,0.9);
        --input-border:  rgba(37,99,235,0.12);
        --tab-bg:        rgba(37,99,235,0.03);
        --tab-hover:     rgba(37,99,235,0.06);
        --tab-active-bg: rgba(37,99,235,0.08);
        --table-stripe:  #FFFFFF;
        --table-hover:   rgba(37,99,235,0.02);
        --table-head-bg: rgba(37,99,235,0.05);
        --table-border:  #F1F5F9;
        --card-hover-bg: rgba(255,255,255,0.9);
        --critical-bg:   rgba(220,38,38,0.04);
        --critical-hover:rgba(220,38,38,0.06);
        --warning-bg:    rgba(245,158,11,0.03);
        --chart-grid:    rgba(37,99,235,0.06);
        --chart-zero:    rgba(37,99,235,0.10);
    }

    .stApp.dark-theme,
    .dark-theme {
        --bg-base:       #0B1120;
        --bg-gradient:   linear-gradient(135deg, #0B1120 0%, #0F172A 50%, #0B1426 100%);
        --bg-card:       rgba(15, 23, 42, 0.75);
        --bg-card-solid: #0F172A;
        --glass-border:  rgba(0, 245, 255, 0.12);
        --glass-shadow:  0 4px 24px rgba(0, 0, 0, 0.30);
        --shadow-lift:   0 8px 32px rgba(0, 245, 255, 0.12);
        --primary:       #00F5FF;
        --primary-light: #38BDF8;
        --cyan:          #00F5FF;
        --green:         #00FF88;
        --orange:        #FFA500;
        --red:           #FF3B3B;
        --text-primary:  #E2E8F0;
        --text-secondary:#94A3B8;
        --text-muted:    #64748B;
        --font-display:  'Orbitron', sans-serif;
        --font-body:     'Rajdhani', sans-serif;
        --grid-color:    rgba(0,245,255,0.03);
        --radial-a:      rgba(0,245,255,0.06);
        --radial-b:      rgba(59,130,246,0.06);
        --radial-c:      rgba(0,245,255,0.03);
        --sidebar-bg:    linear-gradient(180deg, #0B1120 0%, #0F172A 100%);
        --sidebar-border:rgba(0,245,255,0.08);
        --sidebar-shadow:4px 0 20px rgba(0,0,0,0.30);
        --scrollbar-track:#0F172A;
        --scrollbar-thumb:#1E293B;
        --input-bg:      rgba(15,23,42,0.8);
        --input-border:  rgba(0,245,255,0.12);
        --tab-bg:        rgba(0,245,255,0.04);
        --tab-hover:     rgba(0,245,255,0.08);
        --tab-active-bg: rgba(0,245,255,0.12);
        --table-stripe:  #0F172A;
        --table-hover:   rgba(0,245,255,0.04);
        --table-head-bg: rgba(0,245,255,0.06);
        --table-border:  rgba(0,245,255,0.06);
        --card-hover-bg: rgba(15,23,42,0.95);
        --critical-bg:   rgba(255,59,59,0.08);
        --critical-hover:rgba(255,59,59,0.12);
        --warning-bg:    rgba(255,165,0,0.06);
        --chart-grid:    rgba(0,245,255,0.06);
        --chart-zero:    rgba(0,245,255,0.10);
    }

    .stApp,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background: var(--bg-gradient) !important;
        color: var(--text-primary) !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse at 20% 80%, var(--radial-a) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, var(--radial-b) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, var(--radial-c) 0%, transparent 70%);
        animation: bgShift 25s ease-in-out infinite alternate;
        z-index: -2;
        pointer-events: none;
    }
    @keyframes bgShift {
        0%   { opacity: 0.6; transform: scale(1); }
        100% { opacity: 1;   transform: scale(1.03); }
    }

    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(var(--grid-color) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
        background-size: 64px 64px;
        z-index: -1;
        pointer-events: none;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    .main {
        position: relative;
        z-index: 1;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1440px;
        position: relative;
        z-index: 1;
    }

    .main .block-container > div {
        animation: fadeInUp 0.55s ease both;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--scrollbar-track); }
    ::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

    [data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border) !important;
        box-shadow: var(--sidebar-shadow) !important;
        padding: 0.5rem !important;
        width: 300px !important;
        min-width: 260px !important;
        max-width: 320px !important;
    }

    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--cyan), var(--primary));
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] .stRadio > div { gap: 0.3rem; }
    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-primary) !important;
        font-family: var(--font-body);
        font-weight: 600;
        font-size: 0.92rem;
        padding: 0.7rem 1rem;
        margin: 0.15rem 0;
        border-radius: var(--radius);
        transition: var(--transition);
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: var(--tab-bg);
        border: 1px solid var(--glass-border);
        cursor: pointer;
        width: 100%;
        min-height: 2.8rem;
    }

    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label div,
    [data-testid="stSidebar"] .stRadio label [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .stRadio label [data-testid="stMarkdownContainer"] span {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: var(--tab-hover);
        border-color: rgba(37,99,235,0.18);
        box-shadow: 0 2px 8px rgba(37,99,235,0.08);
        transform: translateX(3px);
    }
    .dark-theme [data-testid="stSidebar"] .stRadio label:hover {
        border-color: rgba(0,245,255,0.25);
        box-shadow: 0 2px 8px rgba(0,245,255,0.12);
    }

    [data-testid="stSidebar"] .stRadio input:checked + label {
        background: var(--tab-active-bg) !important;
        border-color: var(--primary) !important;
        border-left: 3px solid var(--primary) !important;
        box-shadow: 0 2px 12px rgba(37,99,235,0.12) !important;
        color: var(--primary) !important;
    }
    .dark-theme [data-testid="stSidebar"] .stRadio input:checked + label {
        box-shadow: 0 2px 12px rgba(0,245,255,0.15) !important;
    }
    [data-testid="stSidebar"] .stRadio input:checked + label p,
    [data-testid="stSidebar"] .stRadio input:checked + label span,
    [data-testid="stSidebar"] .stRadio input:checked + label [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .stRadio input:checked + label [data-testid="stMarkdownContainer"] span {
        color: var(--primary) !important;
    }

    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] { margin-right: 0.3rem; }

    [data-testid="stSidebar"] hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
        margin: 1rem 0.5rem;
    }

    [data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: var(--primary); }

    [data-testid="stSidebar"][aria-expanded="false"],
    section[data-testid="stSidebar"][aria-hidden="true"] {
        width: 0 !important; min-width: 0 !important; display: none !important;
    }
    .main, .main .block-container {
        transition: margin-left 0.3s ease, max-width 0.3s ease !important;
    }

    .health-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.78rem;
        color: var(--text-secondary);
        padding: 0.25rem 0;
        font-family: var(--font-body);
    }
    .health-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .health-dot.green {
        background: var(--green);
        box-shadow: 0 0 6px rgba(22,163,74,0.5);
        animation: dotPulse 2s ease-in-out infinite;
    }
    .dark-theme .health-dot.green {
        box-shadow: 0 0 8px rgba(0,255,136,0.6);
    }
    .health-dot.yellow {
        background: var(--orange);
        box-shadow: 0 0 6px rgba(245,158,11,0.5);
        animation: dotPulse 1.5s ease-in-out infinite;
    }
    .health-dot.red {
        background: var(--red);
        box-shadow: 0 0 6px rgba(220,38,38,0.5);
        animation: dotPulse 0.8s ease-in-out infinite;
    }
    .dark-theme .health-dot.red {
        box-shadow: 0 0 8px rgba(255,59,59,0.6);
    }
    @keyframes dotPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%      { opacity: 0.55; transform: scale(0.85); }
    }

    .glass {
        background: var(--bg-card);
        backdrop-filter: blur(var(--blur));
        -webkit-backdrop-filter: blur(var(--blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        box-shadow: var(--glass-shadow);
        transition: var(--transition);
    }
    .glass:hover {
        border-color: rgba(37,99,235,0.18);
        box-shadow: var(--shadow-lift);
        transform: translateY(-2px);
    }

    .header-banner {
        background: var(--bg-card);
        backdrop-filter: blur(var(--blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 2rem;
        margin-bottom: 1.2rem;
        box-shadow: var(--glass-shadow);
        position: relative;
        overflow: hidden;
    }
    .header-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--cyan), var(--primary));
    }
    .header-banner h1 {
        font-family: var(--font-display);
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        color: var(--text-primary);
    }
    .header-banner h1 a {
        display: none !important;
    }
    .header-banner h1 .accent {
        background: linear-gradient(135deg, var(--primary), var(--cyan));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .header-banner p {
        font-family: var(--font-body);
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin: 0;
    }

    .kpi-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: var(--glass-shadow);
        transition: var(--transition);
        height: 135px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--primary);
    }
    .kpi-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: var(--shadow-lift);
        border-color: rgba(37,99,235,0.2);
    }
    .dark-theme .kpi-card:hover {
        border-color: rgba(0,245,255,0.25);
    }
    .kpi-icon { font-size: 1.8rem; margin-bottom: 0.3rem; }
    .kpi-value {
        font-family: var(--font-display);
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin: 0.15rem 0;
    }
    .kpi-label {
        font-family: var(--font-body);
        font-size: 0.72rem;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }

    .kpi-info::before    { background: var(--primary); }
    .kpi-critical::before { background: var(--red); }
    .kpi-critical { border-color: rgba(220,38,38,0.18); }
    .dark-theme .kpi-critical { border-color: rgba(255,59,59,0.25); }
    .kpi-critical:hover { box-shadow: 0 8px 28px rgba(220,38,38,0.12); }
    .dark-theme .kpi-critical:hover { box-shadow: 0 8px 28px rgba(255,59,59,0.18); }
    .kpi-warning::before { background: var(--orange); }
    .kpi-success::before { background: var(--green); }

    .kpi-critical.glow-pulse { animation: criticalPulse 2s ease-in-out infinite; }
    @keyframes criticalPulse {
        0%, 100% { box-shadow: var(--glass-shadow); }
        50%      { box-shadow: 0 4px 20px rgba(220,38,38,0.18); }
    }

    .section-header {
        font-family: var(--font-display);
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid var(--glass-border);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: 0.3px;
    }

    .detection-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 0.85rem;
        margin-bottom: 0.6rem;
        transition: var(--transition);
        min-height: 95px;
        position: relative;
        overflow: hidden;
        animation: slideUp 0.5s ease both;
    }
    .detection-card:nth-child(2) { animation-delay: 0.1s; }
    .detection-card:nth-child(3) { animation-delay: 0.2s; }
    .detection-card:nth-child(4) { animation-delay: 0.3s; }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .detection-card:hover {
        border-color: rgba(37,99,235,0.25);
        box-shadow: 0 4px 16px rgba(37,99,235,0.10);
        transform: translateY(-2px);
    }
    .dark-theme .detection-card:hover {
        border-color: rgba(0,245,255,0.30);
        box-shadow: 0 4px 16px rgba(0,245,255,0.12);
    }
    .detection-card .det-header {
        display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.5rem;
    }
    .detection-card .det-icon {
        font-size: 1.3rem;
        animation: floatIcon 3s ease-in-out infinite;
    }
    @keyframes floatIcon {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-3px); }
    }
    .detection-card .det-title {
        font-family: var(--font-body);
        font-weight: 700; color: var(--text-primary); font-size: 0.88rem; margin: 0;
    }
    .detection-card .det-desc {
        font-family: var(--font-body);
        font-size: 0.72rem; color: var(--text-secondary); line-height: 1.4; margin: 0;
    }

    .alert-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 0.7rem 0.8rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid var(--primary);
        transition: var(--transition);
        animation: slideInRight 0.4s ease both;
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(16px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    .alert-card:hover {
        border-color: var(--glass-border);
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        background: var(--card-hover-bg);
    }
    .alert-card.critical {
        border-left-color: var(--red);
        background: var(--critical-bg);
    }
    .alert-card.critical:hover { background: var(--critical-hover); }
    .alert-card.warning {
        border-left-color: var(--orange);
        background: var(--warning-bg);
    }
    .alert-card .alert-title {
        font-family: var(--font-body);
        font-weight: 700; font-size: 0.82rem; color: var(--text-primary); margin-bottom: 0.2rem;
    }
    .alert-card .alert-detail {
        font-size: 0.72rem; color: var(--text-secondary); line-height: 1.3;
    }
    .alert-card .alert-time {
        font-size: 0.62rem; color: var(--text-muted); margin-top: 0.15rem;
        font-family: var(--font-body); font-weight: 500;
    }

    .status-badge {
        display: inline-flex; align-items: center; gap: 0.35rem;
        padding: 0.35rem 0.8rem; border-radius: 2rem;
        font-family: var(--font-body);
        font-size: 0.75rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.04em;
    }
    .status-badge.status-online {
        background: rgba(22,163,74,0.10);
        color: var(--green);
        border: 1px solid rgba(22,163,74,0.25);
    }
    .status-badge.status-offline {
        background: rgba(148,163,184,0.10);
        color: var(--text-secondary);
        border: 1px solid rgba(148,163,184,0.2);
    }

    .feature-box {
        background: var(--bg-card);
        backdrop-filter: blur(var(--blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 0.8rem;
        text-align: center;
        transition: var(--transition);
        height: 100px;
    }
    .feature-box:hover {
        border-color: rgba(37,99,235,0.2);
        box-shadow: 0 4px 14px rgba(37,99,235,0.08);
        transform: translateY(-3px);
    }
    .dark-theme .feature-box:hover {
        border-color: rgba(0,245,255,0.25);
        box-shadow: 0 4px 14px rgba(0,245,255,0.10);
    }
    .feature-box .feat-icon {
        font-size: 1.2rem; margin-bottom: 0.3rem;
        animation: floatIcon 3s ease-in-out infinite;
    }
    .feature-box .feat-title {
        font-family: var(--font-body);
        font-weight: 700; color: var(--text-primary); font-size: 0.8rem; margin-bottom: 0.15rem;
    }
    .feature-box .feat-desc {
        font-size: 0.62rem; color: var(--text-muted); line-height: 1.2;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius) !important;
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.3rem !important;
        transition: var(--transition) !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.2) !important;
        position: relative;
        overflow: hidden;
    }
    .dark-theme .stButton > button {
        color: #0B1120 !important;
        box-shadow: 0 2px 8px rgba(0,245,255,0.25) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 16px rgba(37,99,235,0.3) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: scale(0.98) !important; }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: var(--radius) !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }
    .dark-theme .stTextInput > div > div > input:focus,
    .dark-theme .stNumberInput > div > div > input:focus {
        box-shadow: 0 0 0 3px rgba(0,245,255,0.12) !important;
    }
    .stSelectbox > div > div {
        background: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.3rem; background: transparent; }
    .stTabs [data-baseweb="tab"] {
        background: var(--tab-bg) !important;
        color: var(--text-secondary) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--glass-border) !important;
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        transition: var(--transition) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--tab-hover) !important;
        border-color: rgba(37,99,235,0.15) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--tab-active-bg) !important;
        color: var(--primary) !important;
        border-color: var(--primary) !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.1) !important;
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--primary) !important;
        box-shadow: 0 0 6px rgba(37,99,235,0.3) !important;
    }
    .stSlider [data-testid="stTickBar"] > div { background: var(--primary) !important; }

    .stToggle label span[data-testid="stWidgetLabel"] {
        color: var(--text-primary) !important;
    }

    .stMetric {
        background: var(--bg-card) !important;
        backdrop-filter: blur(var(--blur)) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
        padding: 1rem !important;
        box-shadow: var(--glass-shadow) !important;
    }
    .stMetric label { color: var(--text-muted) !important; font-weight: 600 !important; }
    .stMetric [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-family: var(--font-display) !important;
        font-weight: 700 !important;
    }

    .streamlit-expanderHeader {
        background: var(--tab-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
    }

    .dataframe {
        border-radius: var(--radius); overflow: hidden;
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow);
    }
    .dataframe thead { background: var(--table-head-bg); }
    .dataframe th {
        color: var(--primary) !important;
        font-family: var(--font-body);
        font-weight: 700; font-size: 0.8rem;
        text-transform: uppercase; letter-spacing: 0.05em;
        padding: 0.75rem 1rem;
        border-bottom: 2px solid var(--glass-border);
    }
    .dataframe td {
        padding: 0.75rem 1rem;
        color: var(--text-primary);
        background: var(--table-stripe);
        border-bottom: 1px solid var(--table-border);
    }
    .dataframe tr:hover td { background: var(--table-hover); }

    .live-tag {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: rgba(220,38,38,0.08);
        border: 1px solid rgba(220,38,38,0.25);
        color: var(--red);
        padding: 0.3rem 0.9rem;
        border-radius: 2rem;
        font-family: var(--font-display);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        animation: liveFlash 1.2s ease-in-out infinite;
    }
    .live-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: var(--red);
        box-shadow: 0 0 6px rgba(220,38,38,0.4);
        animation: dotPulse 1s ease-in-out infinite;
    }
    @keyframes liveFlash {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.6; }
    }

    .scan-container { position: relative; overflow: hidden; border-radius: var(--radius); }
    .scan-line {
        position: absolute; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        box-shadow: 0 0 8px rgba(37,99,235,0.4);
        animation: scanDown 3s linear infinite;
        z-index: 5;
        pointer-events: none;
    }
    .dark-theme .scan-line {
        box-shadow: 0 0 12px rgba(0,245,255,0.5);
    }
    @keyframes scanDown {
        0%   { top: 0; }
        100% { top: 100%; }
    }

    .theme-toggle-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.4rem 0;
        font-family: var(--font-body);
        font-size: 0.75rem;
        color: var(--text-muted);
        font-weight: 600;
    }

    @media (max-width: 768px) {
        .header-banner h1 { font-size: 1.2rem; }
        .kpi-card { height: 110px; }
    }

    [data-testid="stHeader"] { background: transparent !important; }
    .css-1d391kg, .css-12oz5g7 { background: transparent !important; }
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    </style>
    """


def render_kpi_card(icon: str, value, label: str, color_class: str = "kpi-info") -> str:
    extra = " glow-pulse" if color_class == "kpi-critical" and str(value) not in ("0", "") else ""
    return (
        f'<div class="kpi-card {color_class}{extra}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-label">{label}</div></div>'
    )


def render_alert_card(alert_type: str, detail: str, time_str: str, severity: str = "warning") -> str:
    return (
        f'<div class="alert-card {severity}">'
        f'<div class="alert-title">{alert_type}</div>'
        f'<div class="alert-detail">{detail}</div>'
        f'<div class="alert-time">{time_str}</div></div>'
    )


def render_detection_card(icon: str, title: str, description: str, is_active: bool = True) -> str:
    badge = ('<span style="background:rgba(22,163,74,0.10);color:var(--green);'
             'padding:2px 8px;border-radius:10px;font-size:0.65rem;font-weight:700;'
             'border:1px solid rgba(22,163,74,0.2);'
             'margin-left:0.5rem;">● ACTIVE</span>' if is_active
             else '<span style="background:rgba(148,163,184,0.10);color:var(--text-muted);'
                  'padding:2px 8px;border-radius:10px;font-size:0.65rem;font-weight:700;'
                  'margin-left:0.5rem;">INACTIVE</span>')
    return (
        f'<div class="detection-card">'
        f'<div class="det-header">'
        f'<span class="det-icon">{icon}</span>'
        f'<div style="flex:1;">'
        f'<div style="display:flex;align-items:center;">'
        f'<span class="det-title">{title}</span>{badge}'
        f'</div></div></div>'
        f'<div class="det-desc">{description}</div></div>'
    )


def render_feature_box(icon: str, title: str, description: str) -> str:
    return (
        f'<div class="feature-box">'
        f'<div class="feat-icon">{icon}</div>'
        f'<div class="feat-title">{title}</div>'
        f'<div class="feat-desc">{description}</div></div>'
    )


def get_particle_canvas_html(theme: str = "light") -> str:
    dot = "rgba(37,99,235,0.22)" if theme == "light" else "rgba(0,245,255,0.28)"
    line_base = "37,99,235" if theme == "light" else "0,245,255"
    return f"""
    <canvas id="particles" style="position:fixed;top:0;left:0;width:100%;height:100%;
        pointer-events:none;z-index:0;opacity:0.35;"></canvas>
    <script>
    (function(){{
        const c=document.getElementById('particles');
        if(!c)return;
        const ctx=c.getContext('2d');
        let w,h;
        function resize(){{w=c.width=window.innerWidth;h=c.height=window.innerHeight;}}
        resize(); window.addEventListener('resize',resize);
        const pts=[];
        for(let i=0;i<40;i++){{
            pts.push({{x:Math.random()*w,y:Math.random()*h,
                      vx:(Math.random()-0.5)*0.25,vy:(Math.random()-0.5)*0.25,
                      r:Math.random()*1.5+0.5}});
        }}
        function draw(){{
            ctx.clearRect(0,0,w,h);
            for(const p of pts){{
                p.x+=p.vx; p.y+=p.vy;
                if(p.x<0)p.x=w; if(p.x>w)p.x=0;
                if(p.y<0)p.y=h; if(p.y>h)p.y=0;
                ctx.beginPath();
                ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
                ctx.fillStyle='{dot}';
                ctx.fill();
            }}
            for(let i=0;i<pts.length;i++){{
                for(let j=i+1;j<pts.length;j++){{
                    const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y;
                    const dist=Math.sqrt(dx*dx+dy*dy);
                    if(dist<130){{
                        ctx.beginPath();
                        ctx.moveTo(pts[i].x,pts[i].y);
                        ctx.lineTo(pts[j].x,pts[j].y);
                        ctx.strokeStyle='rgba({line_base},'+(0.06*(1-dist/130))+')';
                        ctx.lineWidth=0.5;
                        ctx.stroke();
                    }}
                }}
            }}
            requestAnimationFrame(draw);
        }}
        draw();
    }})();
    </script>
    """


def get_typing_effect_html(text: str, speed_ms: int = 50, theme: str = "light") -> str:
    clr = "#475569" if theme == "light" else "#94A3B8"
    cursor = "#2563EB" if theme == "light" else "#00F5FF"
    font = "'Inter'" if theme == "light" else "'Rajdhani'"
    return f"""
    <div style="font-family:{font},sans-serif; font-size:0.95rem; color:{clr};
        min-height:1.4em; margin-top:0.2rem;">
        <span id="typed-text"></span><span id="cursor"
        style="color:{cursor};animation:blink 1s step-end infinite;">|</span>
    </div>
    <style>@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:0;}}}}</style>
    <script>
    (function(){{
        const txt="{text}";
        const el=document.getElementById('typed-text');
        if(!el)return;
        let i=0;
        function type(){{
            if(i<txt.length){{el.textContent+=txt.charAt(i);i++;setTimeout(type,{speed_ms});}}
        }}
        type();
    }})();
    </script>
    """


def get_live_clock_html(theme: str = "light") -> str:
    clr = "#2563EB" if theme == "light" else "#00F5FF"
    font = "'Poppins'" if theme == "light" else "'Orbitron'"
    return f"""
    <div style="font-family:{font},sans-serif; font-size:1rem; color:{clr};
        font-weight:600; letter-spacing:1px;">
        <span id="live-clock"></span>
    </div>
    <script>
    (function(){{
        function tick(){{
            const d=new Date();
            const s=d.toLocaleTimeString('en-GB',{{hour12:false}});
            const el=document.getElementById('live-clock');
            if(el) el.textContent=s;
        }}
        tick(); setInterval(tick,1000);
    }})();
    </script>
    """


def get_ai_status_badge_html(is_active: bool = True, critical_count: int = 0,
                              theme: str = "light") -> str:
    font = "'Poppins'" if theme == "light" else "'Orbitron'"
    red = "#DC2626" if theme == "light" else "#FF3B3B"
    green = "#16A34A" if theme == "light" else "#00FF88"
    muted = "#94A3B8"
    if critical_count > 0:
        return f"""
        <div style="display:inline-flex;align-items:center;gap:0.4rem;
            background:rgba({','.join(str(int(red[i:i+2],16)) for i in (1,3,5))},0.08);
            border:1px solid rgba({','.join(str(int(red[i:i+2],16)) for i in (1,3,5))},0.25);
            color:{red};padding:0.3rem 0.9rem;border-radius:2rem;
            font-family:{font},sans-serif;font-size:0.7rem;font-weight:700;
            letter-spacing:0.5px;animation:liveFlash 0.8s ease-in-out infinite;">
            <span style="width:8px;height:8px;border-radius:50%;background:{red};
            box-shadow:0 0 6px rgba({','.join(str(int(red[i:i+2],16)) for i in (1,3,5))},0.4);
            animation:dotPulse 0.6s ease-in-out infinite;"></span>
            CRITICAL ALERTS
        </div>
        """
    if is_active:
        return f"""
        <div style="display:inline-flex;align-items:center;gap:0.4rem;
            background:rgba({','.join(str(int(green[i:i+2],16)) for i in (1,3,5))},0.08);
            border:1px solid rgba({','.join(str(int(green[i:i+2],16)) for i in (1,3,5))},0.2);
            color:{green};padding:0.3rem 0.9rem;border-radius:2rem;
            font-family:{font},sans-serif;font-size:0.7rem;font-weight:700;
            letter-spacing:0.5px;">
            <span style="width:8px;height:8px;border-radius:50%;background:{green};
            box-shadow:0 0 6px rgba({','.join(str(int(green[i:i+2],16)) for i in (1,3,5))},0.4);
            animation:dotPulse 2s ease-in-out infinite;"></span>
            AI ACTIVE
        </div>
        """
    return f"""
    <div style="display:inline-flex;align-items:center;gap:0.4rem;
        background:rgba(148,163,184,0.08);border:1px solid rgba(148,163,184,0.15);
        color:{muted};padding:0.3rem 0.9rem;border-radius:2rem;
        font-family:{font},sans-serif;font-size:0.7rem;font-weight:700;
        letter-spacing:0.5px;">
        <span style="width:8px;height:8px;border-radius:50%;background:{muted};"></span>
        AI IDLE
    </div>
    """


def get_count_up_js(element_id: str, end_val: int, duration_ms: int = 1200) -> str:
    return f"""
    <script>
    (function(){{
        const el=document.getElementById('{element_id}');
        if(!el)return;
        const end={end_val};
        const dur={duration_ms};
        let start=0;
        const t0=performance.now();
        function step(now){{
            const p=Math.min((now-t0)/dur,1);
            const ease=1-Math.pow(1-p,3);
            el.textContent=Math.floor(ease*end);
            if(p<1) requestAnimationFrame(step);
        }}
        requestAnimationFrame(step);
    }})();
    </script>
    """


def get_plotly_theme_template(theme: str = "light") -> dict:
    if theme == "dark":
        return dict(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Rajdhani, sans-serif", color="#E2E8F0"),
            xaxis=dict(gridcolor="rgba(0,245,255,0.06)", zerolinecolor="rgba(0,245,255,0.10)"),
            yaxis=dict(gridcolor="rgba(0,245,255,0.06)", zerolinecolor="rgba(0,245,255,0.10)"),
            hoverlabel=dict(bgcolor="#0F172A", bordercolor="#00F5FF",
                            font=dict(color="#E2E8F0", family="Rajdhani")),
            margin=dict(l=40, r=20, t=40, b=40),
        )
    return dict(
        template="plotly_white",
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, sans-serif", color="#1E293B"),
        xaxis=dict(gridcolor="rgba(37,99,235,0.06)", zerolinecolor="rgba(37,99,235,0.10)"),
        yaxis=dict(gridcolor="rgba(37,99,235,0.06)", zerolinecolor="rgba(37,99,235,0.10)"),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2563EB",
                        font=dict(color="#1E293B", family="Inter")),
        margin=dict(l=40, r=20, t=40, b=40),
    )


def get_theme_colors(theme: str = "light") -> dict:
    if theme == "dark":
        return dict(
            primary="#00F5FF", cyan="#00F5FF", green="#00FF88",
            orange="#FFA500", red="#FF3B3B", blue="#3B82F6",
            text="#E2E8F0", text2="#94A3B8", muted="#64748B",
            bg_card="rgba(11,17,32,0.8)", border="rgba(0,245,255,0.15)",
            bar_bg="rgba(255,255,255,0.08)",
            bar_grad="linear-gradient(90deg,#00F5FF,#3B82F6)",
            font_display="'Orbitron'", font_body="'Rajdhani'",
        )
    return dict(
        primary="#2563EB", cyan="#06B6D4", green="#16A34A",
        orange="#F59E0B", red="#DC2626", blue="#3B82F6",
        text="#1E293B", text2="#475569", muted="#94A3B8",
        bg_card="rgba(255,255,255,0.7)", border="rgba(37,99,235,0.10)",
        bar_bg="rgba(37,99,235,0.08)",
        bar_grad="linear-gradient(90deg,#2563EB,#06B6D4)",
        font_display="'Poppins'", font_body="'Inter'",
    )


def get_logo_html(theme: str = "light") -> str:
    tc = get_theme_colors(theme)
    return f'''
    <div style="display:flex; justify-content:center; align-items:center; padding: 12px 0 8px 0;">
        <svg width="240" height="50" viewBox="0 0 240 50" xmlns="http://www.w3.org/2000/svg">
            <path d="M25 5 L40 10 L40 25 C40 35 32 42 25 45 C18 42 10 35 10 25 L10 10 Z"
                  fill="none" stroke="{tc['cyan']}" stroke-width="2.5"/>
            <path d="M20 25 L24 29 L32 19"
                  fill="none" stroke="{tc['green']}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <text x="50" y="35" font-family="{tc['font_display']}, sans-serif" font-weight="700" font-size="28">
                <tspan fill="{tc['cyan']}">S</tspan><tspan fill="{tc['primary']}">a</tspan><tspan fill="{tc['green']}">f</tspan><tspan fill="{tc['orange']}">e</tspan><tspan fill="{tc['red']}">W</tspan><tspan fill="{tc['cyan']}">a</tspan><tspan fill="{tc['primary']}">t</tspan><tspan fill="{tc['green']}">c</tspan><tspan fill="{tc['orange']}">h</tspan>
            </text>
        </svg>
    </div>
    '''

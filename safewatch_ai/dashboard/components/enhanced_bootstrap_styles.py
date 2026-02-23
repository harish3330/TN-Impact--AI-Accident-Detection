def get_custom_css() -> str:
    """Enhanced Bootstrap-based CSS with advanced styling and animations."""
    return """
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
    /* ===== ENHANCED BOOTSTRAP THEME ===== */
    :root {
        --bs-primary: #4f46e5;
        --bs-primary-dark: #4338ca;
        --bs-primary-light: #818cf8;
        --bs-secondary: #64748b;
        --bs-success: #10b981;
        --bs-danger: #ef4444;
        --bs-warning: #f59e0b;
        --bs-info: #06b6d4;
        --bs-light: #f8fafc;
        --bs-dark: #1e293b;
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-success: linear-gradient(135deg, #00b09b, #96c93d);
        --gradient-danger: linear-gradient(135deg, #ff6b6b, #ee5a24);
    }
    
    /* ===== ADVANCED GLOBAL STYLES ===== */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f3f5 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(79, 70, 229, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(59, 130, 246, 0.03) 0%, transparent 50%);
        animation: floating-bg 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes floating-bg {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(-20px, -20px) rotate(1deg); }
        66% { transform: translate(20px, -10px) rotate(-1deg); }
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f3f5 100%) !important;
    }
    
    /* ===== ENHANCED SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 2px solid rgba(79, 70, 229, 0.1) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08) !important;
        position: relative;
        overflow: hidden;
        padding: 0.5rem 0.5rem 0.5rem 0.5rem !important;
        width: 320px !important;
        min-width: 280px !important;
        max-width: 340px !important;
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #4f46e5);
        animation: gradient-flow 4s ease-in-out infinite;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.3);
    }
    
    @keyframes gradient-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #1e293b !important;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.8rem 1.2rem;
        margin: 0.25rem 0;
        border-radius: 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        gap: 0.7rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        border: 2px solid rgba(79, 70, 229, 0.12);
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.08);
        cursor: pointer;
        font-family: 'Poppins', sans-serif;
        letter-spacing: 0.02em;
        position: relative;
        overflow: hidden;
        width: 100%;
        min-height: 3.5rem;
        justify-content: flex-start;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        color: var(--bs-primary) !important;
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.2);
        border-color: var(--bs-primary-light);
    }
    
    [data-testid="stSidebar"] .stRadio label:active {
        transform: scale(0.98) translateY(0px);
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.15);
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + label {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
        color: #fff !important;
        border-color: var(--bs-primary);
        box-shadow: 0 12px 32px rgba(79, 70, 229, 0.25);
        transform: scale(1.05);
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + label::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        opacity: 0.15;
        z-index: 0;
        border-radius: 1.2rem;
    }
    
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        margin-right: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] {
        font-size: 1.1rem;
        line-height: 1.2;
    }
    
    /* Sidebar Title Enhancement */
    [data-testid="stSidebar"] > div:first-child > div > div > div {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(124, 58, 237, 0.05));
        border-radius: 1rem;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(79, 70, 229, 0.15);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.1);
    }
    
    [data-testid="stSidebar"] > div:first-child > div > div > div > div {
        font-weight: 600 !important;
        color: var(--bs-primary) !important;
        font-size: 0.85rem !important;
        text-align: center;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar Divider Enhancement */
    [data-testid="stSidebar"] hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(79, 70, 229, 0.2), transparent);
        margin: 2rem 1rem;
        border-radius: 1px;
    }
    
    /* Sidebar Content Enhancement */
    [data-testid="stSidebar"] .element-container {
        margin: 0.5rem 0;
    }
    
    /* ===== FULL SCREEN WHEN SIDEBAR COLLAPSED ===== */
    /* When sidebar is collapsed, expand main content to full width */
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 0 !important;
        min-width: 0 !important;
        margin-left: 0 !important;
        display: none;
    }
    
    /* Adjust main content area when sidebar is collapsed */
    [data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stAppViewContainer"] .main,
    [data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stAppViewContainer"] .main .block-container {
        margin-left: 0 !important;
        padding-left: 2rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Alternative selector for collapsed sidebar */
    .stApp[data-test-sidebar-collapsed="true"] [data-testid="stAppViewContainer"] .main,
    .stApp[data-test-sidebar-collapsed="true"] [data-testid="stAppViewContainer"] .main .block-container {
        margin-left: 0 !important;
        padding-left: 2rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Streamlit v1.30+ collapsed sidebar handling */
    section[data-testid="stSidebar"][aria-hidden="true"] {
        width: 0 !important;
        min-width: 0 !important;
        display: none !important;
    }
    
    /* Main content expansion when no visible sidebar */
    .appview-container:has([data-testid="stSidebar"][aria-hidden="true"]) .main .block-container,
    [data-testid="stAppViewContainer"]:has([data-testid="stSidebar"][aria-hidden="true"]) .main .block-container {
        max-width: 100% !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    
    /* Remove left margin when sidebar is hidden */
    .stApp:has([data-testid="stSidebar"][aria-hidden="true"]) .main {
        margin-left: 0 !important;
    }
    
    /* Smooth transition for content expansion */
    .main, .main .block-container {
        transition: margin-left 0.3s ease-in-out, max-width 0.3s ease-in-out, padding 0.3s ease-in-out !important;
    }
    
    /* Active State Enhancement */
    [data-testid="stSidebar"] .stRadio input:checked + label {
        background: linear-gradient(135deg, var(--bs-primary), #7c3aed) !important;
        color: white !important;
        transform: translateX(0.5rem) scale(1.02);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
        border-color: var(--bs-primary);
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + label::before {
        display: none;
    }
    
    /* Sidebar Scrollbar Enhancement */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: rgba(79, 70, 229, 0.05);
        border-radius: 3px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--bs-primary), #7c3aed);
        border-radius: 3px;
    }
    
    /* Sidebar Icon Enhancement */
    [data-testid="stSidebar"] .stRadio label span[data-testid="stMarkdownContainer"] {
        font-size: 1.2rem;
        line-height: 1;
    }
    .header-banner {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(2deg);
        transition: all 0.3s ease;
    }
    
    .header-banner:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-5px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
    }
    
    .header-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: var(--gradient-primary);
        animation: gradient-shift 3s ease infinite;
    }
    
    .header-banner::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 70, 229, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .header-banner h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
        text-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .header-banner p {
        font-size: 1rem;
        color: #64748b;
        margin: 0;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .header-banner .accent {
        color: var(--bs-primary);
        font-weight: 700;
    }
    
    /* ===== ADVANCED KPI CARDS ===== */
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 1rem;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(2deg);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s ease;
    }
    
    .kpi-card:hover::before {
        left: 100%;
    }
    
    .kpi-card:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.3);
        border-color: var(--bs-primary);
    }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 2px 10px rgba(79, 70, 229, 0.2));
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.25rem 0;
        color: #1e293b;
        line-height: 1;
        text-shadow: 0 1px 5px rgba(0,0,0,0.08);
    }
    
    .kpi-label {
        font-size: 0.7rem;
        color: #64748b;
        font-weight: 600;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .kpi-info { 
        border-left: 4px solid var(--bs-primary); 
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(79, 70, 229, 0.02) 100%);
    }
    .kpi-critical { 
        border-left: 4px solid var(--bs-danger); 
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.02) 100%);
    }
    .kpi-warning { 
        border-left: 4px solid var(--bs-warning); 
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(245, 158, 11, 0.02) 100%);
    }
    .kpi-success { 
        border-left: 4px solid var(--bs-success); 
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.02) 100%);
    }
    
    .kpi-info .kpi-icon { }
    .kpi-critical .kpi-icon { }
    .kpi-warning .kpi-icon { }
    .kpi-success .kpi-icon { }
    
    /* ===== DYNAMIC SECTION HEADERS ===== */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(79, 70, 229, 0.15);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100px;
        height: 2px;
        background: var(--gradient-primary);
        animation: expand-width 2s ease infinite;
    }
    
    @keyframes expand-width {
        0%, 100% { width: 60px; }
        50% { width: 100px; }
    }
    
    /* ===== ADVANCED DETECTION CARDS ===== */
    .detection-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.75rem;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100px;
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(2deg);
    }
    
    .detection-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 70, 229, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .detection-card:hover::before {
        opacity: 1;
    }
    
    .detection-card:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-5px);
        box-shadow: 0 15px 35px rgba(79, 70, 229, 0.2);
        border-color: var(--bs-primary);
    }
    
    .detection-card .det-header {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        margin-bottom: 1.25rem;
    }
    
    .detection-card .det-icon {
        font-size: 1.2rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .detection-card .det-title {
        font-weight: 700;
        color: #1e293b;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .detection-card .det-desc {
        font-size: 0.7rem;
        color: #64748b;
        line-height: 1.3;
        margin: 0;
    }
    
    /* ===== SPECTACULAR ALERT CARDS ===== */
    .alert-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.75rem;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid var(--bs-primary);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .alert-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-primary);
        animation: alert-pulse 2s ease-in-out infinite;
    }
    
    @keyframes alert-pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    .alert-card:hover {
        transform: translateX(0.5rem);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .alert-card.critical {
        border-left-color: var(--bs-danger);
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.02) 100%);
    }
    
    .alert-card.critical::before {
        background: var(--gradient-danger);
    }
    
    .alert-card.warning {
        border-left-color: var(--bs-warning);
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(245, 158, 11, 0.02) 100%);
    }
    
    .alert-card.warning::before {
        background: var(--gradient-secondary);
    }
    
    .alert-card .alert-title {
        font-weight: 700;
        font-size: 0.8rem;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .alert-card .alert-detail {
        font-size: 0.7rem;
        color: #64748b;
        line-height: 1.2;
    }
    
    .alert-card .alert-time {
        font-size: 0.6rem;
        color: #94a3b8;
        margin-top: 0.2rem;
        font-weight: 500;
    }
    
    /* ===== ENHANCED STATUS BADGES ===== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .status-badge::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s;
    }
    
    .status-badge:hover::before {
        width: 200%;
        height: 200%;
    }
    
    .status-badge.status-online {
        background: var(--gradient-success);
        color: white;
        animation: badge-glow 2s ease-in-out infinite;
    }
    
    @keyframes badge-glow {
        0%, 100% { box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 6px 25px rgba(16, 185, 129, 0.6); }
    }
    
    .status-badge.status-offline {
        background: linear-gradient(135deg, #64748b, #475569);
        color: white;
    }
    
    /* ===== ADVANCED FEATURE BOXES ===== */
    .feature-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.75rem;
        padding: 0.75rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100px;
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(2deg);
    }
    
    .feature-box::before {
        content: '';
        position: absolute;
        top: -100%;
        left: 0;
        right: 0;
        height: 100%;
        background: linear-gradient(180deg, rgba(79, 70, 229, 0.1), transparent);
        transition: top 0.3s;
    }
    
    .feature-box:hover::before {
        top: 0;
    }
    
    .feature-box:hover {
        transform: perspective(1000px) rotateX(0deg) translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.25);
        border-color: var(--bs-primary);
    }
    
    .feature-box .feat-icon {
        font-size: 1.2rem;
        margin-bottom: 0.3rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .feature-box .feat-title {
        font-weight: 700;
        color: #1e293b;
        font-size: 0.8rem;
        margin-bottom: 0.2rem;
    }
    
    .feature-box .feat-desc {
        font-size: 0.6rem;
        color: #64748b;
        line-height: 1.1;
    }
    
    /* ===== SPECTACULAR BUTTONS ===== */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.5s, height 0.5s;
    }
    
    .stButton > button:hover::before {
        width: 300%;
        height: 300%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4) !important;
    }
    
    /* ===== ENHANCED SELECTBOX ===== */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 0.75rem !important;
        color: #1e293b !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stSelectbox > div > div:focus {
        border-color: var(--bs-primary) !important;
        box-shadow: 0 0 0 0.25rem rgba(79, 70, 229, 0.25) !important;
    }
    
    /* ===== ADVANCED TABLE STYLING ===== */
    .dataframe {
        border-radius: 1rem;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
    }
    
    .dataframe thead {
        background: var(--gradient-primary);
    }
    
    .dataframe th {
        font-weight: 700;
        color: white !important;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        padding: 1rem 1.25rem;
    }
    
    .dataframe td {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        color: #1e293b;
        background: rgba(255, 255, 255, 0.5);
    }
    
    .dataframe tr:hover td {
        background: rgba(79, 70, 229, 0.05);
        transform: scale(1.01);
        transition: all 0.2s ease;
    }
    
    /* ===== ENHANCED METRICS ===== */
    .stMetric {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stMetric:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stMetric label {
        color: #64748b !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .header-banner h1 {
            font-size: 2rem;
        }
        
        .kpi-value {
            font-size: 2.5rem;
        }
        
        .kpi-card {
            min-height: 180px;
            padding: 2rem;
        }
        
        .section-header {
            font-size: 1.5rem;
        }
    }
    
    /* ===== SCROLLBAR STYLING ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--bs-primary-dark);
    }
    </style>
    """


def render_kpi_card(icon, value, label, color_class="kpi-info"):
    """Render an enhanced Bootstrap KPI card HTML."""
    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """


def render_alert_card(alert_type, detail, time_str, severity="warning"):
    """Render an enhanced Bootstrap alert card HTML."""
    return f"""
    <div class="alert-card {severity}">
        <div class="alert-title">{alert_type}</div>
        <div class="alert-detail">{detail}</div>
        <div class="alert-time">{time_str}</div>
    </div>
    """


def render_detection_card(icon, title, description, is_active=True):
    """Render an enhanced Bootstrap detection capability card."""
    status_badge = f'<span class="badge bg-success">ACTIVE</span>' if is_active else '<span class="badge bg-secondary">INACTIVE</span>'
    
    return f"""
    <div class="detection-card">
        <div class="det-header">
            <span class="det-icon">{icon}</span>
            <div style="flex: 1;">
                <div style="display: flex; align-items: center;">
                    <span class="det-title">{title}</span>
                    {status_badge}
                </div>
            </div>
        </div>
        <div class="det-desc">{description}</div>
    </div>
    """


def render_feature_box(icon, title, description):
    """Render an enhanced Bootstrap feature box HTML."""
    return f"""
    <div class="feature-box">
        <div class="feat-icon">{icon}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{description}</div>
    </div>
    """

"""
Revolutionary UI Design System for SafeWatch AI Dashboard
Tailwind-Inspired | Advanced Animations | Modern Effects
"""

def get_custom_css() -> str:
    """Complete CSS design system with advanced animations and effects."""
    return """
    <style>
    /* ===== TAILWIND-INSPIRED DESIGN SYSTEM ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* ===== CSS VARIABLES (TAILWIND-LIKE SYSTEM) ===== */
    :root {
        /* Color Palette */
        --color-primary-50: #eff6ff;
        --color-primary-100: #dbeafe;
        --color-primary-200: #bfdbfe;
        --color-primary-300: #93c5fd;
        --color-primary-400: #60a5fa;
        --color-primary-500: #3b82f6;
        --color-primary-600: #2563eb;
        --color-primary-700: #1d4ed8;
        --color-primary-800: #1e40af;
        --color-primary-900: #1e3a8a;
        
        --color-secondary-50: #faf5ff;
        --color-secondary-500: #a855f7;
        --color-secondary-600: #9333ea;
        --color-secondary-700: #7e22ce;
        
        --color-accent-50: #fef3c7;
        --color-accent-500: #f59e0b;
        --color-accent-600: #d97706;
        
        --color-success-500: #10b981;
        --color-success-600: #059669;
        
        --color-danger-500: #ef4444;
        --color-danger-600: #dc2626;
        
        --color-warning-500: #f59e0b;
        --color-warning-600: #d97706;
        
        /* Grayscale */
        --color-gray-50: #f9fafb;
        --color-gray-100: #f3f4f6;
        --color-gray-200: #e5e7eb;
        --color-gray-300: #d1d5db;
        --color-gray-400: #9ca3af;
        --color-gray-500: #6b7280;
        --color-gray-600: #4b5563;
        --color-gray-700: #374151;
        --color-gray-800: #1f2937;
        --color-gray-900: #111827;
        
        /* Spacing Scale */
        --spacing-1: 0.25rem;
        --spacing-2: 0.5rem;
        --spacing-3: 0.75rem;
        --spacing-4: 1rem;
        --spacing-5: 1.25rem;
        --spacing-6: 1.5rem;
        --spacing-8: 2rem;
        --spacing-10: 2.5rem;
        --spacing-12: 3rem;
        --spacing-16: 4rem;
        --spacing-20: 5rem;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.5rem;
        --radius-3xl: 2rem;
        --radius-full: 9999px;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: 600ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    /* ===== GLOBAL RESET & BASE STYLES ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        color: var(--color-gray-900);
        overflow-x: hidden;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ===== ANIMATED BACKGROUND ELEMENTS ===== */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 135, 252, 0.3), transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(99, 179, 237, 0.3), transparent 50%);
        animation: float 20s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -50px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    .stApp {
        position: relative;
        z-index: 1;
    }
    
    /* ===== ENSURE CONTENT VISIBILITY ===== */
    .stApp > div,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .block-container {
        position: relative;
        z-index: 10;
    }
    
    .element-container {
        position: relative;
        z-index: 10;
    }
    
    /* Fix Streamlit default backgrounds */
    .stApp,
    [data-testid="stAppViewContainer"],
    .main {
        background: transparent !important;
    }
    
    /* ===== STUNNING HEADER WITH 3D EFFECT ===== */
    .header-banner {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: var(--radius-3xl);
        padding: var(--spacing-12);
        margin: var(--spacing-6) 0 var(--spacing-10);
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 
            var(--shadow-2xl),
            0 0 0 1px rgba(255, 255, 255, 0.5) inset,
            0 0 60px rgba(99, 102, 241, 0.3);
        animation: slideDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-50px) rotateX(-15deg);
        }
        to {
            opacity: 1;
            transform: translateY(0) rotateX(0);
        }
    }
    
    .header-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .header-banner::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(
            90deg,
            #ff0000 0%,
            #ff7f00 16.666%,
            #ffff00 33.333%,
            #00ff00 50%,
            #0000ff 66.666%,
            #4b0082 83.333%,
            #9400d3 100%
        );
        border-radius: var(--radius-3xl) var(--radius-3xl) 0 0;
        animation: rainbow-flow 3s linear infinite;
        background-size: 200% 100%;
    }
    
    @keyframes rainbow-flow {
        to { background-position: -200% 0; }
    }
    
    .header-banner h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--spacing-4);
        letter-spacing: -0.05em;
        text-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: textGlow 2s ease-in-out infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    @keyframes textGlow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }
    }
    
    .header-banner p {
        font-size: 1.25rem;
        color: var(--color-gray-600);
        font-weight: 500;
        letter-spacing: 0.02em;
        position: relative;
        z-index: 1;
    }
    
    /* ===== REVOLUTIONARY KPI CARDS ===== */
    .kpi-card {
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(255, 255, 255, 0.85) 100%
        );
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-8);
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-xl);
        transition: all var(--transition-slow);
        cursor: pointer;
        min-height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .kpi-card:nth-child(1) { animation-delay: 0.1s; }
    .kpi-card:nth-child(2) { animation-delay: 0.2s; }
    .kpi-card:nth-child(3) { animation-delay: 0.3s; }
    .kpi-card:nth-child(4) { animation-delay: 0.4s; }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, var(--accent-color), transparent);
        opacity: 0;
        transition: opacity var(--transition-base);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(
            circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
            rgba(99, 102, 241, 0.1),
            transparent 50%
        );
        opacity: 0;
        transition: opacity var(--transition-base);
    }
    
    .kpi-card:hover::after {
        opacity: 1;
    }
    
    .kpi-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 
            var(--shadow-2xl),
            0 0 40px rgba(99, 102, 241, 0.3);
    }
    
    .kpi-card.kpi-primary {
        --accent-color: var(--color-primary-500);
    }
    
    .kpi-card.kpi-success {
        --accent-color: var(--color-success-500);
    }
    
    .kpi-card.kpi-warning {
        --accent-color: var(--color-warning-500);
    }
    
    .kpi-card.kpi-danger {
        --accent-color: var(--color-danger-500);
    }
    
    .kpi-icon {
        font-size: 4rem;
        filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.15));
        animation: float-icon 3s ease-in-out infinite;
        transition: transform var(--transition-base);
    }
    
    @keyframes float-icon {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .kpi-card:hover .kpi-icon {
        transform: scale(1.15) rotate(5deg);
    }
    
    .kpi-card.kpi-primary .kpi-icon { color: var(--color-primary-500); }
    .kpi-card.kpi-success .kpi-icon { color: var(--color-success-500); }
    .kpi-card.kpi-warning .kpi-icon { color: var(--color-warning-500); }
    .kpi-card.kpi-danger .kpi-icon { color: var(--color-danger-500); }
    
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: var(--color-gray-900);
        margin: var(--spacing-6) 0 var(--spacing-3);
        line-height: 1;
        letter-spacing: -0.02em;
        transition: transform var(--transition-base);
    }
    
    .kpi-card:hover .kpi-value {
        transform: scale(1.1);
    }
    
    .kpi-label {
        font-size: 1rem;
        font-weight: 600;
        color: var(--color-gray-600);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* ===== MODERN SECTION HEADERS ===== */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: var(--color-gray-900);
        margin: var(--spacing-12) 0 var(--spacing-6);
        padding-bottom: var(--spacing-4);
        position: relative;
        display: inline-block;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60%;
        height: 6px;
        background: linear-gradient(90deg, var(--color-primary-500), var(--color-secondary-500));
        border-radius: var(--radius-full);
        animation: expand-line 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @keyframes expand-line {
        from { width: 0; }
        to { width: 60%; }
    }
    
    /* ===== 3D FLIP CARDS ===== */
    .flip-card {
        perspective: 1000px;
        height: 320px;
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    }
    
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        transform-style: preserve-3d;
    }
    
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: var(--radius-2xl);
        padding: var(--spacing-8);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: var(--shadow-xl);
    }
    
    .flip-card-front {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
    }
    
    .flip-card-back {
        background: linear-gradient(135deg, 
            var(--color-primary-500) 0%, 
            var(--color-secondary-500) 100%);
        color: white;
        transform: rotateY(180deg);
    }
    
    /* ===== DETECTION CARDS WITH MORPHING ===== */
    .detection-card {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-8);
        margin-bottom: var(--spacing-6);
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        transition: all var(--transition-slow);
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    }
    
    .detection-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            from 0deg at 50% 50%,
            var(--color-primary-500),
            var(--color-secondary-500),
            var(--color-primary-500)
        );
        opacity: 0;
        transition: opacity var(--transition-slow);
        animation: rotate 4s linear infinite;
    }
    
    @keyframes rotate {
        to { transform: rotate(360deg); }
    }
    
    .detection-card:hover::before {
        opacity: 0.1;
    }
    
    .detection-card:hover {
        transform: translateY(-8px);
        box-shadow: 
            var(--shadow-2xl),
            0 0 50px rgba(99, 102, 241, 0.3);
    }
    
    .det-header {
        display: flex;
        align-items: center;
        gap: var(--spacing-5);
        margin-bottom: var(--spacing-5);
    }
    
    .det-icon {
        font-size: 2.5rem;
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-secondary-500));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 4px 12px rgba(99, 102, 241, 0.3));
        transition: transform var(--transition-base);
    }
    
    .detection-card:hover .det-icon {
        transform: scale(1.2) rotate(10deg);
    }
    
    .det-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        color: var(--color-gray-900);
        font-size: 1.5rem;
        letter-spacing: -0.02em;
    }
    
    .det-desc {
        font-size: 1.05rem;
        color: var(--color-gray-600);
        line-height: 1.8;
        font-weight: 500;
    }
    
    /* ===== ALERT CARDS WITH PULSE ===== */
    .alert-card {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-xl);
        padding: var(--spacing-6);
        margin-bottom: var(--spacing-5);
        border-left: 6px solid var(--alert-color);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
        transition: all var(--transition-base);
        animation: slideInLeft 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .alert-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, 
            transparent, 
            var(--alert-color), 
            transparent);
        animation: pulse-line 2s ease-in-out infinite;
    }
    
    @keyframes pulse-line {
        0%, 100% { 
            opacity: 0.5;
            transform: scaleY(0.8);
        }
        50% { 
            opacity: 1;
            transform: scaleY(1);
        }
    }
    
    .alert-card:hover {
        transform: translateX(8px);
        box-shadow: var(--shadow-xl);
    }
    
    .alert-card.critical {
        --alert-color: var(--color-danger-500);
    }
    
    .alert-card.warning {
        --alert-color: var(--color-warning-500);
    }
    
    .alert-card.info {
        --alert-color: var(--color-primary-500);
    }
    
    /* ===== STUNNING BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-secondary-500));
        color: white;
        border: none;
        border-radius: var(--radius-xl);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        padding: var(--spacing-5) var(--spacing-10);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
        transition: all var(--transition-base);
        cursor: pointer;
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
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 400%;
        height: 400%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 
            var(--shadow-2xl),
            0 0 40px rgba(99, 102, 241, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-2px);
    }
    
    /* ===== MODERN SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(30px) saturate(180%);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: var(--shadow-2xl);
    }
    
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
        color: var(--color-gray-700);
        padding: var(--spacing-4) var(--spacing-5);
        border-radius: var(--radius-lg);
        transition: all var(--transition-base);
        margin: var(--spacing-2) 0;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"] .stRadio label::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-secondary-500));
        transform: scaleY(0);
        transition: transform var(--transition-base);
    }
    
    [data-testid="stSidebar"] .stRadio label:hover::before {
        transform: scaleY(1);
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.1), 
            rgba(168, 85, 247, 0.1));
        color: var(--color-primary-600);
        transform: translateX(8px);
    }
    
    /* ===== STATUS BADGES WITH GLOW ===== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--spacing-2);
        padding: var(--spacing-3) var(--spacing-6);
        border-radius: var(--radius-full);
        font-size: 0.875rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        box-shadow: var(--shadow-md);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .status-badge.status-online {
        background: linear-gradient(135deg, var(--color-success-500), var(--color-success-600));
        color: white;
        animation: pulse-badge 2s ease-in-out infinite;
    }
    
    @keyframes pulse-badge {
        0%, 100% { 
            box-shadow: var(--shadow-md), 0 0 20px rgba(16, 185, 129, 0.5); 
        }
        50% { 
            box-shadow: var(--shadow-lg), 0 0 30px rgba(16, 185, 129, 0.8); 
        }
    }
    
    .status-badge.status-offline {
        background: linear-gradient(135deg, var(--color-gray-400), var(--color-gray-500));
        color: white;
    }
    
    /* ===== MODERN TABLES ===== */
    .dataframe {
        border-radius: var(--radius-2xl);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow-xl);
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, var(--color-primary-600), var(--color-secondary-600));
    }
    
    .dataframe th {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        color: white;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: var(--spacing-6) var(--spacing-5);
        border: none;
    }
    
    .dataframe td {
        padding: var(--spacing-5);
        border-bottom: 1px solid var(--color-gray-200);
        color: var(--color-gray-700);
        font-weight: 500;
        transition: background var(--transition-fast);
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: rgba(99, 102, 241, 0.03);
    }
    
    .dataframe tr:hover td {
        background: rgba(99, 102, 241, 0.1);
    }
    
    /* ===== FEATURE BOXES WITH NEUMORPHISM ===== */
    .feature-box {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-10);
        text-align: center;
        box-shadow: 
            var(--shadow-xl),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all var(--transition-slow);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    }
    
    .feature-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle,
            rgba(99, 102, 241, 0.1),
            transparent 70%
        );
        opacity: 0;
        transition: opacity var(--transition-slow);
        animation: rotate 8s linear infinite;
    }
    
    .feature-box:hover::before {
        opacity: 1;
    }
    
    .feature-box:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 
            var(--shadow-2xl),
            0 0 50px rgba(99, 102, 241, 0.3);
    }
    
    .feat-icon {
        font-size: 4rem;
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-secondary-500));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 8px 16px rgba(99, 102, 241, 0.3));
        display: inline-block;
        animation: bounce-icon 2s ease-in-out infinite;
        transition: transform var(--transition-base);
    }
    
    @keyframes bounce-icon {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    .feature-box:hover .feat-icon {
        transform: scale(1.2) rotate(10deg);
    }
    
    .feat-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        color: var(--color-gray-900);
        font-size: 1.25rem;
        margin: var(--spacing-5) 0 var(--spacing-3);
        letter-spacing: -0.02em;
    }
    
    .feat-desc {
        font-size: 1rem;
        color: var(--color-gray-600);
        line-height: 1.7;
        font-weight: 500;
    }
    
    /* ===== LIVE TAG WITH BLINK ===== */
    .live-tag {
        display: inline-flex;
        align-items: center;
        gap: var(--spacing-3);
        background: linear-gradient(135deg, var(--color-danger-500), var(--color-danger-600));
        color: white;
        padding: var(--spacing-3) var(--spacing-6);
        border-radius: var(--radius-full);
        font-weight: 800;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        box-shadow: var(--shadow-lg);
        animation: pulse-live 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse-live {
        0%, 100% { 
            box-shadow: var(--shadow-lg), 0 0 20px rgba(239, 68, 68, 0.5); 
        }
        50% { 
            box-shadow: var(--shadow-xl), 0 0 35px rgba(239, 68, 68, 0.8); 
        }
    }
    
    .live-dot {
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 50%;
        animation: blink-dot 1s ease-in-out infinite;
    }
    
    @keyframes blink-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.2; }
    }
    
    /* ===== SCROLLBAR STYLING ===== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-full);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-secondary-500));
        border-radius: var(--radius-full);
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: background var(--transition-fast);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--color-primary-600), var(--color-secondary-700));
    }
    
    /* ===== METRICS STYLING ===== */
    .stMetric {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(255, 255, 255, 0.85) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--spacing-6) !important;
        box-shadow: var(--shadow-lg) !important;
        transition: transform var(--transition-base) !important;
    }
    
    .stMetric:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-xl) !important;
    }
    
    .stMetric label {
        color: var(--color-gray-600) !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: var(--color-gray-900) !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .header-banner h1 {
            font-size: 2.5rem;
        }
        
        .kpi-value {
            font-size: 2.5rem;
        }
        
        .kpi-card {
            min-height: 200px;
            padding: var(--spacing-6);
        }
        
        .section-header {
            font-size: 1.5rem;
        }
    }
    
    /* ===== SKELETON LOADER ===== */
    .skeleton {
        background: linear-gradient(
            90deg,
            var(--color-gray-200) 25%,
            var(--color-gray-100) 50%,
            var(--color-gray-200) 75%
        );
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s ease-in-out infinite;
        border-radius: var(--radius-lg);
    }
    
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* ===== LOADING SPINNER ===== */
    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(99, 102, 241, 0.1);
        border-top: 4px solid var(--color-primary-500);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* ===== PARTICLE EFFECT ===== */
    .particle {
        position: fixed;
        width: 4px;
        height: 4px;
        background: radial-gradient(circle, white, transparent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        animation: particle-float 4s ease-out forwards;
    }
    
    @keyframes particle-float {
        0% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) scale(0);
            opacity: 0;
        }
    }
    
    /* ===== ADDITIONAL VISIBILITY & TEXT FIXES ===== */
    
    /* Ensure all text is visible */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stText,
    p,
    span {
        position: relative;
        z-index: 10;
    }
    
    /* Column visibility */
    [data-testid="column"],
    .row-widget {
        position: relative;
        z-index: 10;
    }
    
    /* Ensure widgets are visible */
    .stSelectbox,
    .stTextInput,
    .stNumberInput,
    .stCheckbox,
    .stRadio,
    .stSlider {
        position: relative;
        z-index: 10;
    }
    
    /* Fix any transparent backgrounds on inputs */
    input, select, textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        color: var(--color-gray-900) !important;
    }
    
    </style>
    """


def render_kpi_card(icon, value, label, color_class="kpi-primary"):
    """Render a revolutionary KPI card with animations."""
    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """


def render_alert_card(alert_type, detail, time_str, severity="info"):
    """Render an animated alert card."""
    return f"""
    <div class="alert-card {severity}">
        <div class="alert-title" style="font-weight: 700; font-size: 1.1rem; color: var(--color-gray-900); margin-bottom: 0.5rem;">{alert_type}</div>
        <div class="alert-detail" style="font-size: 0.95rem; color: var(--color-gray-600); margin-bottom: 0.5rem;">{detail}</div>
        <div class="alert-time" style="font-size: 0.8rem; color: var(--color-gray-500);">{time_str}</div>
    </div>
    """


def render_detection_card(icon, title, description, is_active=True):
    """Render a detection capability card with morphing effects."""
    status_badge = f'''<span class="status-badge status-online">ACTIVE</span>''' if is_active else '''<span class="status-badge status-offline">INACTIVE</span>'''
    
    return f"""
    <div class="detection-card">
        <div class="det-header">
            <span class="det-icon">{icon}</span>
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span class="det-title">{title}</span>
                    {status_badge}
                </div>
            </div>
        </div>
        <div class="det-desc">{description}</div>
    </div>
    """


def render_feature_box(icon, title, description):
    """Render a feature box with neumorphism effect."""
    return f"""
    <div class="feature-box">
        <div class="feat-icon">{icon}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{description}</div>
    </div>
    """


def render_flip_card(front_icon, front_title, back_content):
    """Render a 3D flip card."""
    return f"""
    <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <div style="font-size: 4rem; margin-bottom: 1rem;">{front_icon}</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-gray-900);">{front_title}</div>
            </div>
            <div class="flip-card-back">
                <div style="font-size: 1.1rem; line-height: 1.8;">{back_content}</div>
            </div>
        </div>
    </div>
    """

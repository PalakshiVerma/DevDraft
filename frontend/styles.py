"""
Custom CSS for sleek, modern Streamlit styling.
Dark glassmorphic accents, clean typography, badge indicators, and cards.
"""

CUSTOM_CSS = """
<style>
/* Completely remove and hide sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* Import modern Google font */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Header badge styling */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.85rem;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #c084fc;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #111827 !important;
    background: none !important;
    -webkit-text-fill-color: #111827 !important;
    margin-bottom: 0.35rem;
    letter-spacing: -0.025em;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #374151 !important;
    margin-bottom: 1.75rem;
    line-height: 1.5;
}

/* Feature card */
.stat-pill {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(71, 85, 105, 0.4);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

.stat-pill .num {
    font-size: 1.25rem;
    font-weight: 700;
    color: #38bdf8;
}

.stat-pill .label {
    font-size: 0.78rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Polished output card */
.output-card {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
}

.output-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(51, 65, 85, 0.5);
    padding-bottom: 0.75rem;
}

/* Hide streamlit default top padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px;
}
</style>
"""

EXAMPLE_STANDUP = """i fixed that weird bug where users get logged out on page refresh. took forever bc the cookie expiry was set wrong in localstorage. also started reading docs for stripe webhooks but didn't finish. today i wanna try writing tests for the auth flow. oh and my blocker is i still don't have access to staging aws keys so i can't deploy yet."""

EXAMPLE_PR = """added rate limiting on the login route because we were getting spammed. used redis with token bucket algorithm. also cleaned up the error messages so attackers cant guess emails. tested by sending 100 requests in 2 seconds with curl and got 429 too many requests. let me know if the max 5 attempts per min is too strict."""

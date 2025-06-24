# =====================================================================
# ============================>> Captcha <<============================
# =====================================================================
USE_CAPTCHA_SOLVER = True
CAPTCHA_SOLVER = "2captcha"
# API keys for solvers
CAPTCHA_API_KEYS = {
    "2captcha": "your_2captcha_api_key_here",
    "anticaptcha": "your_anti_captcha_key_here"
}

# Default timeout for solving captchas
CAPTCHA_TIMEOUT = 120  # seconds

# Reusable headers or proxy for solving if needed
CAPTCHA_HEADERS = {
    "Content-Type": "application/json"
}

# =====================================================================
# ===========================>> TIME DELAY <<==========================
# =====================================================================
# Use random delay between requests?
USE_RANDOM_DELAY = True

# Delay range in seconds (min, max)
DELAY_RANGE = (2, 5)

# Fixed delay fallback if random disabled
FIXED_DELAY = 3

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds between retries


# =====================================================================
# ===========================>> SELENIUM <<============================
# =====================================================================
# Use Selenium for JavaScript-rendered sites?
USE_SELENIUM = False

# Run Chrome headless (no UI)
SELENIUM_HEADLESS = True

# Path to chromedriver executable (if not in PATH)
CHROMEDRIVER_PATH = None  # e.g. "/usr/local/bin/chromedriver"


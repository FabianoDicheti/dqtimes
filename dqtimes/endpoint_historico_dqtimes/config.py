import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getenv("BASE_DIR", os.path.dirname(os.path.abspath(__file__)))
DB_URL = os.getenv("DB_URL", f"sqlite:///{os.path.join(BASE_DIR, 'history.db')}")


PAGE_DEFAULT = int(os.getenv("PAGE_DEFAULT", 1))
LIMIT_DEFAULT = int(os.getenv("LIMIT_DEFAULT", 25))
DETAILS_DEFAULT = os.getenv("DETAILS_DEFAULT", "True").lower() in ("true", "1", "yes")

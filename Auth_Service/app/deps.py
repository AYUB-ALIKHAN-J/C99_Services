# app/deps.py

from app.core.database import get_db

# Re-export the get_db dependency for easy import elsewhere
get_db = get_db

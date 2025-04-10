import logging
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    db = SessionLocal()
    try:
        # Create admin user
        admin_email = "admin@example.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                first_name="Admin",
                last_name="User",
                password="admin123",  # In a real app, hash this
                role=UserRole.ADMIN
            )
            db.add(admin)
            logger.info("Created admin user")

        db.commit()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")
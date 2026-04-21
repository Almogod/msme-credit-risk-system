from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/msme_credit_risk.db")

# Ensure data directory exists if using SQLite
if DATABASE_URL.startswith("sqlite"):
    os.makedirs("data", exist_ok=True)

# For SQLite, we need check_same_thread: False. For Postgres, we don't.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LoanAssessment(Base):
    __tablename__ = "loan_assessments"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Business Inputs
    business_id = Column(String)
    age_years = Column(Integer)
    annual_revenue = Column(Float)
    net_profit = Column(Float)
    total_assets = Column(Float)
    total_debt = Column(Float)
    cibil_score = Column(Integer)
    udyam_registered = Column(Boolean)
    gst_compliant = Column(Boolean)
    
    # Results
    is_approved = Column(Boolean)
    approval_probability = Column(Float)
    recommended_limit = Column(Float)
    max_loan_cap = Column(Float)
    final_limit = Column(Float)
    
    # Explainability
    feature_importance = Column(JSON) # JSON of SHAP values
    remarks = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DATABASE_URL}")

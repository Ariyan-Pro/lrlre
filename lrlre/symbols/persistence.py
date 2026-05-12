"""
PERSISTENCE MODULE - ENTERPRISE GRID EDITION
SQLite database with SQLAlchemy ORM for LRLRE knowledge graph.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

# ==================== DATABASE MODELS ====================

class Fact(Base):
    """Stores atomic facts in Subject-Predicate-Object format."""
    __tablename__ = 'facts'
    
    id = Column(Integer, primary_key=True)
    subject = Column(String(500), nullable=False)
    predicate = Column(String(500), nullable=False)
    object = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    language = Column(String(10), default='en')  # ADDED BACK
    source = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Rule(Base):
    """Stores inference rules in natural language format."""
    __tablename__ = 'rules'
    
    id = Column(Integer, primary_key=True)
    rule_text = Column(Text, nullable=False)
    compiled_logic = Column(Text)
    confidence = Column(Float, default=0.9)
    language = Column(String(10), default='en')
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Rule({self.rule_text[:50]}...)>"

class InferenceResult(Base):
    """Stores results of inference operations."""
    __tablename__ = 'inference_results'
    
    id = Column(Integer, primary_key=True)
    input_text = Column(Text, nullable=False)
    language = Column(String(10))
    detected_language = Column(String(10))
    language_confidence = Column(Float)
    inference_type = Column(String(50))  # 'forward', 'backward', 'unification'
    result_json = Column(Text)
    processing_time_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<InferenceResult({self.inference_type}, {self.created_at})>"

class SystemMetrics(Base):
    """Stores system performance metrics."""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    context = Column(String(200))
    
    def __repr__(self):
        return f"<SystemMetrics({self.metric_name}: {self.metric_value})>"

# ==================== DATABASE INITIALIZATION ====================

def get_db_path():
    """Get the database file path."""
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'knowledge.db')

def init_db():
    """Initialize the database, create tables if they don't exist."""
    db_path = get_db_path()
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print(f"✅ Database initialized at: {db_path}")
    print(f"   - Facts table ready")
    print(f"   - Rules table ready")
    print(f"   - Inference results table ready")
    print(f"   - System metrics table ready")
    
    return engine

def get_session():
    """Get a database session."""
    engine = create_engine(f'sqlite:///{get_db_path()}')
    Session = sessionmaker(bind=engine)
    return Session()

# ==================== CRUD OPERATIONS ====================

def add_fact(subject: str, predicate: str, object: str, confidence: float = 1.0, 
             language: str = 'en', source: str = None):
    """Add a new fact to the database."""
    session = get_session()
    try:
        fact = Fact(
            subject=subject,
            predicate=predicate,
            object=object,
            confidence=confidence,
            language=language,
            source=source
        )
        session.add(fact)
        session.commit()
        print(f"✅ Added fact: {subject} {predicate} {object}")
        return fact.id
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding fact: {e}")
        return None
    finally:
        session.close()

def get_all_facts(limit: int = 100):
    """Retrieve all facts from the database."""
    session = get_session()
    try:
        facts = session.query(Fact).order_by(Fact.created_at.desc()).limit(limit).all()
        return facts
    finally:
        session.close()

def add_rule(rule_text: str, compiled_logic: str = None, confidence: float = 0.9,
             language: str = 'en', category: str = None):
    """Add a new inference rule."""
    session = get_session()
    try:
        rule = Rule(
            rule_text=rule_text,
            compiled_logic=compiled_logic,
            confidence=confidence,
            language=language,
            category=category
        )
        session.add(rule)
        session.commit()
        print(f"✅ Added rule: {rule_text[:50]}...")
        return rule.id
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding rule: {e}")
        return None
    finally:
        session.close()

def log_inference(input_text: str, language: str, detected_language: str,
                  language_confidence: float, inference_type: str,
                  result_json: str, processing_time_ms: float):
    """Log an inference operation result."""
    session = get_session()
    try:
        result = InferenceResult(
            input_text=input_text,
            language=language,
            detected_language=detected_language,
            language_confidence=language_confidence,
            inference_type=inference_type,
            result_json=result_json,
            processing_time_ms=processing_time_ms
        )
        session.add(result)
        session.commit()
        return result.id
    except Exception as e:
        session.rollback()
        print(f"❌ Error logging inference: {e}")
        return None
    finally:
        session.close()

def log_metric(metric_name: str, metric_value: float, 
               metric_unit: str = None, context: str = None):
    """Log a system performance metric."""
    session = get_session()
    try:
        metric = SystemMetrics(
            metric_name=metric_name,
            metric_value=metric_value,
            metric_unit=metric_unit,
            context=context
        )
        session.add(metric)
        session.commit()
        return metric.id
    except Exception as e:
        session.rollback()
        print(f"❌ Error logging metric: {e}")
        return None
    finally:
        session.close()

# ==================== INITIALIZATION CHECK ====================

def check_database_health():
    """Check if database is healthy and accessible."""
    try:
        session = get_session()
        fact_count = session.query(Fact).count()
        rule_count = session.query(Rule).count()
        session.close()
        
        return {
            "status": "healthy",
            "facts_count": fact_count,
            "rules_count": rule_count,
            "database_path": get_db_path(),
            "tables_accessible": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "database_path": get_db_path(),
            "tables_accessible": False
        }

# ==================== INITIALIZE ON IMPORT ====================

# Initialize database when module is imported
print("🔄 Initializing LRLRE Enterprise Grid Database...")
engine = init_db()
print("✅ Database initialization complete.")

# Test connection
health = check_database_health()
print(f"📊 Database Health: {health['status']}")
print(f"   Facts: {health.get('facts_count', 0)}")
print(f"   Rules: {health.get('rules_count', 0)}")




import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app

# Asegúrate de importar la dependencia de seguridad real:
from app.security.auth import check_token

# Configuración de la URL de la base de datos de prueba (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 
# Alternativamente, para una base de datos completamente en memoria: "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 1. FIXTURE para la Base de Datos
@pytest.fixture(scope="session")
def db_engine():
    # Crea todas las tablas
    Base.metadata.create_all(bind=engine)
    yield engine
    # Borra todas las tablas después de las pruebas (opcional)
    # Base.metadata.drop_all(bind=engine) 

@pytest.fixture(scope="function") 
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

# 3. FIXTURE para el Cliente de FastAPI
# ¡CORRECCIÓN CLAVE! Cambiamos scope="module" a scope="function"
@pytest.fixture(scope="function") 
def client(db_session):
    
    # --- MOCKS ---
    def override_get_db():
        yield db_session
    
    # 💥 MOCK CLAVE: Función que anula la autenticación y siempre devuelve éxito
    def mock_check_token():
        """Bypasses authentication for testing purposes."""
        return None 
    # -------------

    # Sobreescribe la dependencia de la DB y la de Seguridad
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[check_token] = mock_check_token # <- ¡AQUÍ ESTÁ LA MAGIA!
    
    with TestClient(app) as c:
        yield c
        
    # Limpia las sobrescrituras después de las pruebas
    app.dependency_overrides = {}
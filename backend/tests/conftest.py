"""
Pytest fixtures for Railway Crew Management System tests.
Uses SQLite for fast, isolated testing with dependency overrides.
"""

import os
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from app.db.database import Base
from app.auth.hashing import hash_password
from app.core.enums import UserRole, Department
from app.models.user import User
from app.models.assignment import Assignment
from app.models.shift import Shift
from app.models.availability import Availability
from app.models.crew import Crew
from app.models.cms_data import CMSData
from app.models.signon_data import SignOnData
from app.models.main_data import MainData
from app.models.archive_data import ArchiveData

engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def app_with_db(db_session: Session) -> FastAPI:
    from app.main import app
    from app.db.database import get_db
    app.dependency_overrides[get_db] = lambda: db_session
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(app_with_db: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app_with_db) as c:
        yield c


@pytest.fixture
def admin_token(client: TestClient, db_session: Session) -> str:
    user = User(
        username="admin",
        full_name="Admin User",
        email="admin@test.com",
        password_hash=hash_password("Admin@123"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.flush()
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def viewer_token(client: TestClient, db_session: Session) -> str:
    user = User(
        username="viewer",
        full_name="Viewer User",
        email="viewer@test.com",
        password_hash=hash_password("Viewer@123"),
        role=UserRole.VIEWER,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.flush()
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "viewer", "password": "Viewer@123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def sample_crew(db_session: Session) -> Crew:
    crew = Crew(
        crew_id="CR001",
        full_name="John Driver",
        department=Department.DRIVER,
        mobile_number="9876543210",
        designation="Driver",
        password_hash=hash_password("Test@1234"),
        is_active=True,
    )
    db_session.add(crew)
    db_session.commit()
    db_session.flush()
    return crew


@pytest.fixture
def sample_cms(db_session: Session, sample_crew: Crew) -> CMSData:
    cms = CMSData(
        crew_id=sample_crew.crew_id,
        crew_name=sample_crew.full_name,
        crew_designation=sample_crew.designation,
        fortnight_hours="80",
        avail_time="08:00",
        avail_station="NDLS",
        status="Available",
        called_time="06:00",
        ack_time="06:15",
        sign_on_time="07:00",
        last_signoff_time="",
        train_no="12345",
        from_station="NDLS",
        to_station="BCT",
        is_active=True,
        is_imported=False,
    )
    db_session.add(cms)
    db_session.commit()
    db_session.flush()
    return cms


@pytest.fixture
def sample_signon(db_session: Session, sample_crew: Crew, sample_cms: CMSData) -> SignOnData:
    signon = SignOnData(
        cms_id=sample_cms.id,
        crew_id=sample_crew.crew_id,
        crew_name=sample_crew.full_name,
        status="SignedOn",
        train_no="12345",
        from_station="NDLS",
        to_station="BCT",
        sign_on_time="07:00",
        cto_train_no="12345",
        cto_station="BCT",
        cto_time="08:00",
        loco1="L001",
        loco2="",
        loco3="",
        shed="SHED_A",
        is_active=True,
    )
    db_session.add(signon)
    db_session.commit()
    db_session.flush()
    return signon


@pytest.fixture
def sample_maindata(db_session: Session, sample_signon: SignOnData) -> MainData:
    main = MainData(
        signon_id=sample_signon.id,
        crew_id=sample_signon.crew_id,
        crew_name=sample_signon.crew_name,
        train_no=sample_signon.train_no,
        from_station=sample_signon.from_station,
        to_station=sample_signon.to_station,
        status=sample_signon.status,
        sign_on_time=sample_signon.sign_on_time,
        cto_train_no=sample_signon.cto_train_no,
        cto_station=sample_signon.cto_station,
        cto_time=sample_signon.cto_time,
        loco1=sample_signon.loco1,
        loco2=sample_signon.loco2,
        loco3=sample_signon.loco3,
        shed=sample_signon.shed,
        is_active=True,
    )
    db_session.add(main)
    db_session.commit()
    db_session.flush()
    return main

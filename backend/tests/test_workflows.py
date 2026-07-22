"""
Integration tests for the complete Railway Crew Management workflows.

Tests all 5 business workflows end-to-end via the API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crew import Crew
from app.models.cms_data import CMSData
from app.models.signon_data import SignOnData
from app.models.main_data import MainData
from app.models.archive_data import ArchiveData
from app.models.audit_log import AuditLog


class TestWorkflow1_FullLifeycle:
    """
    Workflow 1: Full lifecycle
      Create Crew → Create CMS → Sign On → MainData Created → Archive
    """

    def test_full_workflow(
        self, client: TestClient, admin_token: str, db_session: Session
    ):
        headers = {"Authorization": f"Bearer {admin_token}"}

        # ── Step 1: Create Crew ──────────────────────────────────────
        crew_payload = {
            "crew_id": "CR002",
            "full_name": "Alice Conductor",
            "department": "Driver",
            "mobile_number": "9876543211",
            "designation": "Driver",
            "password": "Test@1234",
        }
        resp = client.post("/api/v1/crew", json=crew_payload, headers=headers)
        assert resp.status_code == 200, f"Crew create failed: {resp.text}"
        crew_data = resp.json()["data"]
        assert crew_data["crew_id"] == "CR002"
        assert crew_data["is_active"] is True

        # ── Step 2: Create CMS Record ────────────────────────────────
        cms_payload = {
            "crew_id": "CR002",
            "crew_name": "Alice Conductor",
            "crew_designation": "Driver",
            "fortnight_hours": "80",
            "avail_time": "08:00",
            "avail_station": "NDLS",
            "status": "Available",
            "called_time": "06:00",
            "ack_time": "06:15",
            "sign_on_time": "07:00",
            "last_signoff_time": "",
            "train_no": "12627",
            "from_station": "NDLS",
            "to_station": "BCT",
        }
        resp = client.post("/api/v1/cms", json=cms_payload, headers=headers)
        assert resp.status_code == 200, f"CMS create failed: {resp.text}"
        cms_data = resp.json()["data"]
        cms_id = cms_data["id"]

        # ── Step 3: Sign On ──────────────────────────────────────────
        signon_payload = {
            "cms_id": cms_id,
            "crew_id": "CR002",
            "crew_name": "Alice Conductor",
            "status": "SignedOn",
            "train_no": "12627",
            "from_station": "NDLS",
            "to_station": "BCT",
            "sign_on_time": "07:00",
            "cto_train_no": "12627",
            "cto_station": "BCT",
            "cto_time": "08:00",
            "loco1": "L001",
            "loco2": "",
            "loco3": "",
            "shed": "SHED_A",
        }
        resp = client.post("/api/v1/signon", json=signon_payload, headers=headers)
        assert resp.status_code == 200, f"SignOn create failed: {resp.text}"
        result = resp.json()["data"]
        signon_data = result["signon"]
        main_data_created = result["main_data"]

        # Verify SignOn was created
        assert signon_data["crew_id"] == "CR002"
        assert signon_data["is_active"] is True
        signon_id = signon_data["id"]

        # Verify MainData was automatically created
        assert main_data_created is not None
        assert main_data_created["crew_id"] == "CR002"
        assert main_data_created["is_active"] is True
        main_data_id = main_data_created["id"]

        # ── Step 4: Archive ───────────────────────────────────────────
        resp = client.post(
            f"/api/v1/archive/main/{main_data_id}", headers=headers
        )
        assert resp.status_code == 200, f"Archive failed: {resp.text}"
        archive_data = resp.json()["data"]
        assert archive_data["crew_id"] == "CR002"

        # ── Step 5: Verify Archive in DB ──────────────────────────────
        archived = db_session.query(ArchiveData).filter(
            ArchiveData.crew_id == "CR002"
        ).first()
        assert archived is not None
        assert archived.is_active is False

        # Verify MainData was soft-deleted
        main_deleted = db_session.query(MainData).filter(
            MainData.id == main_data_id
        ).first()
        assert main_deleted is not None
        assert main_deleted.is_active is False

        # ── Step 6: Verify Audit Log ─────────────────────────────────
        audit_logs = db_session.query(AuditLog).all()
        # Should have at least: CREATE(Crew), CREATE(CMS), CREATE(SignOn), ARCHIVE
        entities_seen = {log.entity for log in audit_logs}
        assert "Crew" in entities_seen or "crew" in str(
            [log.entity for log in audit_logs]
        )
        assert "ArchiveData" in entities_seen or "archive" in str(
            [log.entity for log in audit_logs]
        ).lower()


class TestWorkflow2_DuplicateSignOn:
    """
    Workflow 2: Duplicate SignOn → 400 Bad Request
    """

    def test_duplicate_signon_returns_400(
        self,
        client: TestClient,
        admin_token: str,
        sample_crew: Crew,
        sample_cms: CMSData,
        db_session: Session,
    ):
        headers = {"Authorization": f"Bearer {admin_token}"}

        # Create a fresh CMS for this test
        cms_payload = {
            "crew_id": sample_crew.crew_id,
            "crew_name": sample_crew.full_name,
            "crew_designation": sample_crew.designation,
            "fortnight_hours": "80",
            "avail_time": "09:00",
            "avail_station": "NDLS",
            "status": "Available",
            "called_time": "07:00",
            "ack_time": "07:15",
            "sign_on_time": "08:00",
            "last_signoff_time": "",
            "train_no": "12346",
            "from_station": "NDLS",
            "to_station": "BCT",
        }
        resp = client.post("/api/v1/cms", json=cms_payload, headers=headers)
        assert resp.status_code == 200, f"CMS create failed: {resp.text}"
        cms_id = resp.json()["data"]["id"]

        # Sign On — first time: should succeed
        signon_payload = {
            "cms_id": cms_id,
            "crew_id": sample_crew.crew_id,
            "crew_name": sample_crew.full_name,
            "status": "SignedOn",
            "train_no": "12346",
            "from_station": "NDLS",
            "to_station": "BCT",
            "sign_on_time": "08:00",
            "cto_train_no": "12346",
            "cto_station": "BCT",
            "cto_time": "09:00",
            "loco1": "L002",
            "loco2": "",
            "loco3": "",
            "shed": "SHED_B",
        }
        resp = client.post("/api/v1/signon", json=signon_payload, headers=headers)
        assert resp.status_code == 200, f"First SignOn should succeed: {resp.text}"

        # Duplicate SignOn for the same CMS → 400
        resp = client.post("/api/v1/signon", json=signon_payload, headers=headers)
        assert resp.status_code == 400, f"Duplicate SignOn should return 400, got {resp.status_code}: {resp.text}"
        assert "already exists" in resp.json().get("detail", resp.json().get("message", "")).lower()


class TestWorkflow3_DoubleArchive:
    """
    Workflow 3: Archive the same MainData twice → Error
    """

    def test_double_archive_returns_error(
        self,
        client: TestClient,
        admin_token: str,
        sample_maindata: MainData,
        db_session: Session,
    ):
        headers = {"Authorization": f"Bearer {admin_token}"}
        main_data_id = sample_maindata.id

        # First archive: should succeed
        resp = client.post(f"/api/v1/archive/main/{main_data_id}", headers=headers)
        assert resp.status_code == 200, f"First archive should succeed: {resp.text}"

        # Second archive: should fail (already archived / inactive)
        resp = client.post(f"/api/v1/archive/main/{main_data_id}", headers=headers)
        assert resp.status_code == 400, f"Second archive should fail, got {resp.status_code}: {resp.text}"
        err_msg = resp.json().get("detail", resp.json().get("message", "")).lower()
        assert "already archived" in err_msg or \
               "inactive" in err_msg or \
               "not found" in err_msg or \
               resp.status_code == 404


class TestWorkflow4_DeactivatedCrewSignOn:
    """
    Workflow 4: Deactivate Crew → Try SignOn → Not Allowed
    """

    def test_deactivated_crew_cannot_signon(
        self,
        client: TestClient,
        admin_token: str,
        sample_crew: Crew,
        sample_cms: CMSData,
        db_session: Session,
    ):
        headers = {"Authorization": f"Bearer {admin_token}"}
        crew_id = sample_crew.crew_id

        # Deactivate the crew
        resp = client.delete(f"/api/v1/crew/{crew_id}", headers=headers)
        assert resp.status_code == 200, f"Crew deactivate failed: {resp.text}"

        # Verify crew is inactive
        db_session.refresh(sample_crew)
        assert sample_crew.is_active is False

        # Try to SignOn as deactivated crew → 400
        signon_payload = {
            "cms_id": sample_cms.id,
            "crew_id": crew_id,
            "crew_name": sample_crew.full_name,
            "status": "SignedOn",
            "train_no": "12345",
            "from_station": "NDLS",
            "to_station": "BCT",
            "sign_on_time": "07:00",
            "cto_train_no": "12345",
            "cto_station": "BCT",
            "cto_time": "08:00",
            "loco1": "L001",
            "loco2": "",
            "loco3": "",
            "shed": "SHED_A",
        }
        resp = client.post("/api/v1/signon", json=signon_payload, headers=headers)
        assert resp.status_code in (400, 404), (
            f"SignOn for deactivated crew should fail, got {resp.status_code}: {resp.text}"
        )
        err_msg = resp.json().get("detail", resp.json().get("message", "")).lower()
        assert "inactive" in err_msg or \
               "not found" in err_msg


class TestWorkflow5_UnauthorizedDelete:
    """
    Workflow 5: Unauthorized (viewer) user tries to delete Crew → 403
    """

    def test_viewer_cannot_delete_crew(
        self,
        client: TestClient,
        viewer_token: str,
        sample_crew: Crew,
        db_session: Session,
    ):
        headers = {"Authorization": f"Bearer {viewer_token}"}

        resp = client.delete(f"/api/v1/crew/{sample_crew.crew_id}", headers=headers)
        assert resp.status_code == 403, (
            f"Viewer delete should return 403, got {resp.status_code}: {resp.text}"
        )

        # Verify crew still exists (not deleted)
        db_session.refresh(sample_crew)
        assert sample_crew.is_active is True

    def test_viewer_can_read_crew(
        self,
        client: TestClient,
        viewer_token: str,
        sample_crew: Crew,
    ):
        """Viewer should still be able to read crew data."""
        headers = {"Authorization": f"Bearer {viewer_token}"}
        resp = client.get(f"/api/v1/crew/{sample_crew.crew_id}", headers=headers)
        assert resp.status_code == 200

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_rejects_unsupported_formats():
    client = TestClient(app)
    for unsupported_filename in ["image.png", "photo.jpg", "archive.zip", "script.exe"]:
        response = client.post(
            "/api/upload",
            files={"file": (unsupported_filename, b"dummy content", "application/octet-stream")},
        )
        assert response.status_code == 415
        assert "Unsupported file type" in response.json()["detail"]


def test_upload_accepts_supported_formats():
    client = TestClient(app)
    for supported_filename in [
        "doc.pdf",
        "doc.docx",
        "doc.pptx",
        "data.xlsx",
        "data.csv",
        "notes.txt",
        "readme.md",
        "guide.markdown",
    ]:
        response = client.post(
            "/api/upload",
            files={"file": (supported_filename, b"valid content", "application/octet-stream")},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "uploaded"
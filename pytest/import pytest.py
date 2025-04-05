import pytest
from httpx import AsyncClient
from main import app  # Importera FastAPI-appen

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

# ===========================
# 🟢 GET-REQUESTS TESTER
# ===========================

@pytest.mark.asyncio
async def test_get_students(client):
    response = await client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_student_by_id(client):
    response = await client.get("/students/1")
    if response.status_code == 200:
        assert "student_id" in response.json()
    else:
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_search_students(client):
    response = await client.get("/students/filter?name=John")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_invalid_student(client):
    response = await client.get("/students/99999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_courses(client):
    response = await client.get("/courses")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_course_by_id(client):
    response = await client.get("/courses/1")
    if response.status_code == 200:
        assert "course_id" in response.json()
    else:
        assert response.status_code == 404

# ===========================
# 🟢 POST-REQUESTS TESTER
# ===========================

@pytest.mark.asyncio
async def test_create_student(client):
    new_student = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "birthdate": "2000-05-15"
    }
    response = await client.post("/students", json=new_student)
    assert response.status_code == 201
    assert "student_id" in response.json()

@pytest.mark.asyncio
async def test_create_instructor(client):
    new_instructor = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@example.com",
        "department_id": 1
    }
    response = await client.post("/instructors", json=new_instructor)
    assert response.status_code == 201
    assert "instructor_id" in response.json()

@pytest.mark.asyncio
async def test_create_student_invalid_email(client):
    new_student = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "invalid-email",
        "birthdate": "1999-12-12"
    }
    response = await client.post("/students", json=new_student)
    assert response.status_code == 400  # Felaktig email ska ge 400

# ===========================
# 🟢 DELETE-REQUESTS TESTER
# ===========================

@pytest.mark.asyncio
async def test_delete_student(client):
    response = await client.delete("/students/1")
    if response.status_code == 200:
        assert "message" in response.json()
    else:
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_invalid_course(client):
    response = await client.delete("/courses/99999")
    assert response.status_code == 404

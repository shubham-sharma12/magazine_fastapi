import random
from app.schemas import UserCreate
from app.schemas import MagazineCreate


def create_user(client, username, email, password):
    response = client.post(
        "/users/register",
        json={"username": username, "email": email, "password": password},
    )
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code}, Response body: {response.text}"
    user = response.json()
    return user["username"], user["id"]


def login_user(client, username: str, password: str):
    response = client.post(
        "/users/login", json={"username": username, "password": password}
    )
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code}, Response body: {response.text}"
    return response.json()["access_token"]


def create_plan(client, headers):
    magazine = create_magazine(client, headers, "plan")
    response = client.post(
        "/plans/",
        json={"name": "Monthly", "price": 100, "magazine_id": magazine["id"]},
        headers=headers,
    )
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code}, Response body: {response.text}"
    return response.json()


def create_magazine(client, headers, name_suffix, base_price=100):
    magazine_data = MagazineCreate(
        title=f"Magazine {name_suffix}",
        description=f"Description {name_suffix}",
        base_price=base_price,
    )
    response = client.post("/magazines/", json=magazine_data.dict(), headers=headers)
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code}, Response body: {response.text}"
    print(
        f"Created magazine: Magazine {name_suffix}, Description {name_suffix}, {base_price}"
    )
    return response.json()


def generate_random_plan_name():
    random_words = ["Silver", "Gold", "Platinum", "Diamond", "Titanium"]
    random_suffix = random.randint(1000, 9999)
    return f"{random.choice(random_words)} Plan {random_suffix}"

from fastapi.testclient import TestClient

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from api.server import app  # noqa: E402


def test_E2E():
    with TestClient(app) as client:
        # check that the database is empty
        response = client.get("/todo")

        assert len(response.json()) == 0
        assert response.status_code == 200

        # create 3 items
        for i in range(1, 4):
            data = {
                "title": f"todo_{i}",
                "description": f"description_{i}",
                "state": "TODO"
            }
            response = client.post("/todo", json=data)
            assert response.status_code == 201

        # test the get_item_by_id function
        response = client.get("/todo/1")

        assert response.json()["title"] == "todo_1"
        assert response.status_code == 200

        # test the update function
        data = {
                "title": "todo_2",
                "description": "description_2_modified",
                "state": "DONE"
            }
        response = client.put("/todo/2", json=data)

        assert response.json()["description"] == "description_2_modified"

        # test the delete function
        response = client.delete("/todo/3")

        assert response.status_code == 204

        # test the get_all_items function
        response = client.get("/todo")
        assert len(response.json()) == 2
        assert response.status_code == 200

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Hellu mai Zâu'ss Mezzy xinh đẹp tuỵt zời cụa tui"

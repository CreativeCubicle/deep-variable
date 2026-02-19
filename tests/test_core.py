from deep_variable import DeepVariable


def test_basic_get():
    data = {"user": {"name": "Krishna"}}
    assert DeepVariable.get(data, "user.name") == "Krishna"

def test_missing_key():
    data = {"user": {"name": "Krishna"}}
    assert DeepVariable.get(data, "user.email", default="N/A") == "N/A"

def test_list_access():
    data = {"users": [{"id": 1}, {"id": 2}]}
    assert DeepVariable.get(data, "users.1.id") == 2


def test_has_existence():
    data = {"a": {"b": None}}
    assert DeepVariable.has(data, "a.b") is True
    assert DeepVariable.has(data, "a.c") is False

def test_set_new_path():
    data = {}
    DeepVariable.set(data, "organization.team.member", "Krishna")
    assert data["organization"]["team"]["member"] == "Krishna"

def test_set_overwrites():
    data = {"score": 10}
    DeepVariable.set(data, "score", 20)
    assert data["score"] == 20


def test_root_is_list():
    """Ensure we can start traversal even if the root object is a list."""
    data = [{"id": 1}, {"id": 2}]
    assert DeepVariable.get(data, "0.id") == 1
    assert DeepVariable.get(data, "1.id") == 2

def test_nested_list_navigation():
    """Test deep navigation through mixed dicts and lists."""
    data = {
        "teams": [
            {"members": ["Alice", "Bob"]},
            {"members": ["Charlie", "David"]}
        ]
    }
    # Path through dict -> list -> dict -> list
    assert DeepVariable.get(data, "teams.1.members.0") == "Charlie"

def test_list_index_out_of_bounds():
    """Ensure it returns the default value instead of an IndexError."""
    data = ["a", "b", "c"]
    assert DeepVariable.get(data, "5", default="Missing") == "Missing"

def test_invalid_list_index_type():
    """Ensure non-integer keys on a list return the default."""
    data = ["a", "b", "c"]
    # Trying to access a list using a string key like a dict
    assert DeepVariable.get(data, "first_item", default="Not Found") == "Not Found"

def test_has_with_lists():
    """Verify existence checking works for list indices."""
    data = {"items": [None, 0, False]}
    # Even if the value is 'falsy', the index exists
    assert DeepVariable.has(data, "items.0") is True
    assert DeepVariable.has(data, "items.3") is False

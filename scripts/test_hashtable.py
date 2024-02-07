from hash_table import HashTable
import pytest
from pytest_unordered import unordered

@pytest.fixture
def hashtable():
    sample_data = HashTable(capacity=100)
    sample_data["name"] = "Lorena"
    sample_data[55] = 34.99
    sample_data[False] = True
    return sample_data

def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None

def test_should_report_length_of_empty_hashtable():
    assert len(HashTable(capacity=100)) == 0

def test_should_report_length(hashtable):
    assert len(hashtable) == 3

def test_should_report_capacity_of_empty_hashtable():
    assert HashTable(capacity=100).capacity == 100

def test_should_report_capacity(hashtable):
    assert hashtable.capacity == 100

def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)

def test_should_not_create_hashtable_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-100)

def test_should_create_empty_item_slots():
    assert HashTable(capacity=3)._slots == [None, None, None]

def test_should_insert_key_value_pairs():
    hashtable = HashTable(capacity=100)
    hashtable["name"] = "Lorena"
    hashtable[55] = 34.99
    hashtable[False] = True    
    assert ("name", "Lorena") in hashtable.items
    assert (55, 34.99) in hashtable.items
    assert (False, True) in hashtable.items
    assert len(hashtable) == 3
    
def test_should_not_grow_its_size():
    hashtable = HashTable(capacity=1)
    hashtable["name"] = "Lorena"
    assert len(hashtable) == 1

def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=100).values

def test_should_insert_none_value():
    hashtable = HashTable(capacity=100)
    hashtable["key"] = None
    assert ("key", None) in hashtable.items

def test_should_find_value_by_key(hashtable):
    assert hashtable["name"] == "Lorena"
    assert hashtable[55] == 34.99
    assert hashtable[False] == True

def test_should_raise_error_on_missing_key():
    hashtable = HashTable(capacity=100)
    with pytest.raises(KeyError) as exception_info:
        hashtable["missing_key"]
    assert exception_info.value.args[0] == "missing_key"

def test_should_find_key(hashtable):
    assert "name" in hashtable

def test_should_not_find_key(hashtable):
    assert "age" not in hashtable

def test_should_get_value(hashtable):
    assert hashtable.get("name") == "Lorena"

def test_should_get_none_when_missing_key(hashtable):
    assert hashtable.get("age") is None

def test_should_get_default_value_when_missing_key(hashtable):
    assert hashtable.get("age", 30) == 30

def test_should_get_value_with_default(hashtable):
    assert hashtable.get("name", "Maria") == "Lorena"

def test_should_delete_key_value_pair(hashtable):
    assert "name" in hashtable
    assert ("name", "Lorena") in hashtable.items
    assert len(hashtable) == 3

    del hashtable["name"]

    assert "name" not in hashtable
    assert ("name", "Lorena") not in hashtable.items
    assert len(hashtable) == 2

def test_should_raise_key_error_when_deleting_missing_key(hashtable):
    with pytest.raises(KeyError) as exception_info:
        del hashtable["missing_key"]
    assert exception_info.value.args[0] == "missing_key"

def test_should_update_value(hashtable):
    assert hashtable["name"] == "Lorena"
    
    hashtable["name"] = "Maria"

    assert hashtable["name"] == "Maria"
    assert hashtable[55] == 34.99
    assert hashtable[False] == True
    assert len(hashtable) == 3

def test_should_return_pairs(hashtable):
    assert hashtable.items == {
        ("name", "Lorena"),
        (55, 34.99),
        (False, True)}

def test_should_return_values(hashtable):
    assert unordered(hashtable.values) == ["Lorena", 34.99, True]  
    
def test_should_return_keys(hashtable):
    assert hashtable.keys == {"name", 55, False}

def test_should_return_copy_of_pairs(hashtable):
    assert hashtable.items is not hashtable.items

def test_should_not_include_blank_pairs(hashtable):
    assert None not in hashtable.items

def test_should_return_duplicate_values():
    hashtable = HashTable(capacity=100)
    hashtable["Lorena"] = 30
    hashtable["Joana"] = 45
    hashtable["Fernanda"] = 45
    assert [30, 45, 45] == sorted(hashtable.values)

def test_should_get_values_of_empty_hash_table():
    assert HashTable(capacity=100).values == []

def test_should_return_copy_of_values(hashtable):
    assert hashtable.values is not hashtable.values

def test_should_get_keys_of_empty_hash_table():
    assert HashTable(capacity=100).keys == set()

def test_should_return_copy_of_keys(hashtable):
    assert hashtable.keys is not hashtable.keys

def test_should_convert_to_dict(hashtable):
    dictionary = dict(hashtable.items)
    assert set(dictionary.items()) == hashtable.items
    assert set(dictionary.keys()) == hashtable.keys
    assert list(dictionary.values()) == unordered(hashtable.values)

def test_should_iterate_over_items(hashtable):
    for key, value in hashtable.items:
        assert key in hashtable.keys
        assert value in hashtable.values

def test_should_iterate_over_keys(hashtable):
    for key in hashtable.keys:
        assert key in ("name", 55, False)

def test_should_iterate_over_values(hashtable):
    for value in hashtable.values:
        assert value in ("Lorena", 34.99, True)

def test_should_iterate_over_instance(hashtable):
    for key in hashtable:
        assert key in ("name", 55, False)

def test_should_use_literal_for_str(hashtable):
    assert str(hashtable) in {
        "{'name': 'Lorena', 55: 34.99, False: True}",
        "{'name': 'Lorena', False: True, 55: 34.99}",
        "{55: 34.99, 'name': 'Lorena', False: True}",
        "{55: 34.99, False: True, 'name': 'Lorena'}",
        "{False: True, 'name': 'Lorena', 55: 34.99}",
        "{False: True, 55: 34.99, 'name': 'Lorena'}",
    }
from hash_table import HashTable
import pytest
from unittest.mock import patch
from collections import deque

def test_should_detect_hash_collision():
    assert hash("foobar") not in [1, 2, 3]
    with patch("builtins.hash", side_effect=[1, 2, 3]):
        assert hash("foobar") == 1
        assert hash("foobar") == 2
        assert hash("foobar") == 3

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
    assert HashTable(capacity=3)._buckets == [deque()] * 3

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
    assert hashtable.items == [
        ("name", "Lorena"),
        (55, 34.99),
        (False, True)]

def test_should_return_keys(hashtable):
    assert hashtable.keys == ["name", 55, False]
    
def test_should_return_values(hashtable):
    assert hashtable.values == ["Lorena", 34.99, True]  
    
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
    assert HashTable(capacity=100).keys == []

def test_should_return_copy_of_keys(hashtable):
    assert hashtable.keys is not hashtable.keys

def test_should_convert_to_dict(hashtable):
    dictionary = dict(hashtable.items)
    assert list(dictionary.items()) == hashtable.items
    assert list(dictionary.keys()) == hashtable.keys
    assert list(dictionary.values()) == hashtable.values

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

def test_should_create_hashtable_from_dict():
    dictionary = {"name": "Lorena", 55: 34.99, False: True}
    hashtable = HashTable.from_dict(dictionary)

    assert hashtable.capacity == len(dictionary) * 2
    assert hashtable.items == list(dictionary.items())
    assert hashtable.keys == list(dictionary.keys())
    assert hashtable.values == list(dictionary.values())

def test_should_create_hashtable_from_dict_with_custom_capacity():
    dictionary = {"name": "Lorena", 55: 34.99, False: True}
    hashtable = HashTable.from_dict(dictionary, capacity=100)
    assert hashtable.capacity == 100
    assert hashtable.items == list(dictionary.items())
    assert hashtable.keys == list(dictionary.keys())
    assert hashtable.values == list(dictionary.values())

def test_should_have_canonical_string_representation(hashtable):
    assert repr(hashtable) in {
        "HashTable.from_dict({'name': 'Lorena', 55: 34.99, False: True})",
        "HashTable.from_dict({'name': 'Lorena', False: True, 55: 34.99})",
        "HashTable.from_dict({55: 34.99, 'name': 'Lorena', False: True})",
        "HashTable.from_dict({55: 34.99, False: True, 'name': 'Lorena'})",
        "HashTable.from_dict({False: True, 'name': 'Lorena', 55: 34.99})",
        "HashTable.from_dict({False: True, 55: 34.99, 'name': 'Lorena'})",
    }

def test_should_compare_equal_to_itself(hashtable):
    assert hashtable == hashtable

def test_should_compare_equal_to_copy(hashtable):
    assert hashtable is not hashtable.copy()
    assert hashtable == hashtable.copy()

def test_should_compare_equal_different_key_value_order():
    h1 = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    h2 = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    assert h1 == h2

def test_should_compare_unequal(hashtable):
    other = HashTable.from_dict({"a": 1, "b": 2, "c": 3})
    assert hashtable != other 

def test_should_compare_unequal_another_data_type(hashtable):
    assert hashtable != 42

def test_should_copy_key_values_pairs_capacity(hashtable):
    copy = hashtable.copy()

    assert copy is not hashtable
    assert copy.items == hashtable.items
    assert copy.keys == hashtable.keys
    assert copy.values == hashtable.values
    assert copy.capacity == hashtable.capacity
    

def test_should_compare_equal_different_capacity():
    dictionary = {"a": 1, "b": 2, "c": 3}
    h1 = HashTable.from_dict(dictionary, capacity=100)
    h2 = HashTable.from_dict(dictionary, capacity=300)

    assert h1 == h2

def test_should_empty_populated_hashtable(hashtable):
    assert hashtable.capacity == 100
    assert len(hashtable) == 3

    hashtable.clear()
    
    assert hashtable.capacity == 100
    assert len(hashtable) == 0

def test_should_update_hashtable_with_items_from_dict(hashtable):
    assert len(hashtable) == 3
    assert hashtable.items == [
        ("name", "Lorena"),
        (55, 34.99),
        (False, True)]
    assert hashtable.keys == ["name", 55, False]
    assert hashtable.values == ["Lorena", 34.99, True]
    assert hashtable.capacity == 100

    dictionary = {"age": 30, "email": "lorenaax.bastos@hotmail.com"}
    hashtable.update(dictionary)

    assert len(hashtable) == 5
    assert hashtable.items == [
        ("name", "Lorena"),
        (55, 34.99),
        (False, True),
        ("age", 30),
        ("email", "lorenaax.bastos@hotmail.com")]
    assert hashtable.keys == ["name", 55, False, "age", "email"]
    assert hashtable.values == ["Lorena", 34.99, True, 30, "lorenaax.bastos@hotmail.com"]
    assert hashtable.capacity == 100
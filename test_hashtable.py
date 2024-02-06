from hash_table import HashTable

def test_should_create_hashtable():
    assert HashTable(capacity=100) is not None

def test_should_report_capacity():
    assert len(HashTable(capacity=100)) == 100

def test_should_create_empty_value_slots():
    expected_values = [None, None, None]
    hashtable = HashTable(capacity=3)
    actual_values = hashtable.values
    assert actual_values == expected_values
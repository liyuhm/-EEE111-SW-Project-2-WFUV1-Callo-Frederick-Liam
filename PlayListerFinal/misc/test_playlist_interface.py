import db_if

def test_insert():
    for entry in range(30):
        db_if.insert_employee(entry, f'Name{entry} Surname{entry}', f'SW Engineer {entry}', 'MALE', 'NEW')
        assert db_if.id_exists(entry)

    all_entries = db_if.fetch_employees()
    assert len(all_entries) == 30

def test_update():
    for entry in range(10, 20):
        db_if.update_employee(f'Name{entry} Surname{entry}', f'SW Engineer {entry}', 'FEMALE', 'UPDATED', entry)
        assert db_if.id_exists(entry)

    all_entries = db_if.fetch_employees()
    assert len(all_entries) == 30

def test_delete():
    for entry in range(10):
        db_if.delete_employee(entry)
        assert not db_if.id_exists(entry) 

    all_entries = db_if.fetch_employees()
    assert len(all_entries) == 20
import pytest
import sqlite3
from DB.Database import Database

# Setup de la base de données pour les tests
@pytest.fixture(scope="module")
def db():
    # Utiliser une base de données de test
    test_db = Database()
    test_db.cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));")
    yield test_db
    # Nettoyer la base de données après les tests
    test_db.cursor.execute("DROP TABLE IF EXISTS test_table;")
    test_db.close()

def test_connection(db):
    """Vérifie que la connexion à la base de données fonctionne."""
    assert db.conn is not None
    assert db.cursor is not None

def test_dml_insert(db):
    """Teste l'insertion de données avec DML."""
    insert_query = "INSERT INTO test_table (name) VALUES (%s);"
    db.DML(insert_query, ("TestName",))
    db.conn.commit()  # Commit les changements
    # Vérifie que les données ont été insérées
    db.cursor.execute("SELECT COUNT(*) FROM test_table WHERE name = 'TestName';")
    count = db.cursor.fetchone()[0]
    assert count == 1

def test_dql_select(db):
    """Teste la récupération de données avec DQL."""
    select_query = "SELECT * FROM test_table WHERE name = %s;"
    result = db.DQL(select_query, ("TestName",))
    assert len(result) == 1
    assert result[0]["name"] == "TestName"

def test_dml_update(db):
    """Teste la mise à jour de données avec DML."""
    update_query = "UPDATE test_table SET name = %s WHERE name = %s;"
    db.DML(update_query, ("UpdatedName", "TestName"))
    db.conn.commit()
    # Vérifie que les données ont été mises à jour
    db.cursor.execute("SELECT COUNT(*) FROM test_table WHERE name = 'UpdatedName';")
    count = db.cursor.fetchone()[0]
    assert count == 1

def test_dml_delete(db):
    """Teste la suppression de données avec DML."""
    delete_query = "DELETE FROM test_table WHERE name = %s;"
    db.DML(delete_query, ("UpdatedName",))
    db.conn.commit()
    # Vérifie que les données ont été supprimées
    db.cursor.execute("SELECT COUNT(*) FROM test_table WHERE name = 'UpdatedName';")
    count = db.cursor.fetchone()[0]
    assert count == 0
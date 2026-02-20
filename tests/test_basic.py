#test_basic.py

import tempfile
import shutil
from erabytse_rememoir import RememoirDB

def test_add_and_search_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = RememoirDB(user_id="test", db_path=tmpdir)
        db.add("I love open-source AI", content_type="note")
        results = db.search("What do I love?", k=1)
        assert len(results) == 1
        assert "open-source" in results[0].content

def test_user_isolation():
    with tempfile.TemporaryDirectory() as tmpdir:
        db1 = RememoirDB(user_id="alice", db_path=tmpdir)
        db2 = RememoirDB(user_id="bob", db_path=tmpdir)
        db1.add("Alice secret")
        db2.add("Bob secret")
        alice_results = db1.search("secret")
        bob_results = db2.search("secret")
        assert all("Alice" in r.content for r in alice_results)
        assert all("Bob" in r.content for r in bob_results)
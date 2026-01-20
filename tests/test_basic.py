#test_basic.py

def test_add_and_search():
    from erabytse_rememoir import RememoirDB
    db = RememoirDB("test_user")
    db.add("I love open-source AI")
    results = db.search("What do I love?")
    assert len(results) > 0
    assert "open-source" in results[0].content
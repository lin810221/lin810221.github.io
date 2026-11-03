"""A cache key varies by principal, scopes, arguments and schema revision."""
from integration_core import ALICE, BOB, Principal, cache_key


if __name__ == "__main__":
    args = {"query": "MCP"}
    reduced = Principal(ALICE.tenant, ALICE.subject, frozenset({"notes:read"}))
    keys = [cache_key(p, "schema-v1", "search_notes", args) for p in (ALICE, BOB, reduced)]
    assert len(set(keys)) == 3
    assert keys[0] != cache_key(ALICE, "schema-v2", "search_notes", args)
    print("tenant / scope / schema isolation: PASS")

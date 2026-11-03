"""Authorization is enforced before searching, not just in a model prompt."""
from integration_core import ALICE, BOB, Principal, search_notes


if __name__ == "__main__":
    assert search_notes(ALICE, "beta") == []
    assert search_notes(BOB, "beta")[0]["id"] == "N3"
    try:
        search_notes(Principal("alpha", "eve", frozenset()), "MCP")
    except PermissionError:
        print("missing scope rejected")
    print("cross-tenant search isolation: PASS")

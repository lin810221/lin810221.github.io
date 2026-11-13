"""11: known_and_assumed. Original fictional educational example."""
from psych_core import thought_case
case=thought_case("meeting")
for key in ("observation","interpretation","alternative","action"):print(key,case[key])

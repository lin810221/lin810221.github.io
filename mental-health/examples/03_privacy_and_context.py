"""03: privacy_and_context. Original fictional educational example."""
from psych_core import coverage
print(coverage({"synthetic":True,"consent_to_share":False,"purpose":"education"},["synthetic","purpose","consent_to_share","retention_policy"]))
print("明確拒絕分享是已知資訊，不是缺漏。")

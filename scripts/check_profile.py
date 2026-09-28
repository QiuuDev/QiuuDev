"""Small offline check for privacy filtering, escaping, and calendar placement."""
import xml.etree.ElementTree as ET
from update_profile import render

public = dict(name="test<&", private=False, fork=False, size=1, pushed_at="2026-01-02T00:00:00Z", language="PHP", stargazers_count=2)
private = dict(public, name="DO_NOT_PUBLISH", private=True, stargazers_count=999)
calendar = {"totalContributions":3,"weeks":[{"contributionDays":[{"date":"2026-01-02","weekday":5,"contributionCount":3}]}]}
result = render({"followers":1},[public,private],calendar,"2026-01-02")
assert len(result) == 4
for name, content in result.items():
    root = ET.fromstring(content)
    assert "DO_NOT_PUBLISH" not in content
    if name.startswith("activity"):
        assert "test&lt;&amp;" in content
        assert ">999<" not in content
    else:
        assert 'y="210"' in content  # Friday in a partial first week.
print("Profile checks passed: private repos excluded, text escaped, dates positioned correctly.")

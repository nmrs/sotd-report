import re

text1 = "Murphy and McNeill - Cat Power"

pattern = re.compile(r"\bmurphy\s+(?:&|and|\+)\s+mcneill?\b", re.IGNORECASE)

result1 = pattern.sub('', text1)

print(result1)

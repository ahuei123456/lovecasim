import re

text = "山札の上から3枚見て、その中から1枚を手札に加え、残りを山札の下に置く。"
pattern = r"(?:デッキ|山札).*?(\d+)枚.*?見る"
match = re.search(pattern, text)
print(f"Match: {match}")
if match:
    print(match.groups())

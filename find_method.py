with open(r"d:\Projects\lovecasim\engine\game\game_state.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def _check_condition" in line:
        print(f"Found method at line {i+1}: {line.strip()}")

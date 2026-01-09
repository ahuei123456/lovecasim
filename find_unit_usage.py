import os

search_dir = r"d:\Projects\lovecasim\engine\tests"
keyword = ".unit"

print(f"Searching for '{keyword}' in {search_dir}...")

found_files = []
for root, _, files in os.walk(search_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if keyword in content:
                        print(f"Found in: {path}")
                        found_files.append(path)
            except Exception as e:
                print(f"Could not read {path}: {e}")

if not found_files:
    print("No matches found.")

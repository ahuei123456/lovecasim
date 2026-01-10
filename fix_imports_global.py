import os

# 1. Create ai/__init__.py
ai_init = "ai/__init__.py"
if not os.path.exists(ai_init):
    with open(ai_init, "w", encoding="utf-8") as f:
        f.write("")
    print("Created ai/__init__.py")

# 2. Fix imports helper
def fix_imports(path):
    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping binary/non-utf8 file: {path}")
        return
    
    replacements = {
        "from engine.models": "from game.models",
        "from engine.game": "from game",
        "import engine.models": "import game.models",
        "import engine.game": "import game",
        # Fix AI imports
        "from game_state": "from game.game_state",
        "import game_state": "import game.game_state"
    }
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated imports in {path}")

# 3. Scan relevant directories
def scan_and_fix(root_dirs):
    for root in root_dirs:
        if os.path.isfile(root):
            if root.endswith("fix_imports_global.py"): continue
            fix_imports(root)
            continue
            
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                if filename.endswith(".py"):
                    fix_imports(os.path.join(dirpath, filename))

files_to_scan = [
    "game",
    "server.py",
    "ai",
    "compiler",
    "tests"
]

scan_and_fix(files_to_scan)

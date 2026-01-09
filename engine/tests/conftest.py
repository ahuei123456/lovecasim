import sys
from pathlib import Path

# Add project root to sys.path
# engine/tests/conftest.py -> parent=tests -> parent=engine -> parent=root
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

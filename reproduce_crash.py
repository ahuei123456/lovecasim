import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

def get_state():
    try:
        r = requests.get(f"{BASE_URL}/state")
        return r.json()
    except Exception as e:
        print(f"Error getting state: {e}")
        return {}

def do_action(action_id):
    try:
        r = requests.post(f"{BASE_URL}/action", json={"action_id": action_id})
        if r.status_code == 500:
            print(f"CRASH CAUGHT! 500 Error on action {action_id}")
            import os
            abs_path = os.path.abspath("crash_log.txt")
            with open(abs_path, "w", encoding='utf-8') as f:
                f.write(r.text)
            print(f"Wrote crash log to {abs_path}")
            return False
        return r.json()
    except Exception as e:
        print(f"Error doing action: {e}")
        return False

# Attempt to fast forward to Live Set phase
print("Starting reproduction...")
state = get_state()
print(f"Initial Phase: {state.get('phase')}")

# We need to get to Phase 5 (LIVE_SET)
# Usually: Mulligan -> Active -> Energy -> Draw -> Main -> Live Set
# I'll just try to force action 0 repeatedly to skip phases until we hit something interesting or crash
for i in range(20):
    res = do_action(0) # Pass/Skip
    if not res: break
    
    state = res.get('state', {})
    phase = state.get('phase')
    print(f"Step {i}: Phase {phase}")
    
    if phase == 5: # LIVE_SET
        # Try to set a live (Action 400+)
        legal = state.get('legal_actions', [])
        live_acts = [a['id'] for a in legal if 400 <= a['id'] <= 459]
        if live_acts:
            print(f"Attempting Live Set with action {live_acts[0]}")
            do_action(live_acts[0])
            break

# Test Image Serving
print("Testing Image Serving...")
try:
    # Verify that we can fetch an image using the new 'img/' prefix logic
    # We need a valid card ID to simulate what the frontend sees
    # Let's just ask for 'img/cards/BP01/PL!HS-bp1-001-C.png' (example)
    # or just list one fro server if possible.
    # Actually, let's just use a hardcoded path we know exists or close to it
    # I saw 'icon_blade.png' in 'img' dir in previous step
    test_url = f"{BASE_URL}/../img/icon_blade.png" # url is relative to /api/.. so /img/..
    # Correct URL: http://127.0.0.1:5000/img/icon_blade.png
    url = "http://127.0.0.1:5000/img/icon_blade.png"
    r = requests.get(url)
    if r.status_code == 200:
        print("Success: Image fetched correctly")
    else:
        print(f"Failure: Image fetch returned {r.status_code}")
except Exception as e:
    print(f"Image test error: {e}")

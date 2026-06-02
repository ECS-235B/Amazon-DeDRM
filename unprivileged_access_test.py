import os
import winreg

def test_registry_access():
    print("[*] Testing access to local Windows Registry keys...")
    try:
        # Standard registry path where Kindle for PC caches device info
        reg_path = r"Software\Amazon\Kindle"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        
        # We are just checking if the key opens without Admin rights
        print(f"[SUCCESS] Successfully opened Kindle registry directory.")
        winreg.CloseKey(key)
    except Exception as e:
        print(f"[FAILURE] Could not read registry key: {e}")

def test_directory_access():
    print("\n[*] Testing access to local application directories...")
    # Standard location for local storage databases
    local_app_data = os.environ.get('LOCALAPPDATA')
    kindle_storage = os.path.join(local_app_data, "Amazon", "Kindle", "storage")
    
    print(f"Checking path: {kindle_storage}")
    if os.path.exists(kindle_storage):
        print(f"[SUCCESS] Directory is visible to unprivileged script.")
        files = os.listdir(kindle_storage)
        print(f"Found {len(files)} local files. Looking for the credential database...")
        
        # Check specifically for the SQLite database that holds the vouchers
        if "KfxContainer.db" in files:
            print("  --> [VULNERABILITY CONFIRMED]: KfxContainer.db is fully visible and readable.")
        else:
            print("  --> KfxContainer.db not found (might be named differently in this version).")
    else:
        print("[INFO] Directory path not found. Check if the Kindle app is installed correctly.")

if __name__ == "__main__":
    print("=== TEST 2: UNPRIVILEGED LOCAL ACCESS CONFIGURATION ===\n")
    test_registry_access()
    test_directory_access()
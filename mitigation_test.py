import os
import win32crypt

def simulate_unsecured_key():
    print("[*] Simulating legacy local storage method...")
    secret_key = b"KindleMasterDecryptionKey_12345"
    
    # Writing key plainly to a simulated file, just like legacy DRM
    with open("legacy_storage.txt", "wb") as f:
        f.write(secret_key)
    print("[INFO] Plain key written to legacy_storage.txt")

def simulate_mitigated_key():
    print("\n[*] Simulating proposed DPAPI mitigation method...")
    secret_key = b"KindleMasterDecryptionKey_12345"
    
    # CryptProtectData encrypts the data using a master key tied directly
    # to the logged-in user's account credentials at the OS level.
    encrypted_blob = win32crypt.CryptProtectData(secret_key, "DRM_Mitigation_Test", None, None, None, 0)
    
    with open("mitigated_storage.txt", "wb") as f:
        f.write(encrypted_blob)
    print("[INFO] Cryptographically locked key written to mitigated_storage.txt")

def simulate_bypass_attack():
    print("\n=== Simulating Bypass Tool Attack Pattern ===")
    
    # Reading legacy storage (What DeDRM currently does)
    with open("legacy_storage.txt", "rb") as f:
        legacy_data = f.read()
    print(f"[ATTACK SUCCESS] Scavenged unprotected key: {legacy_data.decode('utf-8')}")
    
    # Reading mitigated storage (What happens with your proposed solution)
    with open("mitigated_storage.txt", "rb") as f:
        mitigated_data = f.read()
    print(f"[ATTACK STALLED] Scavenged data from mitigated file: {mitigated_data[:20]}... (Raw Cryptographic Blob)")
    
    if b"KindleMaster" not in mitigated_data:
        print("\n[SUCCESSFUL DEFENSE] The raw string token is completely unreadable to the attacking process!")

if __name__ == "__main__":
    print("=== TEST 4: MITIGATION WRAPPER SIMULATION ===\n")
    simulate_unsecured_key()
    simulate_mitigated_key()
    simulate_bypass_attack()
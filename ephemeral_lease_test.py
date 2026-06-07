import time

def simulate_aws_license_server():
    print("[*] SERVER: Generating a 5-second Ephemeral Key Lease...")
    # The key is bundled with an expiration timestamp
    expiration_time = time.time() + 5 
    master_key = "Kindle_Dynamic_Key_998877"
    return {"key": master_key, "expires_at": expiration_time}

def simulate_kindle_client(lease_data, delay_seconds):
    print(f"\n[*] CLIENT: Attempting to read book after {delay_seconds} seconds offline...")
    time.sleep(delay_seconds)
    
    current_time = time.time()
    
    if current_time > lease_data["expires_at"]:
        print("[BLOCKED] DRM Error: Local lease expired. The key is cryptographically void.")
        print("          Action Required: Silent background handshake with AWS needed.")
    else:
        print("[SUCCESS] Book Decrypted: Local lease is still valid.")

if __name__ == "__main__":
    print("=== TEST 5: EPHEMERAL LEASE ARCHITECTURE ===")
    
    # Simulate a user reading right after downloading (Valid)
    lease_1 = simulate_aws_license_server()
    simulate_kindle_client(lease_1, delay_seconds=2)
    
    # Simulate a bypass tool extracting the key days later (Void)
    lease_2 = simulate_aws_license_server()
    simulate_kindle_client(lease_2, delay_seconds=6)
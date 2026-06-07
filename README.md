# Amazon-DeDRM: Empirical DRM Architecture Security Analysis

This repository contains the empirical testing and simulation scripts developed for our CIS project analyzing the Digital Rights Management (DRM) architecture of the Amazon Kindle desktop client. 

Our threat modeling focuses on local credential storage vulnerabilities—specifically **CWE-284 (Improper Access Control)** and **CWE-321 (Use of Hard-coded Cryptographic Key)**—common in legacy and modern desktop DRM software. The scripts in this workspace act as proof-of-concept simulations demonstrating these weaknesses and validating our proposed engineering mitigations.

---

## 1. Project Overview

Desktop DRM systems face a fundamental security paradox: they must deliver decrypted content to a user's machine while simultaneously preventing the user from extracting the underlying decryption keys. Because the user has physical and administrative control over the execution environment, standard client-side software protections often fail. 

Our project evaluates the security lifecycle of local Kindle DRM keys on Windows. We investigate how local storage configurations allow unprivileged processes to harvest key material, simulate how OS-level credential wrapping (Windows DPAPI) raises the bar for attackers, model time-bound offline leases to limit key exposure, and demonstrate memory scraping attacks that necessitate hardware-isolated roots of trust.

---

## 2. File Directory & Script Analysis

Each script in the workspace simulates a specific phase of our threat modeling, vulnerability analysis, or mitigation testing workflow.

### 🔍 [unprivileged_access_test.py](file:///c:/Users/katka/Documents/ECS%20235/235B-Project/Amazon-DeDRM/unprivileged_access_test.py)
* **Vulnerability Class:** CWE-284: Improper Access Control
* **Description:** In legacy desktop DRM implementations, database directories and configuration parameters are often stored in standard user folders or registry directories with overly permissive access control lists (ACLs). This script queries the Windows Registry (`HKEY_CURRENT_USER\Software\Amazon\Kindle`) and checks the user's local application storage directory (`%LOCALAPPDATA%\Amazon\Kindle\storage`) for the presence of the book metadata and voucher databases (such as `KfxContainer.db`).
* **Security Implications:** It demonstrates that standard unprivileged processes running under the current user's session can navigate, read, and exfiltrate database contents. No administrative privileges (`Run as Administrator`) are required to locate the cryptographic storage directories.

### 🛡️ [mitigation_test.py](file:///c:/Users/katka/Documents/ECS%20235/235B-Project/Amazon-DeDRM/mitigation_test.py)
* **Mitigation Class:** Windows Data Protection API (DPAPI) Integration
* **Description:** To address the threat of plaintext file exposure, this script compares unsecured file-system storage with OS-wrapped storage. It uses the Windows Data Protection API (`win32crypt.CryptProtectData`) to encrypt the master key using a key derived from the user's Windows login credentials. It then simulates a bypass tool attacking both file storage configurations.
* **Security Implications:** The simulation proves that while legacy plaintext files are immediately compromised, the mitigated file prevents simple file-copy extraction. Any external tool or out-of-context process attempting to read the file encounters an opaque cryptographic blob, verifying that OS-level credential binding successfully stalls unprivileged bypass tools.

### ⏳ [ephemeral_lease_test.py](file:///c:/Users/katka/Documents/ECS%20235/235B-Project/Amazon-DeDRM/ephemeral_lease_test.py)
* **Architecture Concept:** Cryptographic Lease Expiration (Time-Bound Validity)
* **Description:** A primary flaw in traditional DRM clients is the indefinite offline validity of decrypted keys. Once a key is extracted, it remains valid forever. This script simulates an ephemeral key lease mechanism where the AWS license server bundles the decryption key with an expiration timestamp. The client decrypts content only if the system time is within the lease boundaries.
* **Security Implications:** The test script demonstrates that a key extracted after lease expiration is rendered mathematically void, forcing a silent, online cryptographic handshake. This restricts the offline window of vulnerability and mitigates the risk of persistent offline exploitation.

### 🧠 [memory_scrape_test.py](file:///c:/Users/katka/Documents/ECS%20235/235B-Project/Amazon-DeDRM/memory_scrape_test.py)
* **Attack Class:** Active RAM Scraping
* **Description:** Even if keys are securely stored on disk (e.g., using DPAPI), they must eventually be decrypted into memory (RAM) for the application to decrypt content. This script simulates an active memory scraper targeting the application process. It uses regular expression patterns to scan a simulated memory block and extract the decrypted master key.
* **Security Implications:** This simulation demonstrates that software-only mitigations are insufficient if an attacker can read active application memory. The results justify our project report's recommendation for hardware-isolated solutions, such as **Trusted Execution Environments (TEEs)** and secure enclaves, where the cryptographic key is never exposed to the host system's primary RAM.

---

## 3. Execution Instructions

These simulations are safe, self-contained Python scripts designed to run in a standard Windows environment without modifying your system settings or altering files outside the project directory.

### Prerequisites
Make sure you are running Windows and have Python 3.x installed. The DPAPI simulation (`mitigation_test.py`) requires the `pywin32` library to interface with Windows security APIs.

To install dependencies, open a command prompt or terminal in this workspace and run:
```bash
pip install pywin32
```

### Running the Tests
You can execute each simulation from your terminal:

1. **Test unprivileged database and registry visibility:**
   ```bash
   python unprivileged_access_test.py
   ```

2. **Test legacy vs. DPAPI-protected key storage simulation:**
   ```bash
   python mitigation_test.py
   ```

3. **Test ephemeral lease expiration mechanism:**
   ```bash
   python ephemeral_lease_test.py
   ```

4. **Test RAM memory scraping vulnerability simulation:**
   ```bash
   python memory_scrape_test.py
   ```

### Output Interpretation
* **Success logs (`[SUCCESS]`, `[SUCCESSFUL DEFENSE]`)** indicate that a mitigation performed as expected under the threat model.
* **Vulnerability markers (`[VULNERABILITY CONFIRMED]`, `[ATTACK SUCCESS]`)** identify where legacy client behaviors fail to protect key secrets.

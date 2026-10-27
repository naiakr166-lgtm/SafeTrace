# SafeTrace | أثر الأمان

## Project Overview
SafeTrace is a prototype medical device safety tracking system that uses blockchain technology to maintain a traceable history of medical devices.

The system helps prevent unsafe medical devices from being lent to healthcare and rehabilitation centers.

## Problem Statement
Medical devices may develop faults or require maintenance. Without a clear tracking system, unsafe devices could be reused or lent before their safety is confirmed.

## Proposed Solution
SafeTrace provides a web-based interface for registering medical devices, reporting damage, managing lending requests, approving repairs, and viewing device histories.

## Key Features
- **Device Registration:** Register medical devices with unique IDs.
- **Damage Reporting:** Mark damaged devices as unsafe.
- **Safe Lending:** Prevent unsafe or unavailable devices from being lent.
- **Repair Approval:** Allow authorized technicians to approve repairs.
- **Digital Safety Passport:** View the recorded history of each device.
- **Blockchain Verification:** Verify the integrity of recorded blockchain data.

## Technologies Used
- Python
- Flask
- HTML
- Blockchain concepts
- SHA-256 Hashing
- JSON

## How to Run
1. Download or clone the repository.
2. Install Flask if it is not already installed:

   `pip install flask`

3. Run the application:

   `python3 app.py`

4. Open the following address in your browser:

   `http://127.0.0.1:5001`

## Prototype Scope
SafeTrace is an educational prototype demonstrating blockchain-based device tracking and safety rules. It is not a production-ready medical device management system.

## Project Goal
Improve medical device safety through traceability, transparent maintenance records, and controlled lending decisions.

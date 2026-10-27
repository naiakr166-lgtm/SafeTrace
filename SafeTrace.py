import hashlib
import json
from datetime import datetime, timezone

blockchain = []
devices = {}

authorized_technicians = {"TECH-01", "TECH-02"}

def calculate_hash(data):
    encoded = json.dumps(
        data, sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def add_block(device_id, action, details):
    previous_hash = blockchain[-1]["hash"] if blockchain else "0"

    block = {
        "index": len(blockchain) + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": device_id,
        "action": action,
        "details": details,
        "previous_hash": previous_hash
    }

    block["hash"] = calculate_hash(block)
    blockchain.append(block)

print("SafeTrace Blockchain initialized!")

def register_device(device_id, device_type):
    if device_id in devices:
        print("REJECTED: Device already registered")
        return

    devices[device_id] = {
        "type": device_type,
        "status": "Available"
    }

    add_block(device_id, "Registered", device_type)

    print("SUCCESS: Device registered!")

register_device("WC-208", "Wheelchair")

def report_damage(device_id, issue):
    if device_id not in devices:
        print("REJECTED: Device not found")
        return

    if devices[device_id]["status"] == "Unsafe":
        print("Device is already marked unsafe")
        return

    devices[device_id]["status"] = "Unsafe"

    add_block(device_id, "Damage Reported", issue)

    print("WARNING: Device marked as UNSAFE!")
    print("Reason:", issue)

report_damage("WC-208", "Broken brakes")

def lend_device(device_id, center):
    if device_id not in devices:
        print("REJECTED: Device not found")
        return

    status = devices[device_id]["status"]

    if status == "Unsafe":
        print("REJECTED: Unsafe device cannot be lent!")
        return

    if status != "Available":
        print("REJECTED: Device is not available!")
        return

    devices[device_id]["status"] = "On Loan"

    add_block(device_id, "Device Lent", center)

    print("SUCCESS: Device safely lent to", center)

# Attempt to lend damaged equipment
lend_device("WC-208", "Rehabilitation Center")

def repair_device(device_id, technician_id):
    if device_id not in devices:
        print("REJECTED: Device not found")
        return

    if technician_id not in authorized_technicians:
        print("REJECTED: Unauthorized technician!")
        return

    if devices[device_id]["status"] != "Unsafe":
        print("REJECTED: No active damage report")
        return

    devices[device_id]["status"] = "Available"

    add_block(
        device_id,
        "Repair Approved",
        technician_id
    )

    print("SUCCESS: Repair approved!")
    print("Device is now AVAILABLE")

# Unauthorized technician
repair_device("WC-208", "UNKNOWN")

# Authorized technician
repair_device("WC-208", "TECH-01")

lend_device("WC-208", "Rehabilitation Center")

print("\nCurrent Device Status:")
print(devices["WC-208"])

def verify_blockchain():
    for i, block in enumerate(blockchain):
        saved_hash = block["hash"]
        data = {k: v for k, v in block.items() if k != "hash"}

        if calculate_hash(data) != saved_hash:
            return False

        if i > 0 and block["previous_hash"] != blockchain[i-1]["hash"]:
            return False

    return True

print("Blockchain valid:", verify_blockchain())

print("\nDevice History:")
for block in blockchain:
    print(
        block["index"],
        block["action"],
        "->",
        block["details"]
    )

print("Before tampering:", verify_blockchain())

# Simulate someone changing the recorded damage
blockchain[1]["details"] = "No damage"

print("After tampering:", verify_blockchain())

if not verify_blockchain():
    print("ALERT: Blockchain tampering detected!")
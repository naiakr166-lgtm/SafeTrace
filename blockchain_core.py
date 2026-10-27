import hashlib

import json

from datetime import datetime, timezone

from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "safetrace_data.json"

# SafeTrace Blockchain Storage
blockchain = []
devices = {}

# Authorized maintenance technicians
authorized_technicians = {"TECH-01", "TECH-02"}
def calculate_hash(data):
    encoded = json.dumps(
        data, sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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
    save_data()
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

def verify_blockchain():
    for i, block in enumerate(blockchain):
        saved_hash = block["hash"]
        data = {k: v for k, v in block.items() if k != "hash"}

        if calculate_hash(data) != saved_hash:
            return False

        if i > 0 and block["previous_hash"] != blockchain[i-1]["hash"]:
            return False

    return True

def get_device_history(device_id):
    if not verify_blockchain():
        return []

    history = []

    for block in blockchain:
        if block.get("device_id") == device_id:
            history.append({
                "index": block.get("index"),
                "action": block.get("action"),
                "details": block.get("details"),
                "timestamp": block.get("timestamp"),
                "hash": block.get("hash")
            })

    return history

def save_data():
    data = {
        "blockchain": blockchain,
        "devices": devices
    }

    temp_file = DATA_FILE.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    temp_file.replace(DATA_FILE)

def load_data():
    if not DATA_FILE.exists():
        return

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    saved_chain = data["blockchain"]
    saved_devices = data["devices"]

    if not isinstance(saved_chain, list) or not isinstance(saved_devices, dict):
        raise ValueError("Invalid SafeTrace data format")

    blockchain.clear()
    blockchain.extend(saved_chain)

    devices.clear()
    devices.update(saved_devices)

    if not verify_blockchain():
        raise ValueError("Blockchain integrity check failed")
load_data()
from app.repository.interaction_repository import create_interaction, is_device_busy


def process_interaction(interaction):

    # checking if it's not call to hem self
    if not is_valid_interaction(interaction):
        return

    from_device = interaction["from_device"]
    to_device = interaction["to_device"]
    timestamp = interaction["timestamp"]

    # check for each one of device that they not make another phone call in the same time
    if is_device_busy(from_device, timestamp):
        print(f"Device {from_device} is already in a call at {timestamp}")
        return {"error": f"Device {from_device} is busy at {timestamp}"}

    if is_device_busy(to_device, timestamp):
        print(f"Device {to_device} is already in a call at {timestamp}")
        return {"error": f"Device {to_device} is busy at {timestamp}"}


    return create_interaction(interaction)


def is_valid_interaction(interaction):
    if interaction["from_device"] == interaction["to_device"]:
        print(f"Ignoring interaction: Same device ({interaction['from_device']})")
        return False
    return True
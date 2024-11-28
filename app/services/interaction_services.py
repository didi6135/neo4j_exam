from app.repository.interaction_repository import create_interaction


def process_interaction(interaction):
    if not is_valid_interaction(interaction):
        return
    create_interaction(interaction)


def is_valid_interaction(interaction):
    if interaction["from_device"] == interaction["to_device"]:
        print(f"Ignoring interaction: Same device ({interaction['from_device']})")
        return False
    return True
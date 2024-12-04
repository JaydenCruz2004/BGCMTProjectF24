sites = [
    {"name": "Site A", "devices_needed": 5, "schedule": "9AM-5PM", "proximity_group": 1},
    {"name": "Site B", "devices_needed": 7, "schedule": "10AM-6PM", "proximity_group": 1},
    {"name": "Site C", "devices_needed": 3, "schedule": "8AM-4PM", "proximity_group": 2},
    {"name": "Site D", "devices_needed": 6, "schedule": "11AM-7PM", "proximity_group": 2},
]

total_devices = 15


def generate_logistics_plan(sites, total_devices):
    devices_distributed = 0
    logistics_plan = []

    for site in sites:
        if devices_distributed < total_devices:
            # Check if the devices available can meet the site's needs
            devices_to_allocate = min(site["devices_needed"], total_devices - devices_distributed)
            devices_distributed += devices_to_allocate

            logistics_plan.append(f'{site["name"]} will receive {devices_to_allocate} devices.')

        if devices_distributed >= total_devices:
            break

    return logistics_plan


def print_logistics_plan(plan):
    print("\nLogistics Plan:")
    for entry in plan:
        print(entry)


logistics_plan = generate_logistics_plan(sites, total_devices)
print_logistics_plan(logistics_plan)


def write_to_file(filename, logistics_plan):
    with open(filename, 'w') as f:
        f.write("Logistics Plan:\n")
        for entry in logistics_plan:
            f.write(entry + "\n")


write_to_file('logistics_plan.txt', logistics_plan)
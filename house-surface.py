

    
# Example room sizes
room_sizes0 = {
    "Living Room": 30.0,
    "Kitchen": 15.0,
    "Dining Room": 10.0,
    "Master Bedroom": 20.0,
    "Bedroom 2": 15.0,
    "Bedroom 3": 15.0,
    "Bathroom": 6.0,
    "Ensuite": 7.0,
    "Home Office": 10.0,
    "Laundry": 5.0,
    "Pantry": 4.0,
    "Hallway": 8.0,
}

def optimize_surface(surface, room_sizes):
    room_division = {}

    # Sort the room sizes in descending order
    room_sizes = sorted(room_sizes, reverse=True)

    for room_size in room_sizes:
        if surface >= room_size:
            # Allocate the largest room to the surface
            room_division[room_size] = room_division.get(room_size, 0) + 1
            surface -= room_size

    if surface > 0:
        # Handle the remaining surface, for example, by allocating it as an open area or storage
        room_division["Remaining"] = surface

    return room_division


def optimize_surface_for_clients(client_surfaces, room_sizes):
    room_divisions = []

    for surface in client_surfaces:
        division = optimize_surface(surface, room_sizes)
        room_divisions.append(division)

    return room_divisions

# Example room sizes with float values
room_sizes = [30.0, 15.0, 10.0, 20.0, 15.0, 15.0, 6.0, 7.0, 10.0, 5.0, 4.0, 8.0]

# Example list of client surfaces
client_surfaces = [300]

room_divisions = optimize_surface_for_clients(client_surfaces, room_sizes)

for i, division in enumerate(room_divisions):
    print(f"Client {i + 1} Room Division:")
    for room, size in division.items():
        print(f"{room} ({size}m²)")


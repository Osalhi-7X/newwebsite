import yaml

# Load the YAML data from the file (you can replace this with your actual data loading method)
with open("price_prediction.yaml", "r") as file:
    data = yaml.safe_load(file)

# Function to get prices based on ZIP code
def get_prices(zip_code):
    for entry in data:
        department = entry["department"]
        zip_codes = entry.get("postal_code", [])

        if zip_code in zip_codes:
            price_1 = entry["price_per_sqm"][0]
            price_2 = entry["price_per_sqm"][1]
            return price_1, price_2

    return None, None  # Return None if the ZIP code is not found

# Example usage:
zip_code = "75"  # Replace with the desired ZIP code
price_1, price_2 = get_prices(zip_code)

if price_1 is not None:
    print(f"ZIP Code {zip_code}:")
    print(f"Price 1: {price_1} €/m²")
    print(f"Price 2: {price_2} €/m²")
else:
    print(f"ZIP Code {zip_code} not found.")

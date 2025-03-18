import yaml
import re  # Regular expression module for filtering numeric IDs

def extract_costume_ids(input_file, output_file, iteminfo_file):
    # Read the iteminfo_EN.lua file to get a list of valid IDs
    with open(iteminfo_file, 'r', encoding='utf-8') as file:
        iteminfo_data = file.read()
    
    valid_ids = set()
    # Extract item IDs from the iteminfo file using a regular expression
    for line in iteminfo_data.splitlines():
        # Find any numbers following the 'Id = ' pattern
        match = re.findall(r'\[(\d+)\] = {', iteminfo_data)
        if match:
            valid_ids.add(int(match.group(1)))  # Add the numeric ID
    
    # Read the item_db_equip.yml file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    shop_data = {}

    if 'Body' in data:
        for item in data['Body']:
            # Ensure the item ID is valid
            if 'Id' in item and item['Id'] in valid_ids:
                # Check for costume in AegisName or Name
                if ('AegisName' in item and 'costume' in item['AegisName'].lower()) or \
                   ('Name' in item and 'costume' in item['Name'].lower()):
                    
                    # Determine category based on Locations
                    location = item.get('Locations', {})
                    if location.get('Costume_Head_Top', False):
                        category = "Costumes (Upper)"
                    elif location.get('Costume_Head_Mid', False):
                        category = "Costumes (Middle)"
                    elif location.get('Costume_Head_Low', False):
                        category = "Costumes (Lower)"
                    elif location.get('Costume_Garment', False):
                        category = "Costumes (Garment)"
                    else:
                        category = "Costumes (Other)"
                    
                    # Ensure category is initialized
                    if category not in shop_data:
                        shop_data[category] = []
                    
                    shop_data[category].append(f"{item['Id']}:500000")

    # Write the shops to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        shop_id = 10300  # Base shop ID
        for category, items in shop_data.items():
            chunk_count = 0
            for i in range(0, len(items), 150):  # Split into chunks of 150 items
                chunk = items[i:i+150]
                shop_name = f"{category}{chunk_count if chunk_count > 0 else ''}"
                file.write(f"prontera.gat,172,200,6\tshop\t{shop_name}\t{shop_id},{','.join(chunk)}\n")
                chunk_count += 1
                shop_id += 1  # Increment shop ID

# Example usage
extract_costume_ids('item_db_equip.yml', 'costume_shops.txt', 'iteminfo_EN1.lua')

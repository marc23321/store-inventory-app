import json, os 
from datetime import datetime


user_options= ["1. View All Inventory", 
                "2. Add New Stock", 
                "3. Update Stock", 
                "4. Delete",
                "5. Show Stock Value",
                "6. Quit"]

path = 'store_inventory/data/inventory.json'
recycle_file = 'store_inventory/data/deleted_inventory.json'

def open_inventory_file():
    if not os.path.exists(path):
        print('No Inventory file found')
        return {}
    try:
        with open(path, 'r', encoding="utf-8") as file_object:
            data = json.load(file_object)
            return data
    except json.JSONDecodeError:
        print('Inventory file empty  or not valid file type')
        return {}

def open_deleted_inventory():
    if not os.path.exists(recycle_file):
        print('No Inventory file found')
        return []
    try:
        with open(recycle_file, 'r') as file_object:
           data = json.load(file_object)
           if isinstance(data, list):
               return data
           else:
               return [data]
    except FileNotFoundError:
        print("File not found")
        return []

def add_to_deleted_file(product):
    deleted = open_deleted_inventory()
    deleted_product = product.copy()
    deleted_product["deleted at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deleted.append(deleted_product)

    try:
        with open(recycle_file, 'w', encoding='UTF-8') as file_object:
            json.dump(deleted, file_object, indent = 2)
            file_object.write('\n')
    except FileNotFoundError:
        print("File not found")

def view_inventory():
    data = open_inventory_file()
    print("----------------- INVENTORY -----------------")
    print(f"{'Name':<15} {'Qty':>5} {'Price':>10} {'Value':>10}")
    print("-" * 45)
    
    # for key,value in data.items():
    #     print(value['name'],value['quantity'] , int(value['price']), int(value['price'])*int(value['quantity']))
    total = 0 
    for item in data.values():
        name = item['name']
        quantity = int(item['quantity'])
        price = float(item['price'])
        value = quantity * price
        total += value
        print(f"{name:<15} {quantity:>5} {price:>10.2f} {value:>10.2f}")
    print("-" * 45)
    print(f"{'TOTAL VALUE':<32} {total:>10.2f}")

    greet()

def greet():
    print("\nWhat would you like to do\n" + "\n".join(user_options))

    user_selection = input("Select an option: ")

    if user_selection == '1':
        view_inventory()
    elif user_selection == '2':
        add_stock()
    elif user_selection == '3':
        update_stock()
    elif user_selection == '4':
        delete_stock()
    elif user_selection == '5':
        stock_value()
    elif user_selection == '6':
        print("Nice doing business with you.")
        return
    else:
        print("Invalid Input, Please select from the options below")
        return greet()

def add_stock():
    print('Adding Stock...')
    product_name = input("Please enter product name: ").strip()
    product_qty = int(input(f"Enter quantity of {product_name}: ").strip())
    product_price = float(input(f"Enter price per unit for {product_name}: ").strip())
    
    data = open_inventory_file()
        
    product_sku = f"A{len(data) + 1}"

    data[product_sku]= {
            'sku':product_sku,
            'name': product_name,
            'quantity':product_qty,
            'price':product_price
        }
    
    with open(path, 'w') as file_object:
        try:
            json.dump(data, file_object, indent=4)
            print(f"Added {product_qty} x {product_name} (Product code :{product_sku}) successfully.")
        except json.JSONDecodeError:
            print('Inventory file empty  or not valid file type')
            return
        except FileNotFoundError:
            print("Inventory File not found")
            return
    view_inventory()
    greet()

def update_stock():
    print('Current Stock list...')
    
    data = open_inventory_file()

    print("Product-----------Code--------")
    for item in data.values():
        print(f"{item['name']:<15} {item['sku']:>5}")
        # temp_sku.append(item['sku'])
    
    product_code = input(f"Enter code of product to be updated: ").strip().upper()


    if product_code not in data:
        print("Product does not exist in inventory")
        update_stock()
    else:
        new_qty = int(input(f"Enter new stock number for {data[product_code]['name']}").strip())
        data[product_code]['quantity'] = new_qty
    
    with open(path, 'w') as file_object:
        try:
            json.dump(data, file_object, indent=4)
            print(f"Set {data[product_code]['name']} (SKU {product_code}) to {new_qty}.")
        except FileNotFoundError:
            print("Inventory File not found")
            return
    greet()

def delete_stock():
    print('Current Stock list...')
    
    data = open_inventory_file()

    print(f"{'Product':<20} {'Code':>10}")
    print("-" * 30)
    for item in data.values():
        print(f"{item['name']:<15} {item['sku']:>5}")
        # temp_sku.append(item['sku'])
    
    product_code = input(f"Enter code of product to be deleted: ").strip().upper()
    

    
    if product_code in data:
        name = data[product_code]['name']
        print(f"Deleting {data[product_code]['sku']}-{data[product_code]['name']} from inventory")
       
        
        product = data[product_code]
        data["deleted at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_to_deleted_file(product)
        # deleted_data = open_deleted_inventory()
        # for item in deleted_data.values():
        #     print(f"Deleted: {item}")
        del data[product_code]
        
        with open(path, 'w') as file_object:
            try:
                json.dump(data, file_object, indent=4)
            except FileNotFoundError:
                print("Inventory File not found")
                return
    else :
        print("Product does not exist in inventory")
        add_stock()  

    greet()

def stock_value():
    data = open_inventory_file()
    
    total = 0 
    for item in data.values():
        name = item['name']
        quantity = int(item['quantity'])
        price = float(item['price'])
        value = quantity * price
        total += value
        # print(f"{name:<15} {quantity:>5} {price:>10.2f} {value:>10.2f}")
    print("-" * 45)
    print(f"{'TOTAL STOCK VALUE':<32} {total:>10.2f}")
    print("-" * 45)

    greet()

def deleted_list():
    with open(recycle_file, 'r') as file_object:
        deleted_data = json.load(file_object)
        for item in deleted_data:
            print(item)

    print(deleted_data)

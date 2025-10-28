from inventory_lib import (
    user_options,
    view_inventory,
    add_stock,
    update_stock,
    delete_stock,
    stock_value
)


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

def main():
    greet()

if __name__ == "__main__":
    main()
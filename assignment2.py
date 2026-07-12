import os

FILENAME = "expenses.txt"

def load_expenses():
    expenses = []
    if not os.path.exists(FILENAME):
        return expenses
    
    file = open(FILENAME, "r")
    for line in file:
        line = line.replace("\n", "")
        if line != "":
            parts = line.split(",")
            if len(parts) == 5:
                try:
                    expense = {
                        "id": parts[0],
                        "date": parts[1],
                        "category": parts[2],
                        "description": parts[3],
                        "amount": float(parts[4])
                    }
                    expenses.append(expense)
                except ValueError:
                    continue
    file.close()
    return expenses

def save_expenses(expenses):
    file = open(FILENAME, "w")
    for exp in expenses:
        file.write(exp["id"] + "," + exp["date"] + "," + exp["category"] + "," + exp["description"] + "," + str(exp["amount"]) + "\n")
    file.close()

def display_expense(expense):
    print("Expense ID :" + expense["id"])
    print("Date       :" + expense["date"])
    print("Category   :" + expense["category"])
    print("Description:" + expense["description"])
    print("Amount     :" + str(expense["amount"]))
    print("-" * 40)

def add_expense():
    expense_id = input("Expense ID:")
    
    if expense_id == "":
        print("Expense ID cannot be empty!")
        return
    
    expenses = load_expenses()
    for exp in expenses:
        if exp["id"] == expense_id:
            print("Expense ID already exists!")
            return
    
    date = input("Date (YYYY-MM-DD):")
    category = input("Category:")
    description = input("Description:")
    
    amount_input = input("Amount:")
    try:
        amount = float(amount_input)
        if amount < 0:
            print("Amount cannot be negative!")
            return
    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return
    
    expense = {
        "id": expense_id,
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }
    
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")

def view_expenses():
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print("No expenses found.")
        return
    
    for expense in expenses:
        display_expense(expense)

def search_expense():
    expense_id = input("Enter Expense ID to search:")
    expenses = load_expenses()
    
    for expense in expenses:
        if expense["id"] == expense_id:
            print("")
            print("Expense Found")
            display_expense(expense)
            return
    
    print("Expense not found.")

def update_expense():
    expense_id = input("Enter Expense ID to update:")
    expenses = load_expenses()
    
    for i in range(len(expenses)):
        if expenses[i]["id"] == expense_id:
            print("")
            print("Current expense details:")
            display_expense(expenses[i])
            print("")
            print("Enter new values (press Enter to keep current value):")
            
            new_date = input("Date (" + expenses[i]["date"] + "):")
            new_category = input("Category (" + expenses[i]["category"] + "):")
            new_description = input("Description (" + expenses[i]["description"] + "):")
            new_amount_input = input("Amount (" + str(expenses[i]["amount"]) + "):")
            
            if new_date != "":
                expenses[i]["date"] = new_date
            if new_category != "":
                expenses[i]["category"] = new_category
            if new_description != "":
                expenses[i]["description"] = new_description
            if new_amount_input != "":
                try:
                    new_amount = float(new_amount_input)
                    if new_amount < 0:
                        print("Amount cannot be negative! Update cancelled for amount.")
                    else:
                        expenses[i]["amount"] = new_amount
                except ValueError:
                    print("Invalid amount! Keeping previous value.")
            
            save_expenses(expenses)
            print("")
            print("Expense updated successfully!")
            return
    
    print("Expense not found.")

def delete_expense():
    expense_id = input("Enter Expense ID to delete:")
    expenses = load_expenses()
    
    for i in range(len(expenses)):
        if expenses[i]["id"] == expense_id:
            expenses.pop(i)
            save_expenses(expenses)
            print("Expense deleted successfully!")
            return
    
    print("Expense not found.")

def expense_summary():
    expenses = load_expenses()
    
    if len(expenses) == 0:
        print("No expenses found.")
        return
    
    total_expenses = len(expenses)
    total_spending = 0
    for exp in expenses:
        total_spending = total_spending + exp["amount"]
    
    average_expense = total_spending / total_expenses
    
    highest = expenses[0]["amount"]
    lowest = expenses[0]["amount"]
    for exp in expenses:
        if exp["amount"] > highest:
            highest = exp["amount"]
        if exp["amount"] < lowest:
            lowest = exp["amount"]
    
    print("")
    print("========= Expense Summary =========")
    print("Total Expenses  : " + str(total_expenses))
    print("Total Spending  : " + str(total_spending) + "BDT")
    print("Average Expense : " + str(average_expense) + "BDT")
    print("Highest Expense : " + str(highest) + "BDT")
    print("Lowest Expense  : " + str(lowest) + "BDT")

def main():
    while True:
        print("")
        print("========= Expense Tracker =========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expense")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Expense Summary")
        print("7. Exit")
        
        choice = input("Choose an option:")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_expense()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            expense_summary()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option.")

main()
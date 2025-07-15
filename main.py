import pandas as pd
import matplotlib.pyplot as plt
import os

# File to store financial data
FILE_NAME = "finance_data.csv"
BUDGET_FILE = "budget_data.csv"

# Check if files exist, else create them
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
    df.to_csv(FILE_NAME, index=False)

if not os.path.exists(BUDGET_FILE):
    budget_df = pd.DataFrame(columns=["Category", "Budget"])
    budget_df.to_csv(BUDGET_FILE, index=False)

# Function to add a transaction
def add_transaction():
    date = input("Enter date (YYYY-MM-DD): ")
    t_type = input("Enter type (income/expense): ").lower()
    category = input("Enter category (rent, food, salary, etc.): ")
    amount = float(input("Enter amount: "))

    # Read existing data
    df = pd.read_csv(FILE_NAME)
    
    # Append new data
    new_data = pd.DataFrame({"Date": [date], "Type": [t_type], "Category": [category], "Amount": [amount]})
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save back to CSV
    df.to_csv(FILE_NAME, index=False)
    print("Transaction added successfully!\n")

# Function to view transactions
def view_transactions():
    df = pd.read_csv(FILE_NAME)
    print("\n Transactions:\n")
    print(df)

# Function to generate a spending report
def generate_report():
    df = pd.read_csv(FILE_NAME)
    
    if df.empty:
        print("No transactions found!")
        return
    
    # Filter expenses
    expense_df = df[df["Type"] == "expense"]
    expense_summary = expense_df.groupby("Category")["Amount"].sum()

    # Plot a pie chart of expenses
    plt.figure(figsize=(7, 5))
    expense_summary.plot(kind="pie", autopct="%1.1f%%", startangle=90, colormap="Set2")
    plt.title("Expense Breakdown")
    plt.ylabel("")  # Hide y-label
    plt.show()

# Function to export data
def export_to_csv():
    print(f"Data is already stored in {FILE_NAME}")

# Function to set a budget for a category
def set_budget():
    category = input("Enter category to set budget for (rent, food, etc.): ")
    budget = float(input(f"Enter budget amount for {category}: "))

    # Read existing budget data
    budget_df = pd.read_csv(BUDGET_FILE)
    
    # Check if category already exists
    if category in budget_df["Category"].values:
        budget_df.loc[budget_df["Category"] == category, "Budget"] = budget
    else:
        new_budget = pd.DataFrame({"Category": [category], "Budget": [budget]})
        budget_df = pd.concat([budget_df, new_budget], ignore_index=True)

    # Save budget to CSV
    budget_df.to_csv(BUDGET_FILE, index=False)
    print(f"Budget set for {category}!\n")

# Function to check spending against budget
def check_budget():
    df = pd.read_csv(FILE_NAME)
    budget_df = pd.read_csv(BUDGET_FILE)

    if df.empty or budget_df.empty:
        print("No transactions or budgets found!")
        return

    # Filter expenses
    expense_df = df[df["Type"] == "expense"]
    expense_summary = expense_df.groupby("Category")["Amount"].sum()

    print("\nBudget Tracking:\n")
    for category, spent in expense_summary.items():
        budget = budget_df.loc[budget_df["Category"] == category, "Budget"].sum()
        if budget > 0:
            print(f"🔹 {category}: Spent {spent}, Budget {budget}")
            if spent > budget:
                print(f"Over budget by {spent - budget}!\n")
            else:
                print(f"Within budget. Remaining: {budget - spent}\n")
        else:
            print(f"No budget set for {category}\n")

# Menu system
def menu():
    while True:
        print("\n🔹 Personal Finance Tracker 🔹")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Report")
        print("4. Set Budget")
        print("5. Check Budget Progress")
        print("6. Export Data")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            check_budget()
        elif choice == "6":
            export_to_csv()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Run the application
if __name__ == "__main__":
    menu()

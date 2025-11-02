# -------------------------------
# BANKING MANAGEMENT SYSTEM (DAA Project)
# -------------------------------
import heapq

# -------------------------------
# DATA STRUCTURES
# -------------------------------
accounts = []  # Each account: {'acc_no', 'name', 'balance', 'cibil_score', 'loans'}
transactions = []  # Each transaction: {'acc_no', 'type', 'amount'}

# -------------------------------
# ACCOUNT MANAGEMENT SECTION
# -------------------------------
def add_account(acc_no, name, balance, cibil_score):
    """Add new account"""
    accounts.append({
        'acc_no': acc_no,
        'name': name,
        'balance': balance,
        'cibil_score': cibil_score,
        'loans': []
    })

def view_accounts():
    """Display all accounts"""
    if not accounts:
        print("\nNo accounts found!")
        return
    print(f"\n{'AccNo':<6} {'Name':<15} {'Balance':<10} {'CIBIL':<6}")
    for acc in accounts:
        print(f"{acc['acc_no']:<6} {acc['name']:<15} {acc['balance']:<10.2f} {acc['cibil_score']:<6}")

def linear_search(acc_no):
    """Linear Search for an account"""
    for acc in accounts:
        if acc['acc_no'] == acc_no:
            return acc
    return None

def bubble_sort(key='balance'):
    """Bubble Sort by balance or cibil_score"""
    if not accounts:
        print("No accounts to sort!")
        return

    if key == 'cibil':
        key = 'cibil_score'
    if key not in ['balance', 'cibil_score']:
        print("Invalid sort key!")
        return

    n = len(accounts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if accounts[j][key] < accounts[j + 1][key]:  # Descending
                accounts[j], accounts[j + 1] = accounts[j + 1], accounts[j]
    print(f"Accounts sorted by {key} successfully!")

# -------------------------------
# TRANSACTIONS SECTION
# -------------------------------
def deposit(acc_no, amount):
    acc = linear_search(acc_no)
    if acc:
        acc['balance'] += amount
        transactions.append({'acc_no': acc_no, 'type': 'Deposit', 'amount': amount})
        print(f"₹{amount} deposited successfully!")
    else:
        print("Account not found!")

def withdraw(acc_no, amount):
    acc = linear_search(acc_no)
    if acc:
        if acc['balance'] >= amount:
            acc['balance'] -= amount
            transactions.append({'acc_no': acc_no, 'type': 'Withdraw', 'amount': amount})
            print(f"₹{amount} withdrawn successfully!")
        else:
            print("Insufficient balance!")
    else:
        print("Account not found!")

def view_transactions():
    if not transactions:
        print("\nNo transactions yet!")
        return
    print(f"\n{'AccNo':<6} {'Type':<10} {'Amount':<10}")
    for t in transactions:
        print(f"{t['acc_no']:<6} {t['type']:<10} {t['amount']:<10}")

def sort_transactions():
    """Sort transactions by amount"""
    if not transactions:
        print("No transactions to sort!")
        return

    n = len(transactions)
    for i in range(n):
        for j in range(0, n - i - 1):
            if transactions[j]['amount'] < transactions[j + 1]['amount']:
                transactions[j], transactions[j + 1] = transactions[j + 1], transactions[j]
    print("Transactions sorted by amount successfully!")

# -------------------------------
# LOAN ISSUING SECTION (Greedy)
# -------------------------------
def allocate_loans(total_fund, loan_requests):
    """Greedy approach using max-heap by CIBIL score"""
    heap = []
    for acc_no, req_amount in loan_requests:
        acc = linear_search(acc_no)
        if acc:
            heapq.heappush(heap, (-acc['cibil_score'], acc_no, req_amount))  # Max-heap

    allocated = []
    fund_remaining = total_fund

    while heap and fund_remaining > 0:
        cibil_neg, acc_no, req_amount = heapq.heappop(heap)
        acc = linear_search(acc_no)
        if acc and fund_remaining >= req_amount:
            fund_remaining -= req_amount
            acc['loans'].append(req_amount)
            allocated.append((acc_no, req_amount, -cibil_neg))

    return allocated

# -------------------------------
# PROFIT CALCULATION (Dynamic Programming)
# -------------------------------
def max_profit(loans, profits):
    """DP approach (0/1 Knapsack)"""
    if not loans or not profits:
        return 0
    n = len(loans)
    total = int(sum(loans))
    dp = [0] * (total + 1)

    for i in range(n):
        loan_amt = int(loans[i])
        for j in range(total, loan_amt - 1, -1):
            dp[j] = max(dp[j], dp[j - loan_amt] + profits[i])

    return max(dp)

# -------------------------------
# MAIN MENU
# -------------------------------
def main():
    while True:
        print("\n===== BANKING MANAGEMENT SYSTEM =====")
        print("1. Add Account")
        print("2. View Accounts")
        print("3. Search Account (Linear Search)")
        print("4. Sort Accounts (Balance/CIBIL)")
        print("5. Deposit")
        print("6. Withdraw")
        print("7. View Transactions")
        print("8. Sort Transactions (By Amount)")
        print("9. Loan Allocation (Greedy)")
        print("10. Max Profit (Dynamic Programming)")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            acc_no = int(input("Account Number: "))
            name = input("Name: ")
            bal = float(input("Initial Balance: "))
            cibil = int(input("CIBIL Score: "))
            add_account(acc_no, name, bal, cibil)

        elif choice == '2':
            view_accounts()

        elif choice == '3':
            acc_no = int(input("Enter account number: "))
            acc = linear_search(acc_no)
            print(f"Account Found: {acc}" if acc else "Account not found!")

        elif choice == '4':
            key = input("Sort by (balance/cibil): ").strip().lower()
            bubble_sort(key)
            view_accounts()

        elif choice == '5':
            acc_no = int(input("Account Number: "))
            amt = float(input("Amount: "))
            deposit(acc_no, amt)

        elif choice == '6':
            acc_no = int(input("Account Number: "))
            amt = float(input("Amount: "))
            withdraw(acc_no, amt)

        elif choice == '7':
            view_transactions()

        elif choice == '8':
            sort_transactions()
            view_transactions()

        elif choice == '9':
            total = float(input("Enter total fund available for loans: "))
            num = int(input("Enter number of loan requests: "))
            requests = []
            for _ in range(num):
                acc_no = int(input("Account No: "))
                amt = float(input("Requested Amount: "))
                requests.append((acc_no, amt))
            allocated = allocate_loans(total, requests)
            print("\nAllocated Loans:")
            for acc_no, amt, cibil in allocated:
                print(f"Account {acc_no} | Amount: {amt} | CIBIL: {cibil}")

        elif choice == '10':
            loans = [float(x) for x in input("Enter loan amounts: ").split()]
            profits = [float(x) for x in input("Enter profit values: ").split()]
            print(f"Maximum Profit: {max_profit(loans, profits)}")

        elif choice == '0':
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice!")

# -------------------------------
# DRIVER CODE
# -------------------------------
if __name__ == "__main__":
    main()

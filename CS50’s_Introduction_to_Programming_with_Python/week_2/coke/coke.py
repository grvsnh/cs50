amount_due = 50
inserted = 0

while inserted < amount_due:
    print("Amount Due:", amount_due - inserted)
    coin = int(input("Insert Coin: "))
    if coin in [5, 10, 25]:
        inserted += coin
    else:
        print("Invalid coin. Please insert 5, 10, or 25 cents.")

change = inserted - amount_due
print("Change Owed:", change)

expression = input("Expression: ")
num1, op, num2 = expression.split()

num1 = float(num1)
num2 = float(num2)

if op == "+":
    print(num1 + num2)
elif op == "-":
    print(num1 - num2)
elif op == "*":
    print(num1 * num2)
elif op == "/":
    print(num1 / num2)
else:
    print("Unknown operator")

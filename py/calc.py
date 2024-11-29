num1 = int(input("Enter num1: "))
operator = input("Operator: ")
num2 = int(input("Enter num2: "))

def calc():
    result = 0
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2
    else:
        print("Unknown operator")
        exit()
    
    return result
print(f"{num1} {operator} {num2} = {calc()}")
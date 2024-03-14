def factor(n):
    i=1
    fact = []
    while i <= n:
        if n % i == 0:
            fact.append(i)
        i += 1
    return fact
num = int(input("Enter a number : "))
print("The factors of", num, "are : ", factor(num))
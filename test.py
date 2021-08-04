# 1
def one(year):
    def is_year_leap(year):
        if year % 4 == 0 and year % 100 == 0 and year % 400 == 0:
            return True
        elif year % 4 == 0 and year % 100 == 0 and year % 400 != 0:
            return False
        return False
    return is_year_leap(year)

# 2
def two(a, b, oper):
    def arithmetic(a, b, oper):
        if oper == "-":
            return a - b
        elif oper == "+":
            return a + b
        elif oper == "*":
            return a * b
        elif oper == "/":
            return a / b
        else:
            return "Неизвестная операция"
    return arithmetic(a, b, oper)

# 3
import math
def threee(a):
    def square(a):
        return a * 4, a * a, a * math.sqrt(2)
    return square(a)

# 4
def four(msg, shift):
    def encode(msg, shift):
        res = ""
        for c in msg:
            i = ord(c)
            new_c = chr(i + shift)
            res += new_c
        return res
    return encode(msg, shift)
    
# 5
def five(n):
    def fib(n):
        arr = [0, 1, 1]
        for i in range(3, n+1):
            arr.append(arr[i-2] + arr[i-1])
        if n > 1:
            return arr[n-1]
        else:
            return arr[n]
    return fib(n)

# 6
def six(x):
    def rev_fib(x):
        arr = [0, 1, 1]
        i = 3
        while True:
            arr.append(arr[i-2] + arr[i-1])
            if arr[i] == x:
                return i + 1
            i += 1
    return rev_fib(x)

# 7
def seven(n):
    def fact(n):
        res = 1
        for i in range(2, n+1):
            res *= i
        return res
    return fact(n)

# 8
def eight(x):
    def rev_fact(x):
        res = 1
        i = 2
        while True:
            res *= i
            if res == x:
                return i
            i += 1
        return res
    return rev_fact(x)

# 9
def nine(a, years):
    def bank(a, years):
        for _ in range(years):
            a  *= 1.1
        return round(a, 2)
    return bank(a, years)

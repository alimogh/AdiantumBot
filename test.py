# 1
def one():
    x = int(input())
    def is_simple(x):
        k = 0
        for i in range(2, x // 2+1):
            if (x % i == 0):
                k = k+1
        if (k <= 0):
            return True
        else:
            return False
    print(is_simple(x))

# 2
def two():
    arr1 = input().split()
    arr2 = input().split()

    # Как я понял гарантируется, что массивы одинаковой длины
    for i in range(len(arr1)):
        print(arr1[i], arr2[i])

# 3
def three():
    names = input().split()
    phones = input().split()

    book = {}

    for i in range(len(names)):
        book[names[i]] = phones[i]

    print(book)

# 4
def four():
    name = input()

    book = ['Мавпродош', 'Лорнектиф', 'Древерол', 'Фиригарпиг', 'Клодобродыч']

    if name in book:
        print('Ты – свой. Приветствую, любезный {}!'.format(name))
    else:
        print('Тут ничего нет. Еще есть вопросы?')

# 5
def five():
    russian_alphabet = [chr(i) for i in range(ord('а'),ord('я')+1)]
    for i in range(0, 10):
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('|  {} {}  ||  {} {}  ||  {} {}  |'.format(
            russian_alphabet[i].upper(), russian_alphabet[i],
            russian_alphabet[i+11].upper(), russian_alphabet[i+11], 
            russian_alphabet[i+22].upper(), russian_alphabet[i+22]
        ))
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^')

# 6
def six():
    for i in range(1, 10):
        for j in range(1, 10):
            print('{} x {} = {}'.format(i, j, i*j))

# 7
def seven():
    x = int(input())
    arr = []
    d = 2
    while d*d <= x:
        while (x % d) == 0:
            arr.append(d)
            x //= d
        d += 1
    if x > 1:
       arr.append(x)
    print(arr)

# 8
def eight():
    arr = input()
    x = input()
    print(arr.count(x))

# 9
def nine():
    arr = input().split()

    def sum_of_nums(s):
        sum = 0
        for c in s:
            sum += int(c)
        return sum

    max = 0
    index = 0
    for elem in arr:
        sum = sum_of_nums(elem)
        if sum > max:
            max = sum
            index = arr.index(elem)

    print(arr[index])

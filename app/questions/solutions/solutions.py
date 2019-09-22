import operator

def last10(n):
    return n % 10000000000

def fib(n):
    before = 1
    curr = 1
    n -= 2
    while n > 0:
        tmp = curr
        curr += before
        before = tmp
        n -= 1
    return last10(curr)

def numTrees(n):
    if n <= 1:
        return 1
    tmp = list(range(0, n+1))
    tmp[0] = 1
    for i in range(3, len(tmp)):
        total = 0
        right = i - 1
        left = 0
        while left <= right:
            total += tmp[left] * tmp[right - left]
            left += 1
        tmp[i] = total
    return last10(tmp[-1])

def charsbycount(chars):
    ans = {}
    for char in chars:
        if char not in ans:
            ans[char] = 0
        ans[char] += 1
    sorted_x = sorted(ans.items(), key=operator.itemgetter(1))
    out = [x[0] for x in sorted_x]
    return out 

print("fibonacci: " + str(fib(70000)))
print("bsts: " + str(numTrees(100)))

teststring = "nxmbbzmmailmmanrbjwfarvnzviikhhiabpsjtqrzbrqizirziddmtjwvkavofaggvjmflyhhhqsfirptznvxxbdmrbumrqfibvndimlubrjnzmfrrmngrbahjvrskfxxnnnrdvhvzkiffsxnrdrnirdffmambxehvfttzlbcdifiljrgmimsxhokzsxtlandrfsrmvvaphtwinnbjwifjdsjjgvxbkcyglkkjzflxwzdndjibzljfkwfwufktzjrjnttlupnjnzffavljanxkivcaautclnawcnxxrannslzrzfmzajakbxwvztvikmidgjjyrckisjnrqkivcdzsqxcxjmmjr"

print("Most common: " + charsbycount(teststring)[-1])
print("10 most common: " + ''.join(charsbycount(teststring)[-10:]))


def weirdshift(inp, n):
    strs = 'abcdefghijklmnopqrstuvwxyz'
    def shift(inp):
        chars = []
        for char in inp:
            if char not in ['a', 'e', 'o']:
                chars.append(strs[(strs.index(char) + 1) % 26])
        return ''.join(chars)
    for i in range(0, n):
        inp = shift(inp)
    return inp

print("Weird shift: " + weirdshift("atelnmyvtokdckw", 5))

import math 
def oddeven(n):
    return math.factorial(n / 2) * math.factorial(n / 2)

print("Odd/Even: " + str(oddeven(100))[:10])

def primes(n):
    primes = [2, 3, 5]
    i = 7
    while len(primes) < n:
        isPrime = True
        for p in primes:
            if i % p == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(i)
        i += 2
    return primes

primes = primes(10001)
print("10001 prime: " + str(primes[-1]))

def zfunc(primes):
    sign = 1
    sum = 0
    ind = 0
    while primes[ind] < 10000:
        sum += primes[ind] * sign
        sign *= -1
        ind += 1
    return sum

print("Z Function: " + str(zfunc(primes)))

def digitFact(n):
    x = n
    count = 0
    while x > 0:
        count += math.factorial(x % 10)
        x = x / 10
    return n == count

def countdigitfact():
    count = 0
    for i in range(10, 3628800):
        if digitFact(i):
            count += i
    return count

print("Digit facts: " + str(countdigitfact()))

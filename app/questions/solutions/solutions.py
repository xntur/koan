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
                             

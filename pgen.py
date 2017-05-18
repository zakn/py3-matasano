import random

###########
#Disclaimer: algorithm essentially taken from  https://github.com/bopace/generate-primes
###########

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71]

def has_smallprime(p):
    for x in primes:
        if p % x == 0:
            return True
    return False

def is_prime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = random.randint(1, num - 1)
        if pow(val, num-1, num) != 1:
            return False
    return True

def generate_prime(n):
    found_prime = False
    while not found_prime:
        p = random.randint(2**(n-1), 2**n)
        if is_prime(p, 10) and not has_smallprime(p):
            return p

if __name__ == '__main__':
    print(generate_prime(128))
    print(generate_prime(128))
    print(generate_prime(128))


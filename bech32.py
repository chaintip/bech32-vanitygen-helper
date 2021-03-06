import sys

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def printUsage():
    print("Usage: python " + sys.argv[0] + " (-p) [pattern]")
    print("Options:\n -p\t Print in pipe format")
    print("\t Example: python " + sys.argv[0] + " -p [pattern] | ./vanitygen -f -")

def encode(b):
    """Encode hex string to a base58-encoded string"""
    # Convert hex string to integer
    n = int(b, 16)
    # Divide that integer into bas58
    res = []
    while n > 0:
        n, r = divmod (n, 58)
        res.append(b58_digits[r])
    res = ''.join(res[::-1])

    # Encode leading zeros as base58 zeros
    czero = "00"

    pad = 0
    for i in range(0,len(b),2):
        if b[i:i+2] == czero: pad += 1
        else: break
    return b58_digits[0] * pad + res


bech32_digits = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

pipe = False

if len(sys.argv) < 2:
    printUsage()
    exit(1)

if len(sys.argv) < 3:
    if sys.argv[1] == sys.argv[1] == "-p":
        print("Pattern missing")
        printUsage()
        exit(1)
    elif "-" not in sys.argv[1]:
        addr = sys.argv[1]
    else:
        print("Unknown option '" + sys.argv[1] + "'")
        printUsage()
        exit(1)
else:
    if sys.argv[1] == "-p":
        pipe = True
    else:
        print("Invalid option '" + sys.argv[1] + "'")
        printUsage()
        exit(1)
    addr = sys.argv[2]


if addr[0] != bech32_digits[0]:
    print("First letter must be q")
else:
    if addr[1] not in bech32_digits[:4]:
        print("Second letter must be one of q|p|z|r")
    else:
        allValid = True;
        for letter in addr:
            if letter not in bech32_digits:
                print("All letters must be one of " + ''.join(sorted(bech32_digits)))
                allValid = False
                break
        if allValid:

            if len(addr) > 42:
                print("Address too long")
            else:
                # Good to go
                binaryString = ""
                for letter in addr:
                    binaryString += format(bech32_digits.find(letter),'05b')

                if len(binaryString) % 4 != 0:
                    # If not divisable by four we need to append in binary instead
                    bmin = binaryString + "0"*(200-len(binaryString))
                    bmax = binaryString + "1"*(200-len(binaryString))

                    # To hex string (https://stackoverflow.com/a/2072384)
                    hmin = '%0*X' % ((len(bmin) + 3) // 4, int(bmin, 2))
                    hmax = '%0*X' % ((len(bmax) + 3) // 4, int(bmax, 2))
                else:
                    h = '%0*X' % ((len(binaryString) + 3) // 4, int(binaryString, 2))

                    hmin = h + "0"*(50-len(h))
                    hmax = h + "F"*(50-len(h))

                emin = encode(hmin)
                emax = encode(hmax)

                for i in range(0,len(emin)+1):
                    if emin[i] != emax[i]:
                        idif = i
                        break

                ecut = emin[:idif]

                ind1 = b58_digits.find(emin[idif])
                ind2 = b58_digits.find(emax[idif])
                im = min(ind1,ind2)

                d = abs(ind2-ind1)

                letters = ""
                for i in range(im+1,im+d):
                    letters += b58_digits[i]

                sol = []
                if len(letters) != 0:
                    for letter in letters:
                        sol.append(ecut + letter)
                else:
                    ind1 = b58_digits.find(emin[idif+1])
                    ind2 = b58_digits.find(emax[idif+1])

                    for i in range(ind1+1,len(b58_digits)):
                        sol.append(ecut + emin[idif] + b58_digits[i])

                    for i in range(0,ind2):
                        sol.append(ecut + emax[idif] + b58_digits[i])

                if not pipe:
                    print("Have vanitygen search for:")
                    for s in sol:
                        print s,
                else:
                    for s in sol:
                        print(s)

from part21 import myMT

def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

class splicedMT:

    def __init__(self, stolen_index):
        self.index = 0
        self.mt = stolen_index
        
    def rand(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]

        # Right shift by 11 bits
        y = y ^ y >> 11
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ y << 7 & 2636928640
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        # Right shift by 18 bits
        y = y ^ y >> 18

        self.index = self.index + 1

        return _int32(y)


def untemper(rand_out):
    z = rand_out
    #revert step 1
    z = z ^ z >> 18
    
    #revert step 2
    z = z ^ z << 15 & 4022730752
    
    #revert step 3
    current = z & 0b1111111
    new = current
    for i in range(1, 4):
        current = current & (2636928640>>(7*i) & 0b1111111)
        nextblock = z>>(7*i) & 0b1111111
        current = current ^ nextblock
        new = (current<<(7*i)) ^ new
    current = current & 0b1111
    current = current & (2636928640>>(7*4) & 0b1111)
    nextblock = z>>(7*4) & 0b1111
    current = current ^ nextblock
    new = (current<<(7*4)) ^ new
    z = new

    #revert step 4
    new = 0b0
    current = 0b0
    for k in range((len(bin(z))-2)//11):
        newblock = z>>(len(bin(z))-2-(11*(k+1))) & 0b11111111111
        current = current ^ newblock
        new = (new<<(11*k)) ^ current
    new = new >> ((11*k + 24) - len(bin(z)))
    newblock = z & 0b11111111111
    current = (new & 0b11111111111)^ newblock
    new = (new<<(11)) ^ current
    return new


if __name__ == '__main__':

    x = myMT(1398397777)
    random_outs = []
    splice_internal = []
    
    for h in range(624):
        random_outs.append(x.rand())
        splice_internal.append(untemper(random_outs[h]))

        #error check
        if (splice_internal[h] != x.mt[h]):
            print([y, z, x.mt[h], h])

    spliced = splicedMT(splice_internal)

    for j in range(len(random_outs)):
        z = spliced.rand()
        if (z != random_outs[j]):
            print([z, random_outs[j], j])
    
    

    
    

    
    

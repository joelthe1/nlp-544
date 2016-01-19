import sys

if len(sys.argv) < 2:
    print "Input file now specified."
    exit()

def tost(i):
    result = []
    while i:
        result.append(chr(i&0xFF))
        i >>= 8
    result.reverse()
    return ''.join(result)

wfile = open('utf8encoder_out.txt', 'wb')

with open(sys.argv[1], 'rb') as f:
    while True:
        utf16_byte = f.read(2)
        if not utf16_byte:
            break
        b1 = ord(utf16_byte[0])
        b2 = ord(utf16_byte[1])
        if b1 == 0xfe and b2 == 0xff:
            print 'it is BOM'
            continue
        
        if b1 == 0x00:
            wfile.write(tost(b2))
        elif b1 < 0x08:
            b2_rem = b2 & 0xc0 #0xc0=11000000
            b2_rem >>= 6
            b2 = b2 & 0x3f #0x3f=00111111
            b2 = b2 | 0x80 #0x80=10000000
            b1_rem = b1 << 2
            b1_rem = b1_rem | b2_rem
            b1 = 0x1f & b1_rem #0x1f=00011111
            b1 = b1 | 0xc0
            wfile.write(tost(b1))
            wfile.write(tost(b2))
        else:
            b1_rem1 = b1 & 0xf0 #0xf0=11110000
            b1_rem1 >>= 4
            b1_rem2 = b1 & 0x0f #0x0f=00001111
            b1_rem2 <<= 2
            utf8_b1 = b1_rem1 | 0xe0 #0xe0=11100000

            b2_rem1 = b2 & 0xc0 #0xc0=11000000
            b2_rem1 >>= 6
            utf8_b2 = b1_rem2 | b2_rem1
            utf8_b2 = utf8_b2 | 0x80 #0x80=10000000

            b2_rem2 = b2 & 0x3f #0x3f=00111111
            utf8_b3 = b2_rem2 | 0x80 #0x80=10000000
            wfile.write(tost(utf8_b1))
            wfile.write(tost(utf8_b2))
            wfile.write(tost(utf8_b3))

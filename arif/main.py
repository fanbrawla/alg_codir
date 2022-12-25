global write_bit
global bit_len
write_bit = 0

global read_bit
global garbage_bit
read_bit = 0
garbage_bit = 0

def indexForSymbol(sin, irgum):
    j = 0
    for i in sin:
        if irgum == i:
            return j + 2
        j += 1

def outPutBit(bit, outputfile):
    global write_bit
    global bit_len
    write_bit >>= 1
    if bit & 1:
        write_bit |= 0x80
    bit_len -= 1
    if bit_len == 0:
        bit_len = 8
        outputfile.write(write_bit.to_bytes(1, "little"))


def bitPlusFollow(bit, bittofollow, outputfile):
    outPutBit(bit, outputfile)
    for _ in range(bittofollow):
        outPutBit(~bit, outputfile)

def compress(fname):
    global write_bit
    global bit_len
    bit_len = 8
    with open(f'{fname}', 'r') as fp:
        sum_wlist = 0
        chunk = fp.read(1)
        wlist = {}
        while chunk:
            sum_wlist += 1
            if wlist.get(chunk) == None:
                wlist.update({chunk: 1})
            else:
                wlist[chunk] = wlist[chunk] + 1
            chunk = fp.read(1)

    sorted_wlist = dict(sorted(wlist.items(), key=lambda item: item[1], reverse=True)) 
    wlist_mas = [0, 1]
    for i in sorted_wlist:
        wlist_mas.append(sorted_wlist[i] + wlist_mas[-1])

    f = open(f"{fname}.compressed", "wb+")
    f.write(len(sorted_wlist).to_bytes(1, "little"))
    for i in sorted_wlist:
        f.write(i.encode("ascii"))
        f.write(sorted_wlist[i].to_bytes(4, "little"))
    
    with open(f'{fname}', 'r') as fp:
        low_v = 0
        high_v = (1<<16)-1 
        delete = wlist_mas[-1]
        diff = high_v - low_v + 1
        first_q = int(int(high_v + 1) / 4)
        half_q = first_q * 2
        third_q = first_q * 3
        bit_to_follow = 0

        chip = fp.read(1)
        while chip:
            j = indexForSymbol(sorted_wlist, chip)
            high_v = int(low_v + wlist_mas[j] * diff / delete - 1)
            low_v = int(low_v + wlist_mas[j - 1] * diff / delete)

            while True:
                if high_v < half_q:
                    bitPlusFollow(0, bit_to_follow, f)
                    bit_to_follow=0
                elif low_v >= half_q:
                    bitPlusFollow(1, bit_to_follow, f)
                    bit_to_follow=0
                    low_v -= half_q
                    high_v -= half_q
                elif low_v >= first_q and high_v < third_q:
                    bit_to_follow += 1
                    low_v -= first_q
                    high_v -= first_q
                else:
                    break
                low_v += low_v
                high_v += high_v + 1

            diff = high_v - low_v + 1
            chip = fp.read(1)

        high_v = int(low_v + wlist_mas[1] * diff / delete - 1)
        low_v = int(low_v + wlist_mas[0] * diff / delete)

        while True:
            if high_v < half_q:
                bitPlusFollow(0, bit_to_follow, f)
                bit_to_follow=0
            elif low_v >= half_q:
                bitPlusFollow(1, bit_to_follow, f)
                bit_to_follow=0
                low_v -= half_q
                high_v -= half_q
            elif low_v >= first_q and high_v < third_q:
                bit_to_follow += 1
                low_v -= first_q
                high_v -= first_q
            else:
                break
            low_v += low_v
            high_v += high_v + 1
        bit_to_follow += 1
        if low_v < first_q:
            bitPlusFollow(0, bit_to_follow, f)
            bit_to_follow=0
        else:
            bitPlusFollow(1, bit_to_follow, f)
            bit_to_follow=0
        write_bit >>= bit_len
        f.write(write_bit.to_bytes(1, "little"))
    f.close()

def inPutBit(input_file): 
    global read_bit
    global bit_len
    global garbage_bit
    if bit_len == 0:
        sid_bit = input_file.read(1)
        read_bit = int.from_bytes(sid_bit, "little")
        if sid_bit == b"":
            garbage_bit += 1
            read_bit = 255
        bit_len = 8

    t = read_bit & 1
    read_bit >>= 1
    bit_len -= 1
    return t

def decompress(fname):
    global bit_len
    bit_len = 0
    with open(f"{fname}", "rb") as file_in:
        chunk = ord(file_in.read(1))
        rasp_wlist = {}
        for i in range(chunk):
            key_hat = file_in.read(1).decode('ascii')
            val_hat = int.from_bytes(file_in.read(4), "little")
            rasp_wlist[key_hat] = val_hat
        wlist_mas = [0, 1]
        for i in rasp_wlist:
            wlist_mas.append(rasp_wlist[i] + wlist_mas[-1])
            
        if "compressed" in fname:
            fname = fname[:-10]+"decompressed"
            
        with open(f"{fname}", "wb+") as file_out:
            low_v = 0
            high_v = (1 << 16) - 1  
            delete = wlist_mas[-1]
            diff = high_v - low_v + 1
            first_q = int(int(high_v + 1) / 4)
            half_q = first_q * 2
            third_q = first_q * 3
            val = 0

            for i in range(16):
                k = inPutBit(file_in)
                val += val + k
            while True:
                freq = int(((val - low_v + 1) * delete - 1) / diff)
                j = 1
                while wlist_mas[j] <= freq:
                    j += 1
                high_v = int(low_v + wlist_mas[j] * diff / delete - 1)
                low_v = int(low_v + wlist_mas[j - 1] * diff / delete)

                while True:
                    if high_v < half_q:
                        pass
                    elif low_v >= half_q:
                        low_v -= half_q
                        high_v -= half_q
                        val -= half_q
                    elif low_v >= first_q and high_v < third_q:
                        low_v -= first_q
                        high_v -= first_q
                        val -= first_q
                    else:
                        break
                    low_v += low_v
                    high_v += high_v + 1
                    k = inPutBit(file_in)
                    val += val + k
                if j == 1:
                    break
                file_out.write(list(rasp_wlist.keys())[j - 2].encode('ascii'))
                diff = high_v - low_v + 1


def main():
    choise = input("1 - сжать, 2 - расжать:\n")
    fname = input("Введите название файла ")
    if choise == "1":
        compress(fname)
    elif choise == "2":
        decompress(fname)
    else:
        print("Неправильный ввод")

if __name__ == "__main__":
    	main()

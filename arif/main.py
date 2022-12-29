def get_index(word, wlist):
    index = 0
    for i in wlist:
        if word == i:
            return index
        index+=1

def get_code(up, down):
    if up == down:
        code_txt = str(up)
        return code_txt[2:]
    s_up = str(up)
    s_down = str(down)
    code_txt = ""
    i = 0
    while(i < len(s_up)):
        if s_up[i] != s_down[i]:
            if (int(s_up[i])-1) > int(s_down[i]):
                code_txt += str(int(s_up[i])-1)
                i = len(s_up)
        else:
            code_txt += s_up[i]
        i+=1
    return code_txt[2:]
    

def compress():
    file_name = input("Введите название файла: ")
    with open(f"{file_name}", "r") as plain_file:
        wlist = {}
        for string in plain_file:
            for word in string:
                if wlist.get(word) == None:
                    wlist.update({word:1})
                else:
                    wlist[word] += 1
        amout_word = 0
        for i in wlist:
            amout_word += wlist[i]
        probability = []
        for i in wlist:
            probability.append(wlist[i]/amout_word)
        plain_file.close()

    with open(f"{file_name}", "r") as plain_file:
        up = 1.0
        down = 0.0
        txt = ""
        for string in plain_file:
            txt+=string
        for word in txt:
            diff = up - down
            index = get_index(word, wlist)
            for i in range(index):
                down = down + diff * probability[i]
            up = down + diff * probability[index]
        code_txt = get_code(up, down)
        plain_file.close()
    with open(f"{file_name}.compressed", "wb") as com_file:
        length = len(wlist)
        com_file.write(length.to_bytes(2, "little"))
        for word in wlist:
            com_file.write(word.encode())
            com_file.write(wlist[word].to_bytes(2, "little"))
        com_file.write(code_txt.encode())

def decompress():
    file_name = input("Введите название файла: ")
    with open(f"{file_name}", "rb") as com_file:
        length = int.from_bytes(com_file.read(2), "little")
        wlist = {}
        for i in range(length):
            word = com_file.read(1).decode()
            amount = int.from_bytes(com_file.read(2), "little")
            wlist.update({word:amount})
        amount_word = 0
        for word in wlist:
            amount_word += wlist[word]
        probability = []
        for word in wlist:
            probability.append(wlist[word]/amount_word)
        com_txt = "0."+com_file.read().decode()
        com_txt = float(com_txt)
        txt_len = 0
        p_txt = ""
        word_list = list(wlist.keys())
        up = 1.0
        down = 0.0
        while(txt_len < amount_word):
            diff = up - down
            for i in range(len(wlist)):
                up = down + diff*probability[i]
                if down < com_txt < up:
                    break
                else:
                    down = up
            
            txt_len += 1
            p_txt += word_list[i]

        com_file.close()
    with open (f"{file_name}.decompress", "w") as dec_file:
        dec_file.write(p_txt)
        dec_file.close()


def main():
    choise = input("Выберите режим: 1 - сжать, 2 - расжать\n")
    if choise == "1":
        compress()
    elif choise == "2":
        decompress()
    else:
        print("Неправильный ввод!!!")


if __name__ == "__main__":
    main()

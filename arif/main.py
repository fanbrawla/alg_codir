def get_index(word, wlist):
    index = 0
    for i in wlist:
        if word == i:
            return index
        index+=1

def get_code(up, down):
    if up == down:
        code_txt = str(up)
        return int(code_txt[2:])
    s_up = str(up)
    s_down = str(down)
    code_txt = ""

    for i in range(len(up)):
        if s_up[i] != s_down[i]:
            code_txt += str(int(s_up[i])+int(s_down[i])//2)
        else:
            code_txt += s_up[i]
    return int(code_txt[2:])
    

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
        for word in wlist:
            com_file.write(word.encode())
            com_file.write(wlist[word].to_bytes(2, "little"))
        com_file.write(b"\n")
        com_file.write(code_txt.to_bytes((code_txt.bit_length()+7)//8, "little"))


def decompress():
    file_name = input("Введите название файла: ")

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

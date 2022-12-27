def compress():
    file_name = input("Введите название файла: ")
    with open(f"{file_name}", "r") as fp:
        wlist = {}
        for string in fp:
            for word in string:
                if wlist.get(word) == None:
                    wlist.update({word:1})
                else:
                    wlist[word] += 1
        amout_word = 0
        for i in wlist:
            amout_word += wlist[i]
        probability = {}
        for i in wlist:
            probability.update({i:wlist[i]/amout_word})
        print(probability)


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

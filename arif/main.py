def main():
    sum_slovar = 0
    f = input("Введите название файла для кодирования:")
    with open(f'{f}', 'r') as fp:
        test_sum = 0
        chunk = fp.read(1)
        slovar = {}
        while chunk:
            test_sum += 1
            if slovar.get(chunk) == None:
                slovar.update({chunk: 1})
            else:
                slovar[chunk] = slovar[chunk] + 1
            chunk = fp.read(1)

if __name__ == "__main__":
    	main()

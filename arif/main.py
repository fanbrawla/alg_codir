def main():
    f = input("Введите название файла для кодирования:")
    with open(f'{f}', 'r') as fp:
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

    f = open(f"{f}.enc", "wb+")
    print(len(sorted_wlist))
    f.write(len(sorted_wlist).to_bytes(1, "little"))
    for i in sorted_wlist:
        f.write(i.encode("ascii"))
        f.write(sorted_wlist[i].to_bytes(4, "little"))
    print(sorted_wlist)

if __name__ == "__main__":
    	main()

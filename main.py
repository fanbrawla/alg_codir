def sort(count):
    for i in range(len(count)-1):
        for j in range(len(count)-1):
            if count[j][1] < count[j+1][1]:
                temp = count[j+1]
                count[j+1] = count[j]
                count[j] = temp
    return count

def ini():
    file = open("text.txt", "r")
    number = [0] * 256
    for i in range(256):
        number[i] = [chr(i), 0]
    f = file.read()
    for i in f:
        number[ord(i)][1] += 1
    j = 0
    count = []
    for i in range(0, 256):
        if number[i][1] != 0:
            count.append(number[i])
    sort(count)
    return(count)

def main():
    count = ini()
    sort(count)
    print(count)

if __name__ == "__main__":
    	main()
     
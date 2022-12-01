class tree:
    def __init__(self, data = 0, name = None):
        self.name = name
        self.left = None
        self.right = None
        self.data = data
        self.code = None
        self.potomok = None

    def add(self, tr):
        new = tree()
        new.left = self
        new.right = tr
        return new

    def PrintTree(self):
        if self.code is None:
            print(self.data, self.name, self.code, self.potomok)
        else:
            print(self.data, self.name, self.code, self.potomok)
        if self.left:
            self.left.PrintTree()
        if self.right:
            self.right.PrintTree()

    def Cost(self, cost = 0):
        cost += self.data
        if self.left:
            cost = self.left.Cost(cost)
        if self.right:
            cost = self.right.Cost(cost)
        return cost
    
    def Num(self, code = 1, potomok = 1):
        self.code = bin(code).replace("0b", "").zfill(potomok)
        self.potomok = potomok
        potomok += 1
        if self.left:
            code0 = code << 1
            self.left.Num(code0, potomok)
        if self.right:
            code1 = (code << 1) | 1
            self.right.Num(code1, potomok)

    def find(self, char, code = None):
        if char == self.name:
            code = self.code
        if code is None:
            if (self.left):
                code = self.left.find(char)
        if code is None:
            if (self.right):
                code = self.right.find(char)
        return code

    def encode(self, massiv):
        filep = open("text.txt", "r")
        plain = filep.read()
        plain = list(plain)
        del plain[len(plain)-1]
        for i in range(len(plain)):
            code = self.find(plain[i])
            plain[i] = code
        plain = ''.join(plain)
        n = len(plain)
        num_pad = (8-n)%8
        pad = "0"*num_pad
        plain = pad+plain
        filect = open("encoded", "wb")
        stroka = ""
        for i in range(len(massiv)):
            for j in range(2):
                stroka += str(massiv[i][j])
                stroka += "-!"
        stroka += str(len(plain)) + "-!"
        stroka += str(num_pad)
        stroka += " \n"
        stroka = bytes(stroka, 'utf-8')
        filect.write(stroka)
        for i in range(int(len(plain)/8)):
            a = plain[i*8:i*8+8]
            vec = int(a[0])
            a = a[1:]
            for j in a:
                if j == '0':
                    vec = vec << 1
                if j == '1':
                    vec = (vec << 1) | 1 
            filect.write((vec).to_bytes(1, byteorder = 'little'))
                


def ini():
    file = open("text.txt", "r")
    number = [0] * 256
    for i in range(256):
        number[i] = [chr(i), 0]
    f = file.read()
    for i in f:
        number[ord(i)][1] += 1
    j = 0
    number[ord("\n")][1]-=1
    count = []
    for i in range(0, 256):
        if number[i][1] != 0:
            count.append(number[i])
    return(count)

def MasToTree(count):
    tr = []
    haftr = []
    for i in range(len(count)):
        a = tree(count[i][1], count[i][0])
        tr.append(a)
    while len(tr) > 1:
        cost = tr[0].Cost()
        l = 0
        for j in range(len(tr)):
            if (cost > tr[j].Cost()):
                l = j
        r = 0
        if l == 0:
            r = 1
        cost1 = tr[r].Cost()
        for k in range(len(tr)):
            if ((k!=l) & (cost1 > tr[k].Cost())):
                r = k
        a = tr[l].add(tr[r])
        tr.append(a) 
        if r > l:
            del tr[r]
            del tr[l]
        else:
            del tr[l]
            del tr[r]
    return tr

def decode(f):
    filenc = open(f"{f}", "rb")
    massiv = []
    string = b""
    sim = filenc.read(1)
    while sim != b" \n":
        string+=sim
        if sim in b" \n":
            tmp =filenc.read(1)
            string += tmp
            sim += tmp
        if sim not in b" \n":
            sim = filenc.read(1)
    string = string.decode()
    string = string.replace(" \n", "")
    string = string.split("-!")
    num_pad = int(string[-1])
    string = string[:-1]
    lenght = int(string[-1])
    string = string[:-1]
    massiv = []
    for i in range(0, len(string)-1, 2):
        podmas = []
        podmas.append(string[i])
        podmas.append(int(string[i+1]))
        massiv.append(podmas)
    tre = MasToTree(massiv)
    tre = tre[0]
    tre.left.Num(0)
    tre.right.Num(1)
    codes = []
    for i in range(len(massiv)):
        tmp = []
        tmp.append(massiv[i][0])
        tmp.append(tre.find(massiv[i][0]))
        codes.append(tmp)
    encoded_text = filenc.read()
    encoded_text = bin(int(encoded_text.hex(), 16))[2:]
    encoded_text = encoded_text.zfill(lenght)
    encoded_text = encoded_text[num_pad:]
    plain_text = ""
    while encoded_text != "":
        for i in codes:
            if i[1] == encoded_text[:len(i[1])]:
                encoded_text = encoded_text[len(i[1]):]
                plain_text += i[0]
    filept = open("decoded", "w")
    filept.write(plain_text+"\n")

def main():
    count = ini()
    tre = MasToTree(count)
    tre = tre[0]
    tre.left.Num(0)
    tre.right.Num(1)
    tre.encode(count)
    f = "encoded"
    decode(f)

if __name__ == "__main__":
    	main()
     

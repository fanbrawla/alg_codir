class tree:
    def __init__(self, data = 0, name = None):
        self.name = name
        self.left = None
        self.right = None
        self.data = data
        self.code = None
        self.child = None

    def add(self, tr):
        new = tree()
        new.left = self
        new.right = tr
        return new

    def PrintTree(self):
        if self.code is None:
            print(self.data, self.name, self.code, self.child)
        else:
            print(self.data, self.name, self.code, self.child)
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
    
    def Num(self, code = 1, child = 1):
        self.code = bin(code).replace("0b", "").zfill(child)
        self.child = child
        child += 1
        if self.left:
            code0 = code << 1
            self.left.Num(code0, child)
        if self.right:
            code1 = (code << 1) | 1
            self.right.Num(code1, child)

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

    def encode(self, massiv, name):
        filep = open(f"{name}", "rb")
        plain = filep.read()
        plain = list(plain)
        for i in range(len(plain)):
            code = self.find(chr(plain[i]))
            plain[i] = code
        plain = ''.join(plain)
        n = len(plain)
        num_pad = (8-n)%8
        pad = "0"*num_pad
        plain = pad+plain
        filect = open(f"{name}_encoded", "wb")
        string = b""
        filect.write(len(massiv).to_bytes(1, byteorder = "little"))
        for i in range(len(massiv)):
            string += ord(massiv[i][0]).to_bytes(1, byteorder = "little")
            string += massiv[i][1].to_bytes(2, byteorder = "little")
        string += num_pad.to_bytes(1, byteorder = "little")
        filect.write(string)
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
        filect.close()
                
def counter(name):
    file = open(f"{name}", "rb")
    number = [0] * 256
    for i in range(256):
        number[i] = [chr(i), 0]
    f = file.read()
    for i in f:
        number[i][1] += 1
    number[ord("\n")][1]-=1
    count = []
    for i in range(0, 256):
        if number[i][1] != 0:
            count.append(number[i])
    return(count)

def MasToTree(count):
    tr = []
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

def decode(name):
    filenc = open(f"{name}", "rb")
    massiv = []
    len_mas = filenc.read(1)
    len_mas = int.from_bytes(len_mas, byteorder = "little")
    for i in range(len_mas):
        subarray = []
        word = filenc.read(1)
        amount = filenc.read(2)
        amount = int.from_bytes(amount, byteorder= "little")
        subarray.append(word)
        subarray.append(amount)
        massiv.append(subarray)
    tre = MasToTree(massiv)
    tre = tre[0]
    tre.left.Num(0)
    tre.right.Num(1)
    num_pad = filenc.read(1)
    num_pad = int.from_bytes(num_pad, byteorder= "little")
    codes = []
    for i in range(len_mas):
        tmp = []
        tmp.append(massiv[i][0])
        tmp.append(tre.find(massiv[i][0]))
        codes.append(tmp)
    encoded_text = filenc.read()
    encoded_text = bin(int(encoded_text.hex(), 16))[2:]
    encoded_text = (-(len(encoded_text))%8)*"0"+encoded_text
    encoded_text = encoded_text[num_pad:]
    plain_text = []
    while encoded_text != "":
        for i in codes:
            if i[1] == encoded_text[:len(i[1])]:
                encoded_text = encoded_text[len(i[1]):]
                plain_text.append(ord(i[0]))
    filept = open(f"{name}_decoded", "wb")
    for i in plain_text:
        filept.write(i.to_bytes(1, byteorder="little"))
    filept.close()

def start(choise):
    name = input("Введите название файла\n")
    if choise == "1":
        count = counter(name)
        tre = MasToTree(count)
        tre = tre[0]
        tre.left.Num(0)
        tre.right.Num(1)
        tre.encode(count, name)
    if choise == "2":
        decode(name)

def main():
    choise = input("Выберите режим:\n1)Кодировка\n2)Раскодировка\n")
    start(choise)

if __name__ == "__main__":
    	main()
     

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
            #self.code = bin(self.code).replace("0b", "").zfill(self.potomok)
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

    def encode(self):
        filep = open("text.txt", "r")
        plain = filep.read()
        code = []
        for i in plain[:-1]:
            code.append(self.find(i))
        print(code)


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

def main():
    count = ini()
    print(count)
    tre = MasToTree(count)
    print(f"len = {len(tre)}")
    tre = tre[0]
    tre.left.Num(0)
    tre.right.Num(1)
    tre.encode()
    tre.PrintTree()
    

if __name__ == "__main__":
    	main()
     

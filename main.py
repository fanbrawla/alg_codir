class tree:
    def __init__(self, data = 0, name = None):
        self.name = name
        self.left = None
        self.right = None
        self.data = data
        self.num = None

    def add(self, tr):
        new = tree()
        new.left = self
        new.right = tr
        return new

    def PrintTree(self):
        print(self.data, self.name, self.num)
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
    
    def Num(self, num = ""):
        self.num = num
        if self.left:
            #num0 = (num << 1)
            num0 = num+"0"
            self.left.Num(num0)
        if self.right:
            #num1 = (num << 1) | 1 
            num1 = num+"1"
            self.right.Num(num1)


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
    tre.Num()
    tre.PrintTree()
    

if __name__ == "__main__":
    	main()
     

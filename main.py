class tree:
    def __init__(self, data = None, name = None):
        self.name = name
        self.left = None
        self.right = None
        self.data = data
    
    def add(self, tr):
        new = tree()
        new.left = self
        new.right = tr
        return new

    def PrintTree(self):
        print(self.data)
        if self.left:
            self.left.PrintTree()
        if self.right:
            self.right.PrintTree()


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
    haf = tree(count[len(count)-1][1], count[len(count)-1][0])
    tr = tree(2, "r")
    a = haf.add(tr)
    a.PrintTree()


if __name__ == "__main__":
    	main()
     

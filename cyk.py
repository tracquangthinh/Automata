class CYK:
    def __init__(self, path):
        self.transitions= dict()
        self.table = []
        self.load_data(path)

    def load_data(self, path):
        with open(path) as file:
            for line in file:
                objlines = line.strip().split(" -> ")
                non_terminal = objlines[0]
                self.transitions[non_terminal] = objlines[1].split("|")
                
    def print(self):
        for i in range(len(self.table)):
            for j in range(len(self.table) - i - 1):
                print(self.table[i][j], '\t', end='')
            print("\n")
                
    def get_non_terminal(self, symbol):
        result = [s for s in self.transitions.keys() if symbol in
                self.transitions[s]]
        return result
    
    def plus(self, symbol_arr_1, symbol_arr_2):
        result = set()
        for s1 in symbol_arr_1:
            for s2 in symbol_arr_2:
                r =self.get_non_terminal(s1 + s2)
                if len(r) > 0:
                    for r_ in r:
                        result.add(r_)
        return list(result)
                
    def decide(self, input):
        for i in range(len(input)):
            self.table.append([])
            for j in range(len(input)):
                self.table[i].append([])

        for i in range(len(input)):
            if i == 0:
                for j in range(len(input)):
                    self.table[i][j] = self.get_non_terminal(input[j])
            else:
                for j in range(len(input)-i):
                    result = set()
                    for k in range(i):
                        if len(self.table[k][j]) > 0 and len(self.table[i-1-k][j+k+1]) > 0:
                            r = self.plus(self.table[k][j], self.table[i-1-k][j+k+1])
                            for r_ in r:
                                result.add(r_)
                    self.table[i][j] = list(result)

        if len(self.table[-1][0]) > 0:
            return True
        return False

cyk = CYK("./test/cyk")
word = input("Please type your word: ")

print("CFG: ")
with open("./test/cyk") as file:
    for line in file:
        print(line.strip())
print("\n=================\n")
print(word, "belongs to L(G): ", cyk.decide('aabbb'), "\n")
cyk.print()

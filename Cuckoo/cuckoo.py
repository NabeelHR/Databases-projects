from __future__ import print_function
#import hashlib
class Cuckoo:
    '''
    docstring
    '''
    def __init__(self):
        self.n = 11         #this variable will store the table size
        self.table1 = [None] * self.n
        self.table2 = [None] * self.n
        self.scalar = 1
    def search(self, key):
        h_val = self.hash1(key)
        if self.table1[h_val] == key:
            print(key, " is present in table 1 at index ", h_val)
        else:
            h_val = self.hash2(key)
            if self.table2[h_val] == key:
                print(key, " is present in table 2 at index ", h_val)
            else:
                print ("BUG: Key is loststtsds")

    def insert(self, key):
        if key%2 == 0: #try inserting in table 1
            h_val = self.hash1(key)
            if self.table1[h_val] is None:
                self.table1[h_val] = key
            else:
                h_val = self.hash2(key)
                if self.table2[h_val] is None:
                    self.table2[h_val] = key
                else:
                    self.evict(key, 1)
        else:#odd numbers go to table 2 first
            h_val = self.hash2(key)
            if self.table2[h_val] is None:
                self.table2[h_val] = key
            else:
                h_val = self.hash1(key)
                if self.table1[h_val] is None:
                    self.table1[h_val] = key
                else:
                    self.evict(key, 1)

    def evict(self, key, i):
        print("evicting @", i)
        if i > 2:
            self.scalar += 1
            self.n *= 2
            self.rearrange()
            self.insert(key)
        else:
            h_val = self.hash1(key)
            evictee = self.table1[h_val]
            if evictee is None:
                print("BROOO wtf @", key)
                self.print_tables()
            self.table1[h_val] = key
            h_val = self.hash2(evictee)

            if self.table2[h_val] is None:
                self.table2[h_val] = evictee
            else:
                evictee2 = self.table2[h_val]
                self.table2[h_val] = evictee
                h_val = self.hash1(evictee2)
                if self.table1[h_val] is None:
                    self.table1[h_val] = evictee2
                else:
                    self.evict(evictee2, i+1)

    #this function rehashes AND resizes both the tables
    def rearrange(self):
        print("rehashing table!!!")
        copy = []
        for i in self.table1:
            if i != None:
                copy.append(i)
        for i in self.table2:
            if i != None:
                copy.append(i)
        self.table1 = [None] * self.n
        self.table2 = [None] * self.n
        for el in copy:
            if el is None:#JUST to be sure lol
                print(i, el)
            self.insert(el)

    def hash1(self, key):
        return key%self.n

    def hash2(self, key):
        if self.scalar == 1:
            return int(key/11)%11
        else: # NEW HASH FUNCTION FOR TABLE 2
            return int(key/self.n+key%self.n)%self.n

    def delete(self, key):
        h_val = self.hash1(key)
        if self.table1[h_val] == key:
            self.table1[h_val] = None
            print("Element ", key, " successfully deleted.")
        else:
            h_val = self.hash2(key)
            if self.table2[h_val] == key:
                self.table2[h_val] = None
                print("Element ", key, " is successfully deleted ")
            else:
                print("Key was not found :((")

    def print_tables(self):
        print("++++++++++++++++++++++++++++PRINTING TABLES++++++++++++++++++++++++++++")
        print ("Table 1: \n", self.table1)
        print ("\nTable 2: \n", self.table2, "\n")
def main():
    my_hash = Cuckoo()
    # my_hash.insert(3)
    # my_hash.insert(32)
    # my_hash.insert(41)
    # my_hash.insert(54)
    # my_hash.insert(45)
    # my_hash.insert(14)
    # my_hash.insert(11)
    # my_hash.insert(18)
    # my_hash.insert(177)
    # my_hash.insert(44)
    # my_hash.insert(84)
    # my_hash.insert(17)
    # my_hash.insert(54)
    # my_hash.insert(88)
    # my_hash.insert(69)
    # my_hash.print_tables()
    # my_hash.search(707)
    # my_hash.search(94)
    # my_hash.search(169)
    while 1:
        print("____________________________")
        print("Enter A to print tables")
        print("Enter B to insert key")
        print("Enter C to delete key")
        print("Enter D to search key")
        print("Enter Q to quit")
        choice = input("Enter Choice: ")
        if choice == "A":
            my_hash.print_tables()
        elif choice == "B":
            my_hash.insert(int(input("Enter key to insert: ")))
        elif choice == "C":
            my_hash.delete(int(input("Enter key to delete: ")))
        elif choice == "D":
            my_hash.search(int(input("Enter key to search: ")))
        elif choice == "Q":
            break
        else:
            print("invalid entry")



if __name__ == "__main__":
    main()

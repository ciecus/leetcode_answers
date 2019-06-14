import sys

def replace_space(string):
    p1 = len(string)-1
    if p1 <0:
        return "None"
    else:
        i = 0
        for char in string:
            if char == " ":
                i += 1
        p2 = p1+2*i
        string_new = ['0' for i in range(p2)]
        while p2!=p1:
            char = string[p1-1]
            if char != " ":
                string_new[p2-1] = string[p1-1]
                p2-=1
                p1-=1
            else:

                string_new[p2-3:p2] = ['%','2','0']
                p2-=3
                p1-=1
        string_new[:p2] = string[:p1]

    return string_new

if __name__ == "__main__":
    string = list(sys.stdin.readline())
    print("".join(replace_space(string)))

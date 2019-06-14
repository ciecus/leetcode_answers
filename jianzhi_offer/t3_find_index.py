import sys

def find_number(num,n,m,matrix):
    y = 0
    x = m-1
    while num != matrix[y][x]:
        if num < matrix[y][x]:
            if x-1<0:
                return "None"
            else:
                x-=1
        if num >matrix[y][x]:
            if y+1<n:
                y+=1
            else:
                return 'None'
    return "yes"

if __name__ == "__main__":
    num = input()
    n = input()
    m = input()
    matrix = []
    for i in range(n):
        values = [int(x) for x in sys.stdin.readline().strip().split()]
        matrix.append(values)
    print(find_number(num,n,m,matrix))

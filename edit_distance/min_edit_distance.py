def min_edit_distance(string1,string2):
    m = len(string1)
    n = len(string2)
    matrix = [[0]*(n+1) for i in range(m+1)]
    #matrix initial
    for i in range(n+1):
        matrix[0][i] = i
    for i in range(m+1):
        matrix[i][0] = i
    #dp programme
    for i in range(1,m+1):
        for j in range(1,n+1):
            if string1[i-1] == string2[j-1]:
                temp = 0
            else:
                temp =1
            matrix[i][j] = min(matrix[i-1][j-1]+temp,matrix[i-1][j]+1,matrix[i][j-1]+1)
    return matrix[m][n]

if __name__ == "__main__":
    string1 = input().strip()
    string2 = input().strip()
    min_edit_distance(string1,string2)
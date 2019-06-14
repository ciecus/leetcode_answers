import sys

def duplicated_number_1(n,values):
    if (len(values) != n) |(len(values)==0):
        print('the wrong input')
    else:
        values.sort()
        dup_list = []
        for i in range(n-1):
            if values[i] == values[i+1]:
                dup_list.append(values[i])
        dup_list = set(dup_list)
        if len(dup_list)>0:
            string = ''
            for dup in dup_list:
                string += str(dup)+'\t'
            print(string)
        else:
            print('no duplicates')

def duplicated_number_2(n,values):
    if (len(values) != n) | (len(values) == 0):
        print('the wrong input')
    else:
        value_dict = {}
        dup_list = set([])
        for value in values:
            if value in value_dict:
                dup_list.appen(value)
        dup_list = set(dup_list)
        if len(dup_list) > 0:
            string = ''
            for dup in dup_list:
                string += str(dup) + '\t'
            print(string)
        else:
            print('no duplicates')


if __name__ == "__main__":
    n = input()
    values = [int(x) for x in sys.stdin.readline().strip().split()]
    duplicated_number_1(n, values)


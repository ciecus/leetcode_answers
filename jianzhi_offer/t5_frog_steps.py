import sys
def frog_steps(n):
    if not isinstance(n,int):
        return 'wrong input'
    else:
        if n in {0,1}:
            return 1
        elif n == 2:
            return 2
        else:
            list_ = [1 for i in range(n+1)]
            for i in range(2,n+1):
                list_[i] = list_[i-1]+list_[i-2]
            return list_[n]

if __name__ == "__main__":
    n = input()
    print(frog_steps(n))
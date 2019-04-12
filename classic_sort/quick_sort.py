"""
算法思想：
（1）选取一个数字作为基准，可以选取末位数字或者首位数字
（2）小于该基准数字就放在左边，大于该基准数字放在右边
（3）对于两个数组重复（1）（2）

两个指针left，right分别指向列表的第一个元素和最后一个元素，然后取一个参考值，默认为第一个列表的第一个元素list[0]，称为K
然后left指向的值先和参考值K进行比较，若list[left]小于或等于K值，left就一直向右移动，left+1，直到移动到大于K值的地方，停住
right指向的值和参考值K进行比较，若list[right]大于K值，right就一直向左移动，right-1，直到移动到小于K值的地方，停住
此时，left和right若还没有相遇，即left还小于right，则二者指向的值互换
若已经相遇则说明，第一次排序已经完成，将list[right]与list[0]的值进行互换，进行之后的递归

"""
#算法导论解法
def quick_sort(arr,l,r):
    if l < r:
        q = partition(arr,l,r)
        partition(arr,l,q-1)
        partition(arr,q+1,r)
def partition(arr,l,r):
    key = arr[r]
    i = l-1
    for j in range(l,r):
        if arr[j] <= key:
            i +=1
            arr[i],arr[j] = arr[j],arr[i]
    arr[i+1],arr[j] = arr[j],arr[i+1]
    return i+1



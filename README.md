＃leetcode_answers
记录一些leetcode题目和解题思路，欢迎小伙伴一起组队呀


补充剑指offer笔记
# 题目一：找出数组中重复的数字
书P39
github代码名称：t1_duplicated_numbers.py
在一个长度为n的数组里的所有数字都在0～n-1的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。例如，如果输入长度为7的数组{2,3,1,0,2,5,3},那么对应的输出是重复的数字2或者3.

==解题思路==
思路一：先排序，排序的时间复杂度为O(nlogn),然后从头到尾扫描
思路二：利用哈希表，字典结构，时间复杂度O(n),空间复杂度O(n)
思路三【比较复杂】：数组中的数字都在0~n-1的范围内。如果这个数字中没有重复的数字，排序之后数字i将出现在下标为i的位置。
所以可以从头到尾扫描这个数组的每个数字，当扫描到下标为i的数字时，首先比较这个数字是不是等于i，如果不是就拿它和第m个数字进行比较。如果它和m个数字相等就找到了一个重复数字。如果和第m个数字不想等，就和第m个数字交换。【太复杂了，暂缓】

==测试用例==
（1）长度为n的数组里包含一个或者多个重复的数字。
（2）数组中不包含重复的数字
（3）无效测试用例（输入空指针：长度为n的数组中包含0～n-1之外的数字）

==输入格式 ==
数组长度n
输入数组 长度为n的列表
例如：
3
1 2 2

==代码==
方法一：

```
import sys

def duplicated_number(n,values):
    if len(values) != n:
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

if __name__ == "__main__":
    n = input()
    values = [int(x) for x in sys.stdin.readline().strip().split()]
    duplicated_number(n, values)

```
方法二：

```
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
```

# 题目二：不修改数组找出重复数字
书P41
在一个长度为n+1的数组里的所有数字都在1～n的范围内，所以数组中至少有一个数字时重复的。请找出数组中任意一个重复的数字，但不能修改输入的数组。例如，如果输入长度为8的数组{2,3,5,4,3,2,6,7}，那么对应的输出时重复的数字2或者3。

==思路分析==
和上一题类似，但是不能修改数组，所以就不能直接排序了。
但是使用哈希表的空间复杂度为o(n)
如果优化的话，可以从二分查找的角度出发，调用countrange函数，调用O(logn)次，每次需要O(n)的时间，总时间复杂度为O(nlongn),空间复杂度为O(1)。和哈希表相比的空间换时间。

# 题目三：二维数组中的查找
书p44
github代码名称：t3_find_index.py
在一个二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，判断数组汇总是否含有该整数。

例如下面数组

|1|2 |8|9|
|--|--|--|--|
| 2 |4  |9|12|
|4|7|10|13|
|6|8|11|15|
==思路分析==

这道题比较巧妙的技巧应该从右上角搜索。
如果搜索数字7:
对于右上角的数字9，9是第四列最小的数字，因为9大于7，所以7不可能在第4列，
同理不在第三列，所以应在在第2列或者第1列，然后从最右上角的数字2往下搜索。
因为2是第一行现在剩下的最大的数字，所以不在第一行，
然后4是第二行剩下的最大数字，所以不在第二行，
然后就搜索到了7。


假如搜索数字5，从4往下接着搜索，然后发现7大于5，所以5不在第二列。
往左走到4，发现4小于5，所以往下走。
然后是6大于5，往左走，发现不可以了。就结束，找不到。

==思路总结==
从右上角开始遍历，如果待比较的数字小于右上角的数字，就往左走，如果大于右上角的数字就往下走。知道out of index终结。

==测试用例==
（1）二维数组中包含查找的数字
（2）二维数组中没有查找的数字
（3）特殊输入用例，输入空指针
输入格式：
待查找的数组num
行数n，
列数m，
数组
输出格式：如果找到输出yes 否则输出none
例如
7
3 
2
1 2 
2 4
4 6


==代码==

```
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

```

# 题目四：替换空格
书p51
github代码名称：jianzhi_offer/t4_replace_space.py
请实现一个函数，把字符串中的每个空格替换成"%20"，例如，输入“we are happy。”则输出"we%20are%20happy."


==思路分析==
（1）如果一个空格替换成"%","2","0"这3个字符，因此字符串会变长。所以如果没有测试用例应该提问面试官是不是覆盖。
（2）替换操作就是每次往后移动两个字节，但是复杂度为$O(n^2)$
(3)可以先遍历数空格个数，然后进行替换。使用两个指针，p1和p2，p1指向原字符串的末尾，p2指向替换之后的字符串的末尾，然后直到p1和p2位置相等为止。



==测试用例==
（1）输入字符串包含空格。空格位于最前面，空格位于最后面，空格位于中间，连续有多个空格
（2）输入的字符串中没有空格
（3）特殊用例，输入为空字符串，输入只有一个空格

==代码==

```
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

```

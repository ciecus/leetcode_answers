"""
用两个栈来实现一个队列，完成队列的Push和Pop操作。 队列中的元素为int类型。
https://www.nowcoder.com/practice/54275ddae22f475981afa2244dd448c6?tpId=13&tqId=11158&rp=2&ru=%2Factivity%2Foj&qru=%2Fta%2Fcoding-interviews%2Fquestion-ranking
"""


class Solution:
    def __init__(self):
        self.stackA = []#push
        self.stackB = []#pop
    def push(self, node):
        self.stackA.append(node)

    # write code here
    def pop(self):
        if self.stackB:
            return self.stackB.pop()
        elif self.stackA:
            while self.stackA:
                self.stackB.append(self.stackA.pop())
            return self.stackB.pop()
        else:
            return None


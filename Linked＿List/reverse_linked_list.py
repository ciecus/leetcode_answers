#https://leetcode.com/problems/reverse-linked-list/
#leetcode 格式
class ListNode(object):
    def __init__(self,x):
        self.val = x
        self.next = None
class Solution(object):
    def reverseList(self,head):
        if head == None:
            return None
        L = None
        M = None
        R = head
        while R.next != None:
            L = M
            M = R
            R = R.next
            M.next = L
        R.next = M
        return R


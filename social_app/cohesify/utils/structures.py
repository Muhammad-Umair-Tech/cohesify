class UserNode:
    def __init__(self, user):
        self.user = user
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Append
    def add_friend(self, user):
        new_node = UserNode(user)
        if self.head == None:
            self.head = new_node
            return True
        temp = self.head
        while temp.next is not None:
            temp = temp.next
        temp.next = new_node
        new_node.next = None
        return True

    def remove_friend(self, username):
        if self.head == None:
            return False
        if self.head.user.username == username:
            to_del = self.head.user
            if self.head.next is not None:
                self.head = self.head.next
            else:
                self.head = None
            return True
        temp = self.head
        while temp.next is not None and temp.next.user.username != username:
            temp = temp.next
        if temp.next is None:
            return None
        to_del = temp.next
        if temp.next.next is not None:
            temp.next = temp.next.next
        else:
            temp.next = None
        return True

    def load_all_friends(self, curr_user):
        friends = curr_user.friends.all()
        for friend in friends:
            self.add_friend(friend)

    def get_arr(self):
        arr = []
        if self.head == None:
            return arr
        temp = self.head
        while temp is not None:
            arr.append(temp)
            temp = temp.next
        return temp
    

class PostNode:
    def __init__(self, post):
        self.post = post
        self.next = None


class Queue:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head == None

    def peek(self):
        if self.head == None:
            return None
        return self.head

    def enqueue(self, post):
        new_node = PostNode(post)
        if self.head == None:
            self.head == new_node
            return True
        temp = self.head
        while temp.next is not None:
            temp = temp.next
        temp.next = new_node
        new_node.next = None
        return True
    
    def dequeue(self):
        if self.head == None:
            return None
        to_remove = self.head
        if self.head.next == None:
            self.head = None
        else:
            self.head = self.head.next
        return to_remove

    def load_all_posts(self, curr_user):
        posts = curr_user.posts.all()
        for post in posts:
            self.enqueue(post)

    def remove(self, post_id):
        if self.head is None:
            return False
        if self.head.id == post_id:
            if self.head.next is not None:
                self.head = self.head.next
            else:
                self.head = None
            return True
        temp = self.head
        while temp.next is not None and temp.next.id != post_id:
            temp = temp.next
        if temp.next is None:
            return False
        if temp.next.next is not None:
            temp.next = temp.next.next
        else:
            temp.next = None
        return True


class Stack:
    def __init__(self):
        self.top = -1
        self.arr = []

    @property
    def is_empty(self):
        return self.top == -1
    
    def pop(self):
        if self.top == -1:
            return None
        value = self.arr.pop()
        self.top -= 1
        return value
    
    def peek(self):
        if self.top == -1:
            return None
        value = self.arr[self.top]
        return value
    
    def push(self, value):
        self.top += 1
        self.arr.append(value)

    def clear_stack(self):
        self.arr.clear()
        self.top = -1


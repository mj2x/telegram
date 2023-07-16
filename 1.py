from __future__ import annotations
from anytree import Node as nodetree, RenderTree
class Node(nodetree):
    def __str__(self) -> str:
        string=""
        for pre, fill, node in RenderTree(self):
            string+="%s%s" % (pre, node.name)+"\n"
        return string
    def children_name(self)->list:
        out=[]
        for i in range(len(super().children)):
            out.append(super().children[i].name)
        return out
home_out=Node("home out")

signup=Node("sign-up",parent=home_out)
back=Node("back",parent=signup)

signin=Node("sign-in",parent=home_out)
back=Node("back",parent=signin)

home_in=Node("home in")
my_words=Node("my words",parent=home_in)
add=Node("add",parent=my_words)
back=Node("back",parent=my_words)
my_friends=Node("my friends",parent=home_in)
back=Node("back",parent=my_friends)
setting=Node("setting",parent=home_in)
back=Node("back",parent=setting)
logout=Node("logout",parent=home_in)

class menu():
    def __init__(self,root:Node) -> None:
        self.root=root
        self.current_step=root
        self.url=root.name+"/"
    def to(self,node_name:str)->menu:
        if node_name in self.current_step.children_name():
            for i in range(len(self.current_step.children)):
                if self.current_step.children[i].name==node_name:
                    self.current_step=self.current_step.children[i]
                    self.url+=node_name+"/"
                    return self
        else:
            raise ValueError("NO CHILDREN LIKE "+node_name)
    def step_back(self)->menu:
        if self.current_step.parent:
            self.current_step=self.current_step.parent
            self.url=self.url[:self.url[:len(self.url)-1].rindex("/")+1]
        return self
    def goto(self,url)->menu:
        url_list=url.split("/")[:-1]
        
        if url_list[0]==self.root.name:
            self.current_step=self.root
            self.url=self.root.name+"/"
            url_list=url.split("/")[1:-1]
            for i in url_list:
                self.to(i)
            return self
        else:
            raise ValueError("no such url root")
# a="s/f/g/ad/gggg/g/af/3e/w/w/f/f/w/q/"
# print(a[:-1])

# print(navigate.url)
# navigate.to("my words")
# print(navigate.url)
# navigate.to("add")
# print(navigate.url)
# navigate.step_back()
a=menu(home_in)
a.to("my words").to("add").to("add").to("add")
print(a.url)

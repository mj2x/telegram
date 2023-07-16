from __future__ import annotations
import requests
import json
from types import SimpleNamespace as SNS
dbconnection=None
users_step={}
user_info={}
def execute_non_query(sql_obj,query):
    sql_obj.execute(query)
    sql_obj.commit()
def execute_query(sql_obj,query):
    curs=sql_obj.execute(query)
    
    List=[]

    for row in curs:
        dic={}
        for id,col in enumerate(curs.description):
            dic[col[0]]=row[id]
        List.append(dic)
    return List
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

    
class thread:
    def __init__(self,target,args=()):
        self.__result=None
        self.__exception=None
        self.instants=None
        import threading
        self.instants=threading.Thread(target=self.__def,args=(target,args,))
        self.instants.start()
    def __def(self,target,args):
        try:
            self.__result=target(*args)
        except Exception as x:
            print(x)
            self.__exception=x
    @property
    def result(self):
        if self.instants==None:
            raise Exception ("Thread is not called")
        return self.__result
    @property
    def exception(self):
        return self.__exception
    @property
    def is_alive(self):
        if self.instants==None:
            raise Exception ("Thread is not called")
        return self.instants.is_alive()
class bot():
    def __init__(self,token:str) -> None:
        self.token=token
        self.stop_pulling=False
    def start_pulling(self,handler:any):
        last_offset=0
        import time
        while(not self.stop_pulling):
            url = f"https://api.telegram.org/bot{self.token}/getUpdates"
            try:
                resp = requests.get(url,params={"offset":last_offset+1})
            except Exception as x:
                print(x)
            json_result=resp.json()
            for i in json_result["result"]:
                
                studentJsonData = json.dumps(i)
                studObj = json.loads(studentJsonData, object_hook=lambda d: SNS(**d))
                thread(handler,(studObj,))
                last_offset=i['update_id']
            time.sleep(1)
    def set_commands(self,commands:json):
        try:
            url = f"https://api.telegram.org/bot{self.token}/setMyCommands"
            f=requests.post(url,params={"commands":str(json.dumps(commands))})
            return f.content
        except Exception as x:
            print(x)
    def deleteMessage(self,chat_id, message_id):
        try:
            url = f"https://api.telegram.org/bot{self.token}/deleteMessage"
            f=requests.post(url,params={"chat_id":chat_id,"message_id":message_id})
            return f.content
        except Exception as x:
                print(x)
    def send_message(self,chat_id,text
                     ,disable_web_page_preview=False
                     ,disable_notification=False
                     ,protect_content=False
                     ,reply_to_message_id=None
                     ,allow_sending_without_reply=False
                     ,reply_markup={}):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            f=requests.post(url,params={"chat_id":chat_id,
                                            "text":text,
                                            "disable_web_page_preview":disable_web_page_preview,
                                            "disable_notification":disable_notification,
                                            "protect_content":protect_content,
                                            "reply_to_message_id":reply_to_message_id,
                                            "allow_sending_without_reply":allow_sending_without_reply,
                                            "reply_markup":reply_markup,})
            return f.content
        except Exception as x:
                print(x)
def show_menu_as_keyboard(text,chat_id,top_keyboard:list=[],keyboard_type="keyboard",disable_menu=False):
    keyboard=[]
    for i in top_keyboard:
        t=[]
        for j in i:
            a={}
            a["text"]=j
            a["callback_data"]=j
            t.append(a)
        keyboard.append(t)
    if not disable_menu:
        for i in users_step[chat_id].current_step.children_name():
            a={}
            a["text"]=i
            a["callback_data"]=i
            keyboard.append([a])
    
    keyboard=json.dumps({keyboard_type:keyboard })
    boter.send_message(chat_id,text,reply_markup=keyboard)
def message_text_handler(message:SNS):
    global dbconnection
    if hasattr(message,"callback_query"):
        if message.callback_query.data=="back":
            if users_step[message.callback_query.message.chat.id].current_step.parent:
                users_step[message.callback_query.message.chat.id]=users_step[message.callback_query.message.chat.id].step_back()
                execute_non_query(dbconnection,f"update user_info set step='{users_step[message.callback_query.message.chat.id].url}' where chat_id={message.callback_query.message.chat.id}")
                boter.deleteMessage(message.callback_query.message.chat.id,message.callback_query.message.message_id)
                show_menu_as_keyboard("backed",message.callback_query.message.chat.id)
        elif message.callback_query.data=="friends" and users_step[message.callback_query.message.chat.id].url=="home in/my words to my friends/groups/":
            
            
            
            boter.deleteMessage(message.callback_query.message.chat.id,message.callback_query.message.message_id)

    elif hasattr(message,"message"):
        if message.message.text=="/start":
            show_menu_as_keyboard("wellcome",message.message.chat.id)
        elif message.message.text=="back":
            if users_step[message.message.chat.id].current_step.parent:
                users_step[message.message.chat.id]=users_step[message.message.chat.id].step_back()
                show_menu_as_keyboard("backed",message.message.chat.id)
                execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")
        elif message.message.text=="my words to my friends" and users_step[message.message.chat.id].url=="home in/":
            users_step[message.message.chat.id]=users_step[message.message.chat.id].to(message.message.text)
            show_menu_as_keyboard("ok",message.message.chat.id)
            execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")
        

        elif message.message.text=="groups" and users_step[message.message.chat.id].url=="home in/my words to my friends/":
            users_step[message.message.chat.id]=users_step[message.message.chat.id].to(message.message.text)
            text="friends:\n"
            temp=execute_query(dbconnection,f"select * from groups where owner='{message.message.chat.id}'")
            for i in temp:
                text+=f"              {i['name']}       \n"
            show_menu_as_keyboard(text,message.message.chat.id,keyboard_type="inline_keyboard",top_keyboard=[["send stuff to this group"],["friends"],["stuffs"]])
            execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")
        
        elif message.message.text=="Create New Group" and users_step[message.message.chat.id].url=="home in/my words to my friends/":
            users_step[message.message.chat.id]=users_step[message.message.chat.id].to(message.message.text)
            show_menu_as_keyboard("send the name of new group",message.message.chat.id)
            execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")
        
        # create new group
        elif users_step[message.message.chat.id].url=="home in/my words to my friends/Create New Group/":
            temp=execute_query(dbconnection,f"select * from groups where name='{message.message.text}' and owner='{message.message.chat.id}'")
            if len(temp)==0:
                execute_non_query(dbconnection,f"insert into groups (name,owner) values ('{message.message.text}','{message.message.chat.id}')")
                users_step[message.message.chat.id]=users_step[message.message.chat.id].step_back()
                execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")
                show_menu_as_keyboard(f"Done created group named {message.message.text}",message.message.chat.id)
            else:
                users_step[message.message.chat.id]=users_step[message.message.chat.id].step_back()
                execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")
                show_menu_as_keyboard(f"you already have this group named :{message.message.text}",message.message.chat.id)

        else:
            if message.message.text in users_step[message.message.chat.id].current_step.children_name():
                users_step[message.message.chat.id]=users_step[message.message.chat.id].to(message.message.text)
                show_menu_as_keyboard("ok",message.message.chat.id)
                execute_non_query(dbconnection,f"update user_info set step='{users_step[message.message.chat.id].url}' where chat_id={message.message.chat.id}")

def message_handler(message:SNS):
    print(message)
    global dbconnection
    dbconnection = sqlite3.connect('.\\databases.db')

    try:
        if hasattr(message,"message"):
            chatid=message.message.chat.id
        elif hasattr(message,"callback_query"):
            chatid=message.callback_query.message.chat.id

        if chatid in users_step:
            temp=execute_query(dbconnection,f"select * from user_info where chat_id='{chatid}'")
            if temp[0]["loged_in"]:
                message_text_handler(message)
            else:
                pass
        else:
            temp=execute_query(dbconnection,f"select * from user_info where chat_id='{chatid}'")
            if len(temp)>0:
                if temp[0]["loged_in"]:
                    temp[0]["input_mode"]=False
                    user_info[chatid]=temp[0]
                    menu_temp=menu(home_in).goto(temp[0]["step"])
                    users_step[chatid]=menu_temp
                    message_text_handler(message)
                else:
                    pass
            else:
                print("new_user")

                
    except Exception as x:
        print(x)
    dbconnection.close()

from anytree import Node as nodetree, RenderTree
class Node(nodetree):
    def __init__(self, name, parent=None, children=None, **kwargs):
        super().__init__(name, parent, children, **kwargs)
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
my_words_to_my_friends=Node("my words to my friends",parent=home_in)
group=Node("groups",parent=my_words_to_my_friends)
back=Node("back",parent=group)
Specials=Node("Specials",parent=my_words_to_my_friends)
back=Node("back",parent=Specials)
Create_New_Special=Node("Create New Special",parent=my_words_to_my_friends)
back=Node("back",parent=Create_New_Special)
Create_New_Group=Node("Create New Group",parent=my_words_to_my_friends)
back=Node("back",parent=Create_New_Group)
back=Node("back",parent=my_words_to_my_friends)
my_friends_words_for_me=Node("my friends words for me",parent=home_in)
back=Node("back",parent=my_friends_words_for_me)
setting=Node("setting",parent=home_in)
back=Node("back",parent=setting)
logout=Node("logout",parent=home_in)
print(home_in)
import sqlite3

boter=bot("6147919570:AAGuLLWoWqMG9j-21rSrGjdivIhfICeLcgY")
boter.set_commands([{"command":"/start", "description":"start the bot"},{"command":"/home", "description":"go home"}])
boter.start_pulling(message_handler)
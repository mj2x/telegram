top_keyboard=[[1,3],[2,2],[8,9]]
out=[]
for i in top_keyboard:
    t=[]
    for j in i:
        a={}
        a["text"]=j
        t.append(a)
    out.append(t)
print(out)
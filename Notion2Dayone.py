import pandas as pd


allres = []
for fs in files:
    fs = '/Users/shixiaoying/Downloads/11/'+fs
    f2=open(fs, 'r')
    data=[i.strip() for i in f2.readlines()]
    res = [data[2]]
    res.extend(data[7:])
    res = [i for i in res if 'png' not in i]
    res[0]='Date:'+res[0].split()[3]+'年'+str(cal_dict[res[0].split()[1][0:3]])+'月'+res[0].split()[2].replace(',', '')+'日 GMT+8 上午7:21:00\n\n\n'
    allres.extend(res)
    f2.close()

with open('notion.txt', 'w', encoding = 'utf-8') as f:
    for rec in allres:
        f.write(rec + '\n')
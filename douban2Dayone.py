import pandas as pd

boolist=['https' in i for i in tb.content.to_list()]
rows=tb.index[[i for i, x in enumerate(boolist)  if x]]
tb.drop(rows, inplace=True)
boolist=['读过这本书' in i for i in tb.content.to_list()]
rows=tb.index[[i for i, x in enumerate(boolist)  if x]]
tb.drop(rows, inplace=True)
boolist=['看过这部剧集' in i for i in tb.content.to_list()]
rows=tb.index[[i for i, x in enumerate(boolist)  if x]]
tb.drop(rows, inplace=True)
boolist=['豆瓣' in i for i in tb.content.to_list()]
rows=tb.index[[i for i, x in enumerate(boolist)  if x]]
tb.drop(rows, inplace=True)



tb.content=[i.replace('UserName 读过这本书:','') for i in tb.content.tolist()]
tb.content=[i.replace('UserName 看过这部剧集:','') for i in tb.content.tolist()]
tb.content=[i.replace('UserName 看过这部电影:','') for i in tb.content.tolist()]
tb.content=[i.replace('UserName 说:','') for i in tb.content.tolist()]

tb.content=[i.replace('[推荐]','') for i in tb.content.tolist()]


tb=pd.read_csv('/Users/shixiaoying/movie.txt', sep='\t')
tb.to_csv('movie.txt',sep='\t',index=False)


tb.Time = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('Date:%Y年%m月%d日 GMT+8 下午2:2:2') for x in tb.Time.to_list()]



with open('res1.txt', 'w', encoding = 'utf-8') as f:
    for rec_index, rec in tb.iterrows():
        if len(rec['content']) > 1:
            f.write(rec['Time'] +   '\n\n\n')
            f.write(rec['content'] + '\n\n\n')


with open('res2.txt', 'w', encoding = 'utf-8') as f:
    for rec_index, rec in tb.iterrows():
        if len(rec['content']) > 1:
            f.write(rec['Time'] +   '\n\n\n')
            f.write(rec['content']+'\n')
            f.write('#评论\n\n\n')

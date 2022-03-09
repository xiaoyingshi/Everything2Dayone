import pandas as pd

draftcsv = pd.read_csv('/Users/shixiaoying/DraftsExport.csv', sep=',')
create_time=draftcsv.created_at.to_list()
create_time = [re.split('-|:|T|Z',i) for i in create_time]
create_time = ['Date:'+res[0]+'年'+res[1]+'月'+res[2]+'日 GMT+8 下午9:21:00\n\n\n' for res in create_time]


draft=pd.DataFrame(zip(create_time, draftcsv.content.tolist()), columns=['Time','content'])


with open('draft.txt', 'w', encoding = 'utf-8') as f:
    for rec_index, rec in draft.iterrows():
        f.write(rec['Time']+'\n')
        f.write(rec['content']+'\n')
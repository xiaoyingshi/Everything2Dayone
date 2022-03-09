import pandas as pd


# 获取文件夹内所有的微博文件
def getAllFilePath(fPath):
    BlogList = []

    for root, dirs, files in os.walk(fPath):
        # print("根目录：",root,'\n')
        # print("所含目录：",dirs, '\n')
        # print("所含文件：",files, '\n——————————————————————————')
        for file in files:
            if '.html' in file:
                BlogA = file
                BlogList.append(BlogA)
    # 返回一个是html的日志内容list
    return BlogList

BlogList = getAllFilePath(r".")

allweibo = []
for blog in BlogList:
    blog = '/Users/shixiaoying/Downloads/weibo/'+blog
    f2=open(blog, 'r')
    weibo=[i.strip() for i in f2.readlines()]
    remove_list = ['Sakuraxxy2333','<span>','</span>','分享图片']
    weibo = [i for i in weibo if 'div' not in i ]
    weibo = [i for i in weibo if 'meta' not in i ]
    weibo = [i for i in weibo if 'head' not in i ]
    weibo = [i for i in weibo if 'html' not in i ]
    weibo = [i for i in weibo if 'link' not in i ]
    weibo = [i for i in weibo if '<i' not in i ]
    weibo = [i for i in weibo if 'href' not in i ]
    weibo = [i for i in weibo if 'content' not in i ]
    weibo = [i for i in weibo if 'style' not in i ]
    weibo = [i for i in weibo if 'title' not in i ]
    weibo = [i for i in weibo if 'article' not in i ]
    weibo = [i for i in weibo if 'article' not in i ]
    weibo = [i for i in weibo if '/a' not in i ]
    weibo = [i for i in weibo if '<ul' not in i ]
    weibo = [i for i in weibo if 'body' not in i ]
    weibo = [i for i in weibo if '<h3' not in i ]
    weibo = [i for i in weibo if '来自' not in i ]
    weibo = [i for i in weibo if '来自' not in i ]
    weibo = [i for i in weibo if i not in remove_list ]
    weibo = [i for i in weibo if 'm-auto-box' not in i ]
    allweibo.extend(weibo)
    f2.close()

# record index need be removed
index_record = []
for i in range((len(allweibo)-1)):
    if 'class="time"' in allweibo[i]:
        if 'class="time"' in allweibo[i+1]: 
            index_record.append(i)
            # remove
            
for index in sorted(index_record, reverse=True):
    del allweibo[index]
# allweibo = [i.replace('<span class="time">','').replace('</span>','') for i in allweibo]


# record index need be removed
index_record = []
for i in range((len(allweibo)-1)):
    if '<span class="time">' not in allweibo[i]:
        if '<span class="time">' not in allweibo[i+1]: 
            index_record.append(i)
            # remove
            
for index in sorted(index_record, reverse=True):
    allweibo[index] = allweibo[index]+'\n'+allweibo[index+1]
    del allweibo[index+1]


import calendar
cal_dict = {month: index for index, month in enumerate(calendar.month_abbr) if month}

for i in range(len(allweibo)):
    if '<span class="time">' in allweibo[i]:
        tmp=allweibo[i].replace('<span class="time">','').replace('</span>', '').split()
        clock=tmp[3].split(':')
        if int(clock[0])>12:
            clock[0]=str(int(clock[0])-12)
            time1='Date:'+tmp[5]+'年'+str(cal_dict[tmp[1]])+'月'+tmp[2]+'日 GMT+8 下午'+clock[0]+':'+clock[1]+':'+clock[2]
            
        else:
            time1='Date:'+tmp[5]+'年'+str(cal_dict[tmp[1]])+'月'+tmp[2]+'日 GMT+8 上午'+clock[0]+':'+clock[1]+':'+clock[2]
        allweibo[i] = time1
    else:
        allweibo[i] = allweibo[i]


import pandas as pd
weiboDF = pd.DataFrame(list(zip(allweibo[0::2], allweibo[1::2])),
               columns =['Time', 'content'])

stay_index=[]
for i in range(len(allweibo[1::2])) :
    if 'span' in allweibo[1::2][i] and '抱歉'  not in  allweibo[1::2][i] and '转发' not  in allweibo[1::2][i] and i!='</li></ul> ' and i!='</li></ul>' and '抱歉' not  in allweibo[1::2][i] :
        stay_index.append(i)



with open('weibo1.txt', 'w', encoding = 'utf-8') as f:
    for rec_index, rec in weiboDF1.iterrows():
        rec['content'] = rec['content'].strip()
        if len(rec['content']) > 1 and not rec['content'].isspace():
            f.write(rec['Time'] +   '\n\n\n')
            f.write(rec['content'].replace('<span>','').replace('</span>','').replace('<span class="m-line-gradient">','') + '\n\n\n')
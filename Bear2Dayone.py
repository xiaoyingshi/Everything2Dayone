import pandas as pd

# add Date
for file in os.listdir('/Users/shixiaoying/Documents/旧时琐碎/no'):
file='/Users/shixiaoying/Documents/旧时琐碎/no/'+file
res=time.gmtime(os.path.getmtime(file))
res = [str(i) for i in list(res)]
if int(res[3])>11:
res[3]=int(res[3])-12
res[3]=str(res[3])
res1 = "Date:	"+res[0]+"年"+res[1]+"月"+res[2]+"日"+" GMT+8 下午"+res[3]+":"+res[4]+":"+res[5]
else:
res1 = "Date:	"+res[0]+"年"+res[1]+"月"+res[2]+"日"+" GMT+8 上午"+res[3]+":"+res[4]+":"+res[5]
os.system("echo '"+res1+"' | cat - '"+file+"' > temp && mv temp '"+file+"'")


[datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(python) for x in l1]


# 增加2个空行

for i in `ls`; do sed -i 'tmp.txt' 's/Date.*/&\n\n\n\n/g' $i; done

# 去掉#

sed -i 'day' '/^#/d' /Users/shixiaoying/Documents/旧时琐碎/111
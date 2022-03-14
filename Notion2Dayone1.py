def notion2dayone(fname):
	draftcsv = pd.read_csv(fname, sep=',')
	draftcsv = draftcsv.dropna(how='all')
	print(fname)
	print(draftcsv)
	create_time=draftcsv.Date.to_list()
	create_time = [re.split('/',i) for i in create_time]
	create_time = ['Date:'+res[2]+'年'+res[0]+'月'+res[1]+'日 GMT+8 下午9:21:00\n\n\n' for res in create_time]
	draft=pd.DataFrame(zip(create_time, draftcsv.随手记.tolist()), columns=['Time','content'])
	draft=draft.dropna()
	with open(fname.split('/')[-1].replace('csv','txt'), 'w', encoding = 'utf-8') as f:
	    for rec_index, rec in draft.iterrows():
	    	f.write(rec['Time']+'\n')
	    	f.write(rec['content']+'\n\n')


fnames = ['/Users/shixiaoying/fitcsv/'+i for i in os.listdir('/Users/shixiaoying/fitcsv')]
for fname in fnames:
	if fname != '/Users/shixiaoying/fitcsv/.DS_Store':
		notion2dayone(fname)
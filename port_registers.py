import json
line=1
i=0
for port in range(10):
    file_name='port'+str(port)+'.txt'
    js_file='port'+str(port)+'.json'
    with open(file_name,'w') as f:
        with open(js_file,'r+') as fjson:
            data=json.load(fjson)
            for i in range(16):
                line=1
                for key,value in data.items():
                    hexbitt=format(int(value,16),'016b')
                    bitt=hexbitt[15-i]
#                    dstr=str(line)+'.'+' '+key+str(port)+'.'+str(i)+'='+str(bitt)
                    dstr = f'{line}. {key}{port}.{i}={bitt}'
                    f.write(dstr)
                    f.write('\n')
                    line=line+1 
                f.write('---------------------------------------------------')
                f.write('\n')
# 检查文件头的yaml，如果 title 错了，则修改为与文本名相同，如果没有写 yaml，则添上。


import time
from datetime import datetime
import os
import linecache

basedir="content//post"

def Checkyaml(path):
    for p in os.listdir(path):
        p = os.path.join(path, p)
        if os.path.isdir(p):
            Checkyaml(p)
        else:
            filemt= time.localtime(time.time())
            fileTime= time.strftime("%Y-%m-%d",filemt)
            print(p)

            # 快速检查前两行
            lines = linecache.getlines(p)[0:2]
            if len(lines) == 2:
                if lines[0]=="---\n":
                    if lines[1]==('title: '+os.path.splitext(os.path.basename(p))[0]+'\n'):
                        linecache.clearcache()
                        continue

            # 对不符合的文本进行修改
            linecache.clearcache()
            with open(p, 'r+',encoding= 'utf-8') as f:
                content = f.read()
                ls= content.splitlines(True)
                if len(ls) != 0:
                    if ls[0]=="---\n":
                        if ls[1]==('title: '+os.path.splitext(os.path.basename(p))[0]+'\n'):
                            pass
                        else:
                            ls[1]=('title: '+os.path.splitext(os.path.basename(p))[0]+'\n')
                            f.seek(0,0)
                            f.writelines(ls)
                            f.flush()
                    else:
                        f.seek(0, 0)
                        f.write('---\n'
                            +'title: '+os.path.splitext(os.path.basename(p))[0]+'\n'
                            +'toc: true\n'
                            +'date: '+fileTime+'\n'
                            +'---\n'
                            +content)
                        f.flush()


Checkyaml(basedir)



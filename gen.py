
import time
from datetime import datetime
import os

isFormal=1

basedir="content//post"
mdpath="content//catalog.md"


# basedir="C://Users//evo//Desktop//iterateself//content//post"
# mdpath="C://Users//evo//Desktop//iterateself//content//catalog.md"
urlbase="http://localhost:1313/post"
urlbase_formal="http://iterate.site/post"

basedir_len=len(basedir)


def ListFilesToTxt(dir,file,wildcard,recursion,levelnum):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    files.sort()
    for name in files:
        fullname=os.path.join(dir,name)
        if(os.path.isdir(fullname) & recursion):
            for x in range(levelnum):
                file.write("\t")
            file.write("- "+name +"\n")
            ListFilesToTxt(fullname,file,wildcard,recursion,levelnum+1)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    for x in range(levelnum):
                        file.write("\t")
                    if isFormal:
                        urlb=urlbase_formal
                    else:
                        urlb=urlbase
                    url=urlb+os.path.splitext(fullname)[0][basedir_len:].replace('\\','/').replace(' ','-').lower()
                    file.write("- ["+name +"]("+url+")\n")
                    break

def Test():
    wildcard = ".md"
    file = open(mdpath,"w",encoding= 'utf-8')
    file.write("---\n"
        +"title: 完整目录\n"
        +"date: 2017-08-20T21:38:52+08:00\n"
        +"lastmod: 2017-08-28T21:41:52+08:00\n"
        +"menu: main\n"
        +"weight: 50\n"
        +"---\n")
    ListFilesToTxt(basedir,file,wildcard, 1,levelnum=0)
    file.close()


Test()
---
title: wmi
toc: true
date: 2018-10-15
---
```
# MAC地址、CPU序列号、硬盘序列号



import os, sys
import time
import wmi,zlib

c = wmi.WMI()
#获取主板序列号
c.Win32_BaseBoard()[0].SerialNumber.strip()
#获取CPU序列号 速度有点慢
c.Win32_Processor()[0].ProcessorId.strip()



def get_disk_info():
    tmplist = []
    encrypt_str = ""
    c = wmi.WMI ()
    for cpu in c.Win32_Processor():
        # cpu 序列号
        encrypt_str = encrypt_str+cpu.ProcessorId.strip()
        print("cpu id:", cpu.ProcessorId.strip())

    for physical_disk in c.Win32_DiskDrive():
        encrypt_str = encrypt_str+physical_disk.SerialNumber.strip()
        #硬盘序列号
        print('disk id:', physical_disk.SerialNumber.strip())
        tmpdict = {}
        tmpdict["Caption"] = physical_disk.Caption
        tmpdict["Size"] = int(physical_disk.Size)/1000/1000/1000
        tmplist.append(tmpdict)

    for board_id in c.Win32_BaseBoard():
        # 主板序列号
        encrypt_str = encrypt_str+board_id.SerialNumber.strip()
        print("main board id:",board_id.SerialNumber.strip())
#          for mac in c.Win32_NetworkAdapter():

    #mac 地址（包括虚拟机的）
    # print "mac addr:", mac.MACAddress:
    for bios_id in c.Win32_BIOS():
        # bios 序列号
        encrypt_str = encrypt_str+bios_id.SerialNumber.strip()
        print("bios number:", bios_id.SerialNumber.strip())
        print("encrypt_str:", encrypt_str)

    #加密算法
    print(zlib.adler32(encrypt_str))
    return encrypt_str





if __name__ == "__main__":
#     a = get_cpu_info()
    get_disk_info()
```




```


import uuid

def get_mac_address1():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def get_mac_address():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

print(get_mac_address1())
print(get_mac_address())


import os, sys
import time
import wmi,zlib

c = wmi.WMI()
#获取主板序列号

print(c.Win32_BaseBoard()[0].SerialNumber.strip())
print(c)
#获取CPU序列号 速度有点慢
print(c.Win32_Processor()[0].ProcessorId.strip())


```

---
title: os 模块的一些常量
toc: true
date: 2018-06-22 22:15:54
---

# 需要补充的



代码如下：

```python
import os
print(os.name)
print(os.environ)
```


输出：

```text
nt
environ({'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\evo\\AppData\\Roaming', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'EVO-LI', 'COMSPEC': 'C:\\Windows\\system32\\cmd.exe', 'FPS_BROWSER_APP_PROFILE_STRING': 'Internet Explorer', 'FPS_BROWSER_USER_PROFILE_STRING': 'Default', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\evo', 'LOCALAPPDATA': 'C:\\Users\\evo\\AppData\\Local', 'LOGONSERVER': '\\\\EVO-LI', 'NUMBER_OF_PROCESSORS': '4', 'ONEDRIVE': 'C:\\Users\\evo\\OneDrive', 'OPENCVBUILD': 'E:\\14.Develop\\OpenCV\\opencv\\build', 'OS': 'Windows_NT', 'PATH': 'E:\\11.ProgramFiles\\Anaconda3\\Library\\bin;E:\\17.Start;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Program Files (x86)\\Windows Kits\\8.1\\Windows Performance Toolkit\\;C:\\Program Files\\Microsoft SQL Server\\110\\Tools\\Binn\\;C:\\Program Files\\Intel\\WiFi\\bin\\;C:\\Program Files\\Common Files\\Intel\\WirelessCommon\\;E:\\14.Develop\\Graphviz2.38\\bin;E:\\14.Develop\\Graphviz2.38\\bin\\dot.exe;E:\\11.ProgramFiles\\Anaconda3;E:\\11.ProgramFiles\\Anaconda3\\Scripts;E:\\11.ProgramFiles\\Anaconda3\\Library\\bin;C:\\Users\\evo\\AppData\\Local\\Microsoft\\WindowsApps;E:\\11.ProgramFiles\\Microsoft VS Code\\bin;C:\\Program Files\\Intel\\WiFi\\bin\\;C:\\Program Files\\Common Files\\Intel\\WirelessCommon\\;E:\\14.Develop\\Graphviz2.38\\bin', 'PATHEXT': '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 78 Stepping 3, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': '4e03', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PSMODULEPATH': 'C:\\Program Files\\WindowsPowerShell\\Modules;C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\Modules', 'PUBLIC': 'C:\\Users\\Public', 'PYCHARM_HOSTED': '1', 'PYTHONIOENCODING': 'UTF-8', 'PYTHONPATH': 'E:\\01.Learn\\01.Python\\01.PythonBasic', 'PYTHONUNBUFFERED': '1', 'SESSIONNAME': 'Console', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\Windows', 'TEMP': 'C:\\Users\\evo\\AppData\\Local\\Temp', 'TMP': 'C:\\Users\\evo\\AppData\\Local\\Temp', 'USERDOMAIN': 'EVO-LI', 'USERDOMAIN_ROAMINGPROFILE': 'EVO-LI', 'USERNAME': 'evo', 'USERPROFILE': 'C:\\Users\\evo', 'VS120COMNTOOLS': 'E:\\11.ProgramFiles\\VS\\Common7\\Tools\\', 'WINDIR': 'C:\\Windows'})
```



<span style="color:red;">上面这个 nt 是什么意思来着？之前好像还看到过的。再补充一下。</span>

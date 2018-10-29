 今天遇到一个 Python 的编码问题，一个 txt 的 UTF-8 格式的文件，文件里面存放了路径，我用 with open('1.txt',r,encoding='utf-8') as f 读出来的东西，print() 出来是正确的路径，
 但是使用 cv2.imread('path') 来读取文件的时候，总是说读不到。

 但是，我自己的 ANSI 格式的文件是可以正确 print ，也可以正确 imread 的。

 不知道为什么，为什么 print() 可以正确打印出来，但是 imread 却没有正确加载这个图片呢？

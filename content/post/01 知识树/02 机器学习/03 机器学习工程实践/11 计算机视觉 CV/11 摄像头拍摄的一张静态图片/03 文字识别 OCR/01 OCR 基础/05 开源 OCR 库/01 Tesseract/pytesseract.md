
# 需要补充的




# pytesseract

这个 README 上讲的还是很全面的






```python
import pytesseract
from PIL import Image

img_path="cutImages\\aa.png"
img_string=pytesseract.image_to_string(Image.open(img_path))
print(img_string)
```



# 相关资料

- [pytesseract](https://github.com/madmaze/pytesseract)

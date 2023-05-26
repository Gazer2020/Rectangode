from Rectangode import Rectangode
s = "My name's Chen Ke. I'm from SJTU."
r = Rectangode()
r.create(s)
r.calculating()
r.make_img()

# import numpy as np
# from PIL import Image

# path='./output.png'
# with Image.open(path) as img:
#     bits = np.array(img).astype(int)
# print(bits)
# bits[-5:, :5] = 1
# img = Image.new('1', bits.shape[::-1])
# img.putdata(bits.flatten())
# img.save(path)


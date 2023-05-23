from Rectangode import Rectangode
import numpy as np
from PIL import Image
s = "My name's Chen Ke. I'm from SJTU."
r = Rectangode(s)
r = Rectangode(s, 30, 20)
r.calculating(k=28)
r.make()


p = np.array(Image.open("output.png").getdata())
print(p)
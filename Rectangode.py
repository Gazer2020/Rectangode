import os
import numpy as np
from PIL import Image

# large position symbol size 8*8
L_POS = np.array([[1,1,1,1,1,1,1,0],
                  [1,0,0,0,0,0,1,0],
                  [1,0,1,1,1,0,1,0],
                  [1,0,1,1,1,0,1,0],
                  [1,0,1,1,1,0,1,0],
                  [1,0,0,0,0,0,1,0],
                  [1,1,1,1,1,1,1,0],
                  [0,0,0,0,0,0,0,0]])

# small position symbol size 6*6
S_POS = np.array([[1,1,1,1,1,0],
                  [1,0,0,0,1,0],
                  [1,0,1,0,1,0],
                  [1,0,0,0,1,0],
                  [1,1,1,1,1,0],
                  [0,0,0,0,0,0]])

class Rectangode:
    def __init__(self, _s:str, _c:int=0, _r:int=0):
        self.content = _s
        self.col = _c
        self.row = _r
        
        
    
    def calculating():
        """
        using numpy to concatenate
        """
        pass
    
    def padding():
        """
        if the length of the content is smaller than xxx,
        we need to padding it.
        """
        # haha
        pass
        
        
    def make(output:str='./output.png') -> None:
        img = Image.new('1', (self.col, self.row))
        img.putdata(self.bits)
        img.save(output)
    
    
    
    
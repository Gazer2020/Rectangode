import numpy as np
from reedsolo import RSCodec
from PIL import Image

# large position symbol size 8*8
L_POS = np.array([[1, 1, 1, 1, 1, 1, 1, 0],
                  [1, 0, 0, 0, 0, 0, 1, 0],
                  [1, 0, 1, 1, 1, 0, 1, 0],
                  [1, 0, 1, 1, 1, 0, 1, 0],
                  [1, 0, 1, 1, 1, 0, 1, 0],
                  [1, 0, 0, 0, 0, 0, 1, 0],
                  [1, 1, 1, 1, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])

# small position symbol size 6*6
S_POS = np.array([[0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 1],
                  [0, 1, 0, 0, 0, 1],
                  [0, 1, 0, 1, 0, 1],
                  [0, 1, 0, 0, 0, 1],
                  [0, 1, 1, 1, 1, 1]])


class Rectangode:
    def __init__(self, _s: str, _c: int = 0, _r: int = 0):
        self.content = _s
        self.col = _c
        self.row = _r

    def calculating(self):
        """
        using numpy to concatenate
        """
        rs = RSCodec()
        self.code = rs.encode(self.content.encode())
        self.code = np.array([list(format(byte, '08b'))
                             for byte in self.code]).astype(int)
        self.code.resize((self.code.size,))
        self.row = np.ceil(np.sqrt((self.code.size + 100)/2)).astype(int)
        self.col = np.ceil((self.code.size + 100) / self.row).astype(int)
        # print(self.row, self.col,self.code.size)
        if self.row < 14:
            part1 = np.array(self.code[:(self.col-8)*8])
            part2 = np.array(
                self.code[(self.col-8)*8:(self.col-8)*8 + (self.col-14)*(14-self.row)])
            part3 = np.array(
                self.code[(self.col-8)*8 + (self.col-14)*(14-self.row):])
            part1.resize(((self.row-6), (self.col-8)))
            part2.resize(((14-self.row), (self.col-14)))
            part3.resize((self.row-8, self.col-6))
            temp1 = np.concatenate((part1[:, :self.col-14], part2), axis=0)
            temp2 = np.concatenate((L_POS, temp1), axis=1)
            temp3 = np.concatenate((temp2, part3), axis=0)
            temp4 = np.concatenate((part1[:, self.col-14:], S_POS), axis=0)
            self.bits = np.concatenate((temp3, temp4), axis=1)
            self.bits.resize((self.row*self.col,))
        else:
            part1 = np.array(self.code[:(self.col-8)*8])
            part2 = np.array(
                self.code[(self.col-8)*8:(self.col-8)*8 + (self.col)*(self.row-14)])
            part3 = np.array(
                self.code[(self.col-8)*8 + (self.col)*(self.row-14):])
            part1.resize((8, (self.col-8)))
            part2.resize(((self.row-14), self.col))
            part3.resize((6, self.col-6))
            temp1 = np.concatenate((L_POS, part1), axis=1)
            temp2 = np.concatenate((temp1, part2), axis=0)
            temp3 = np.concatenate((part3, S_POS), axis=1)
            self.bits = np.concatenate((temp2, temp3), axis=0)
            self.bits.resize((self.row*self.col,))

    def make(self, output: str = './output.png') -> None:
        img = Image.new('1', (self.col, self.row))
        img.putdata(self.bits)
        img.save(output)


if __name__ == '__main__':
    s = '我是cheng ke，我来自SJTU。'
    r = Rectangode(s)
    r.calculating()
    r.make()

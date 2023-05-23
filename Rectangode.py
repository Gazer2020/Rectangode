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
    def __init__(self, _s: str, _r: int = 0, _c: int = 0):
        """It create a Rectangode class.

        Args:
            _s (str): the content string
            _c (int, optional): setting the number of rows. If set to 0, we'll do it ourselves. Defaults to 0.
            _r (int, optional): setting the number of columns. If set to 0, we'll do it ourselves. Defaults to 0.
        """
        self.content = _s
        self.row = _r
        self.col = _c

    def calculating(self, k: int = 10):
        """calculaing the bit matrix of the Reed-Solomon code of the content

        Args:
            k (int, optional): setting the length of the error-correcting code. Defaults to 10.
        """
        assert (k > 0 and k <= 255)

        self.k = k
        rs = RSCodec(nsym=self.k)
        self.code = rs.encode(self.content.encode())
        self.code = np.array([list(format(byte, '08b'))
                             for byte in self.code]).astype(int)
        self.code.resize((self.code.size,))
        
        if self.row and self.col:
            assert ((self.row*self.col) > (self.code.size + 108))
            assert (self.row > 8)
            assert (self.col > 15)
        else:
            self.row = np.ceil(np.sqrt((self.code.size + 108)/2)).astype(int)
            self.col = np.ceil((self.code.size + 108) / self.row).astype(int)

        # setting a symbol of the error correcting code
        error_code = np.array(
            list('0'*(8-len(bin(self.k)[2:])) + bin(self.k)[2:])).astype(int)
        error_code.resize((8, 1))

        if self.row < 14:
            part1 = np.array(self.code[: (self.row-6) * (self.col-9)])
            part2 = np.array(
                self.code[(self.row-6) * (self.col-9): (self.row-6) * (self.col-9) + (14-self.row)*(self.col-15)])
            part3 = np.array(
                self.code[(self.row-6) * (self.col-9) + (14-self.row)*(self.col-15):])
            part1.resize(((self.row-6), (self.col-9)))
            part2.resize(((14-self.row), (self.col-15)))
            part3.resize((self.row-8, self.col-6))

            temp1 = np.concatenate((L_POS, error_code), axis=1)
            temp2 = np.concatenate((part1[:, :self.col-15], part2), axis=0)
            temp3 = np.concatenate((temp1, temp2), axis=1)
            temp4 = np.concatenate((temp3, part3), axis=0)
            temp5 = np.concatenate((part1[:, self.col-15:], S_POS), axis=0)
            self.bits = np.concatenate((temp4, temp5), axis=1)
            self.bits.resize((self.row*self.col,))
        else:
            part1 = np.array(self.code[: 8*(self.col-9)])
            part2 = np.array(
                self.code[8*(self.col-9): 8*(self.col-9) + (self.row-14) * (self.col)])
            part3 = np.array(
                self.code[8*(self.col-9) + (self.row-14) * (self.col):])
            part1.resize((8, (self.col-9)))
            part2.resize(((self.row-14), self.col))
            part3.resize((6, self.col-6), refcheck=False)

            temp1 = np.concatenate((L_POS, error_code), axis=1)
            temp2 = np.concatenate((temp1, part1), axis=1)
            temp3 = np.concatenate((temp2, part2), axis=0)
            temp4 = np.concatenate((part3, S_POS), axis=1)
            self.bits = np.concatenate((temp3, temp4), axis=0)
            self.bits.resize((self.row*self.col,))
            print(self.bits)

    def make(self, output: str = './output.png') -> None:
        img = Image.new('1', (self.col, self.row))
        img.putdata(self.bits)
        img.save(output)


if __name__ == '__main__':
    s = "I'm Chen Ke."
    r = Rectangode(s)
    r.calculating()
    r.make()

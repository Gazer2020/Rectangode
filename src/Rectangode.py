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
    def __init__(self):
        """It create an empty class.
        You can use create to create an image from string.
        You can also use open to open an image.
        """
        pass

    def create(self, _s: str, _r: int = 0, _c: int = 0):
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

        if self.row and self.col:
            assert ((self.row*self.col) >
                    (len(self.content)*8 + self.k*8 + 108))
            assert (self.row > 8)
            assert (self.col > 15)
        else:
            self.col = np.ceil(
                np.sqrt((len(self.content)*8 + self.k*8 + 108)*2)).astype(int)
            self.row = np.ceil(
                (len(self.content)*8 + self.k*8 + 108) / self.col).astype(int)

        self.code = self.content.encode()
        self.code = rs.encode(self.code)

        print(self.code)
        self.code = np.array([list(format(byte, '08b'))
                             for byte in self.code]).astype(int)
        self.code.resize((self.code.size,))

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

    def make_img(self, output: str = './output.png') -> None:
        img = Image.new('1', (self.col, self.row))
        img.putdata(self.bits)
        img.save(output)

    def open_img(self, path: str = './output.png') -> None:
        with Image.open(path) as img:
            self.bits = np.array(img).astype(int)

    def converting(self) -> str:
        print(self.bits)
        while not np.array_equal(self.bits[:8, :8], L_POS) or not np.array_equal(self.bits[-6:, -6:], S_POS):
            self.bits = np.rot90(self.bits)
        error_code = ''.join(self.bits[:8, 8].copy().astype(str))

        print(error_code)
        self.k = int(error_code, base=2)

        self.row, self.col = self.bits.shape
        if self.row < 14:
            part1 = self.bits[:self.row-6, 9:].copy()
            part2 = self.bits[self.row-6:8, 9:self.col-6].copy()
            part3 = self.bits[8:, :self.col-6].copy()
            self.code = ''.join(part1.flatten().astype(
                str)) + ''.join(part2.flatten().astype(str)) + ''.join(part3.flatten().astype(str))
        else:
            part1 = self.bits[:8, 9:].copy()
            part2 = self.bits[8:self.row-6, :].copy()
            part3 = self.bits[self.row-6:, :self.col-6].copy()
            self.code = ''.join(part1.flatten().astype(
                str)) + ''.join(part2.flatten().astype(str)) + ''.join(part3.flatten().astype(str))

        self.code = bytes([int(self.code[i:i+8], 2)
                          for i in range(0, len(self.code), 8)]).rstrip(b'\x00')
        rs = RSCodec(nsym=self.k)
        print(self.code)
        return rs.decode(self.code)[0].decode()


if __name__ == '__main__':
    r = Rectangode()
    r.open_img()
    print(r.converting())

"""
cf. https://www.youtube.com/watch?v=gP4PqVGudtg
"""

import numpy as np
import math




class Hexadecimal:
    """
    This class represents a string encoded in hexadecimal
    
    :param str s: the string to convert
    """
    def __init__(self, s=str()):
        self.s = str()
        for char in s:
            self.s += hex(ord(char))[2:] # ord: "Return the Unicode code point for a one-character string."
                                        # Cette fonction renvoie "0xaa", donc on ne garde que les deux derniers caractères


    def decode(self) -> str:
        """
        Decodes the hexadecimal string into its plaintext shape.

        :return: the plaintext string
        :rtype: str
        """
        decoded = str()
        i = 0
        while i < len(self.s):
            decoded += bytearray.fromhex(self.s[i:i+2]).decode()
            i += 2
        return decoded


    def __add__(self, s):
        newHex = Hexadecimal()
        if type(s) != Hexadecimal:
            raise ValueError("s has to be Hexadecimal")
        newHex.s = self.s + s.s
        return newHex
    
    def __iadd__(self, s):
        if type(s) != Hexadecimal:
            raise ValueError("s has to be Hexadecimal")
        self.s += s.s
        return self
    
    def __eq__(self, h):
        return self.s == h.s

    def __len__(self):
        return int(len(self.s) / 2)

    def __getitem__(self, index: int):
        if index < 0:
            index += len(self)
        if index >= len(self) or index < 0: raise IndexError
        hexVal = Hexadecimal()
        hexVal.s = self.s[index*2: (index+1)*2]
        return hexVal

    def __repr__(self):
        return self.s
    
    def __str__(self):
        s = str()
        for char in self:
            s += char + " "
        return s[:-1]

    def __iter__(self):
        self._iterIndex = 0
        return self
    
    def __next__(self):
        i = self._iterIndex
        if i >= len(self.s):
            raise StopIteration
        self._iterIndex += 2
        return self.s[i:i+2]



class Matrix:
    def __init__(self, m: list[list]):
        self._matrix = m
    

    def size(self):
        return (len(self._matrix), len(self._matrix[0]))


    def shiftRow(self, rowIndex: int):
        """
        Rotates the row 1 time to the left

        :param int rowIndex: the index of the row to rotate
        """
        firstVal = self._matrix[rowIndex].pop(0)
        self._matrix[rowIndex].append(firstVal)


    def getRow(self, index: int):
        return self._matrix[index]
    
    def setRow(self, index: int, value: list):
        if self.size()[1] != len(value):
            raise ValueError("the value has to be of the same length as the matrix width")
        self._matrix[index] = value
    

    def getColumn(self, index: int):
        return [self._matrix[i][index] for i in range(len(self._matrix))]
    
    def setColumn(self, index: int, value: list):
        if self.size()[0] != len(value):
            raise ValueError("the value has to be of the same length as the matrix heigth")
        for i in range(len(value)):
            self[i, index] = value[i]


    def __getitem__(self, index: tuple[int, int]):
        return self._matrix[index[0]][index[1]]
    
    def __setitem__(self, index: tuple[int, int], value):
        self._matrix[index[0]][index[1]] = value

    def __add__(self, m):
        if self.size() != m.size():
            raise ValueError("both matrix has to be of the same size")
        n, p = self.size()
        newMatrix = Matrix.empty((n, p))
        for i in range(n):
            for j in range(p):
                newMatrix[i, j] = self[i, j] + m[i, j]
        return newMatrix
    
    def __iadd__(self, m):
        if self.size() != m.size():
            raise ValueError("both matrix has to be of the same size")
        n, p = self.size()
        for i in range(n):
            for j in range(p):
                self[i, j] += m[i, j]
        return self
    
    def __iter__(self):
        self._iterIndex = (0, 0)
        return self
    
    def __next__(self):
        i, j = self._iterIndex
        n, p = self.size()
        if i+1 >= n:
            self._iterIndex = (0, j+1)
        else:
            self._iterIndex = (i+1, j)
        if self._iterIndex[1] >= p:
            raise StopIteration
        return self[i, j]

    def __repr__(self):
        return self._matrix.__repr__()

    def __str__(self):
        s = "["
        n, p = self.size()
        for i in range(n-1):
            s += str(self._matrix[i]) + "\n "
        s += str(self._matrix[n-1]) + "]"
        return s

    
    @staticmethod
    def zeros(size: tuple[int, int]):
        """
        Creates a matrix full of zeros

        :param size: the size of the matrix: first the number of columns, second the number of rows
        :type size: tuple[int, int]
        """
        return Matrix([[0 for i in range(size[1])] for j in range(size[0])])


    @staticmethod
    def empty(size: tuple[int, int]):
        """
        Creates a matrix full of empty strings

        :param size: the size of the matrix: first the number of columns, second the number of rows
        :type size: tuple[int, int]
        """
        return Matrix([[str() for i in range(size[1])] for j in range(size[0])])


    @staticmethod
    def xor(m1, m2):
        """
        Applies a XOR function between the 2 matrix

        :param Matrix m1: the first matrix
        :param Matrix m2: the second matrix
        """
        if m1.size() != m2.size():
            raise ValueError("both matrix has to be of the same size")
        n, p = m1.size()
        newMatrix = Matrix.empty((n, p))
        for i in range(n):
            for j in range(p):
                newMatrix[i, j] = xor(m1[i, j], m2[i, j])
        return newMatrix
    

    @staticmethod
    def strToHex(m, alreadyHex=True):
        """
        Converts a str Matrix into an Hexadecimal matrix.

        :param Matrix m: the matrix to convert
        :param bool alreadyHex: if the string already are thenhexadecimal values. Default True
        """
        for i in range(m.size()[0]):
            for j in range(m.size()[1]):
                if alreadyHex:
                    h = Hexadecimal()
                    h.s = m[i, j]
                else:
                    h = Hexadecimal(m[i, j])
                m[i, j] = h
    

    @staticmethod
    def listToMatrix(l: list, column=True):
        """
        Creates a matrix from a list.

        :param list l: the list
        :param bool column: True if the matrix is a column, False for a row. True by default.
        :return: the matrix
        :rtype: Matrix
        """
        n = len(l)
        size = (n, 1) if column else (1, n)
        newMatrix = Matrix.empty(size)
        if column:
            newMatrix.setColumn(0, l)
        else:
            newMatrix.setRow(0, l)
        return newMatrix
    

    @staticmethod
    def matrixToStr(m) -> str:
        h = Hexadecimal() if type(self[0, 0]) == Hexadecimal else str()
        for x in m:
            h += x
        return h


    @staticmethod
    def strToMatrix(s):
        """
        Transforms string-like object into a matrix. Has to be 128 bits long here.

        :param s: the string, 128 bits long
        :type s: a string-link object
        :return: the matrix of the string
        :rtype: list[list[str]]
        """
        size = int(math.sqrt(len(s)))
        matrix = Matrix.empty((size, size))
        for i in range(len(s)):
            matrix[i%size, i//size] = s[i]
        return matrix




def hexToBin(s: Hexadecimal) -> str:
    if type(s) != Hexadecimal:
        raise ValueError("s has to be an Hexadecimal")
    return bin(int(s.__repr__(), 16))[2:].zfill(len(s)*8) # bin() returns "0bxx", and zfill(8) fills with zeros until it is 8 digits long



def binaryToHex(s: str) -> Hexadecimal:
    if type(s) != str:
        raise ValueError("s has to be a string")
    hexa = Hexadecimal()
    hexa.s = hex(int(s, 2))[2:]
    return hexa



def xor(h1: Hexadecimal, h2: Hexadecimal) -> Hexadecimal:
    """
    Applies a XOR function between two hexadecimal strings.

    :param Hexadecimal h1: the first hexadecimal string
    :param Hexadecimal h1: the first hexadecimal string
    :return: the XOR hexadecimal string
    :rtype: Hexadecimal
    """
    if len(h1) != len(h2):
        raise ValueError("both hexa strings have to be of the same length")
    b1 = hexToBin(h1)
    b2 = hexToBin(h2)
    newBin = str()
    for i in range(len(b1)):
        newBin += '0' if b1[i] == b2[i] else '1'
    newHex = Hexadecimal()
    newHex.s = hex(int(newBin, 2))[2:].zfill(2)
    return newHex












# =================================================
# =============== The AES algorithm ===============
# =================================================


# The S-Box used in the AES algorithm
# ========== DO NOT MODIFY ==========
S_BOX = Matrix([
    ["63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
    ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
    ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
    ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
    ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
    ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
    ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
    ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
    ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
    ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
    ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
    ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
    ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
    ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
    ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
    ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]
])
Matrix.strToHex(S_BOX)

# The matrix used in the mix-columns function of the AES algorithm
# ========== DO NOT MODIFY ==========
MIX_COLUMNS_MATRIX = Matrix([
    ["02", "03", "01", "01"],
    ["01", "02", "03", "01"],
    ["01", "01", "02", "03"],
    ["03", "01", "01", "02"]
])
Matrix.strToHex(MIX_COLUMNS_MATRIX)

# The matrix used in the expand-key function of the AES algorithm
# ========== DO NOT MODIFY ==========
RCON = Matrix([
    ["01", "02", "04", "08", "10", "20", "40", "80", "1b", "36"],
    ["00", "00", "00", "00", "00", "00", "00", "00", "00", "00"],
    ["00", "00", "00", "00", "00", "00", "00", "00", "00", "00"],
    ["00", "00", "00", "00", "00", "00", "00", "00", "00", "00"]
])
Matrix.strToHex(RCON)






def expandKeyMod4Column(columnIndex: int, allKeysMatrix: Matrix):
    """
    Applies the expand-key algorithm to a column which index is 0 modulo 4.
    """
    n = allKeysMatrix.size()[0]
    newColumn = Matrix.empty((n, 1))
    newColumn.setColumn(0, allKeysMatrix.getColumn(columnIndex-1))
    
    # RotWord : applies a rotation on the column
    c = newColumn.getColumn(0)
    c.append(c.pop(0))
    newColumn.setColumn(0, c)
    
    # SubBytes
    subBytes(newColumn)
    previousColumn = Matrix.listToMatrix(allKeysMatrix.getColumn(columnIndex-n))
    firstXOR = Matrix.xor(
        previousColumn,
        newColumn
    )
    newColumn = Matrix.xor(
        firstXOR,
        Matrix.listToMatrix(RCON.getColumn((columnIndex-1)//n))
    )
    allKeysMatrix.setColumn(columnIndex, newColumn.getColumn(0))



def expandKeyNotMod4Column(columnIndex: int, allKeysMatrix: Matrix):
    """
    Applies the expand-key algorithm to the columns which index is not 0 modulo 4.
    """
    columnsXOR = Matrix.xor(
        Matrix.listToMatrix(allKeysMatrix.getColumn(columnIndex-1)),
        Matrix.listToMatrix(allKeysMatrix.getColumn(columnIndex-4))
    )
    allKeysMatrix.setColumn(columnIndex, columnsXOR.getColumn(0))



def expandKey(keyMatrix: Matrix) -> list[Matrix]:
    n = keyMatrix.size()[0]
    allKeysMatrix = Matrix.empty((n, n*11))
    for i in range(n):
        c = keyMatrix.getColumn(i)
        allKeysMatrix.setColumn(i, c)
    for i in range(n, n*11):
        if i % 4 == 0:
            expandKeyMod4Column(i, allKeysMatrix)
        else:
            expandKeyNotMod4Column(i, allKeysMatrix)
    allKeys = [Matrix.empty((n, n)) for i in range(11)]
    for i in range(n*11):
        allKeys[i//n].setColumn(
            i%n,
            allKeysMatrix.getColumn(i)
        )
    return allKeys





def subBytes(m: Matrix) -> None:
    """
    Performs the sub-bytes operation in the AES algorithm on the given matrix.

    :param m: the matrix to perform the sub-bytes to
    :type m: Matrix of Hexadecimal values
    """
    n, p = m.size()
    for i in range(n):
        for j in range(p):
            x = int(m[i, j].s[0], 16)
            y = int(m[i, j].s[1], 16)
            m[i, j] = S_BOX[x, y]



def shiftRows(m: Matrix) -> None:
    """
    Performs the shift-rows operation in the AES algorithm on the given matrix.

    :param m: the matrix to rotate the rows
    :type m: Matrix
    """
    n, p = m.size()
    for i in range(n):
        for j in range(i):
            m.shiftRow(i)



def mixColumns(m: Matrix):
    """
    Performs the mix-columns function of the AES algorithm on the given matrix.
    cf. https://en.wikipedia.org/wiki/Rijndael_MixColumns
    Can use pre-calculated tables (search on internet).

    :param Matrix m: the matrix to mix the columns
    """



def addRoundKey(m: Matrix, key: Matrix) -> None:
    """
    Performs the round-keys function of the AES algorithm on the given matrix.

    :param Matrix m: the matrix to apply the key to
    :param Matrix key: the key to apply
    """
    m._matrix = Matrix.xor(m, key)._matrix



def AESRound(stateMatrix: Matrix, subKey: Hexadecimal):
    subBytes(stateMatrix)
    shiftRows(stateMatrix)
    mixColumns(stateMatrix)
    addRoundKey(stateMatrix, subKey)



def AESOn128BitsData(data: Hexadecimal, key: Hexadecimal) -> Hexadecimal:
    # Convert str to Matrix
    allSubKeys = expandKey(Matrix.strToMatrix(key))
    stateMatrix = Matrix.strToMatrix(data)
    
    # Initial round
    addRoundKey(stateMatrix, allSubKeys[0])
    
    # 9 main rounds
    for i in range(1, 10):
        AESRound(stateMatrix, allSubKeys[i])
    
    # Final round
    subBytes(stateMatrix)
    shiftRows(stateMatrix)
    addRoundKey(stateMatrix, allSubKeys[-1])

    # Convert Matrix to str
    return Matrix.matrixToStr(stateMatrix)











if __name__ == "__main__":
    m = Matrix([
        ["04", "e0", "48", "58"],
        ["66", "cb", "f8", "06"],
        ["81", "19", "d3", "26"],
        ["e5", "9a", "7a", "4c"]
    ])
    Matrix.strToHex(m)
    key = Matrix([
        ["2b", "28", "ab", "09"],
        ["7e", "ae", "f7", "cf"],
        ["15", "d2", "15", "4f"],
        ["16", "a6", "88", "3c"]
    ])
    Matrix.strToHex(key)
    AESOn128BitsData(m, key)

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import struct
import hashlib

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import QtWidgets
import os
import sys
from struct import *
import sys
from PyQt5.QtCore import qDebug
# Press the green button in the gutter to run the script.
import untitled
import mainwindow
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
last_size = 0
last_addr = 0
cur_size = 0
cur_addr = 0
high_addr = 0
expand_f = 0
bin_buff = []
bin_file = ''
cnt = 0
hsm_boot_start_addr = 0x80010000
# file_path: str = "./"
file_path = 'D:/'


class MyMainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    global cnt

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.select_hex_file.clicked.connect(self.select_hex_file_slot)
        self.clear.clicked.connect(self.slot_create_array)
        self.create_signature_without_key.clicked.connect(self.slot_create_signature_without_key)
        self.create_bin2hash.clicked.connect(self.slot_create_SHA256_Hash)
        # self.create_signature_using_key.clicked.connect(self.slot_create_signature_using_key)

    # def slot_create_signature_using_key(self):

    def slot_create_signature_without_key(self):
        global file_path

        curve = ec.SECP256R1()
        signature_algorithm = ec.ECDSA(hashes.SHA256())
        sender_private_key = ec.generate_private_key(curve, default_backend())
        sender_public_key = sender_private_key.public_key()

        print(hex(sender_public_key.public_numbers().x))
        print(hex(sender_public_key.public_numbers().y))
        print(hex(sender_private_key.private_numbers().private_value))
        # temp = '\n' + '私钥为:' + hex(sender_private_key)
        # self.textEdit.insertPlainText(temp)
        data = b"this is some  data  to sign"
        for index, item in enumerate(bin_buff):
            bin_buff[index] = int.from_bytes(item, 'big')
        print('bin_buff %s' % type(bin_buff))
        temp = bytes(bin_buff)
        print(temp)
        signature = sender_private_key.sign(temp, signature_algorithm)
        print('Signature: 0x%s' % signature.hex())
        signature_display = '\n' + 'Signature: 0x%s' % signature.hex()
        self.textEdit.insertPlainText(signature_display)
        print(len(signature))
        # signature1 = b'abcdefghijklmnopqrstuvwxyzabcedfghijklmnopqrstuvwxyz12345678901234567890'
        # signature1 =0x30460221009426e507d78d3cb9e9de3f1341d72c8ad7154bfa50fb6564594b7fe440e7cc1a022100ce529e6b11f304ee12c2d713c6bebe006b079c9dc4a2dea76776559478a64a11
        try:
            sender_public_key.verify(signature, temp, signature_algorithm)
            print('Verification OK')
        except InvalidSignature:
            print('Verification failed')

    def select_hex_file_slot(self):
        file_name_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                 "选取文件",
                                                                 "./",
                                                                 "Hex Files (*.hex);;hex Files (*.hex)",
                                                                 "hex文件(*.hex)")  # 设置文件扩展名过滤,
        # 用双分号间隔

        if file_name_choose == "":
            print("\n取消选择")
            return
        else:
            file_path = file_name_choose
            print("file_path %s" % file_path)
            self.textEdit.insertPlainText(file_name_choose + '\n')
            # self.textEdit.insertPlainText(str(cnt))

        hex_bin(file_name_choose, file_name_choose[:-4] + '.bin', self)
        # hex2bin(file_name_choose, file_name_choose[:-4]+'.bin')
        # hex2bin.wr_bin(hex2bin.bin_file_name)

        print("\n你选择的文件为:")
        print(file_name_choose)
        print("文件筛选器类型: ", filetype)

    def slot_create_array(self) -> None:
        global bin_file
        out_file = bin_file[:-4] + '.txt'
        fin = open(bin_file, 'rb')
        fin.seek(0, os.SEEK_END)
        size = fin.tell()
        fin.seek(0, os.SEEK_SET)
        fout = open(out_file, 'w')
        fout.truncate()
        fout.seek(0, 0)

        fout.write("const uint8 boot_data={ \\")
        for i in range(size):
            if i % 16 != 0:
                temp = "0x%.2x" % ord(fin.read(1))
                fout.write(temp + ',')
            else:
                fout.write('\n')
                temp = "0x%.2x" % ord(fin.read(1))
                fout.write(temp + ',')
        fout.write("};")

        fin.close()
        fout.close()

        self.textEdit.insertPlainText('\n' + "已生成C标准数组，存入文件" + out_file)

        # print("'0x' + str(fin.read(1), 16")
        # print(temp)

    def slot_create_SHA256_Hash(self):
        global file_path
        print("file_path = %s" % file_path)
        temp = bytes(bin_buff)
        s = hashlib.sha256()
        s.update(temp)
        b = s.hexdigest()
        print(len(bin_buff))
        print(b)
        print(file_path)
        # file = open('D:/C++/SecIC_Hsm_boot.hex'[:-4] + '1.bin', 'wb')
        file = open(bin_file[:-4] + '1.bin', 'wb')
        for item in bin_buff:
            s = struct.pack('B', item)
            file.write(s)
        file.close()


# intel-hex 格式
#:LLAAAARRDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDZZ
# LL——长度,单位，byte
# AAAA——16 bit 地址
# RR——类型
# - 00 数据记录 (data record)
# - 01 结束记录 (end record)
# - 02 扩展段地址记录 (paragraph record)
# - 03 转移地址记录 (transfer address record)
# - 04 扩展线性地址记录 (expand address record)
# DD——16byte数据
# ZZ——校验


def hex_bin(hexfile, binfile, myWin: MyMainWindow):
    global bin_buff
    global cnt
    global bin_file
    global hsm_boot_start_addr
    bin_buff.clear()
    cnt = 0
    bin_file = binfile
    fin = open(hexfile)
    fout = open(binfile, 'wb')
    result = ''
    for hexstr in fin.readlines():
        hexstr = hexstr.strip()
        size = int(hexstr[1:3], 16)
        if int(hexstr[7:9], 16) != 0:
            continue
            # end if
        for h in range(0, size):
            b = int(hexstr[9 + h * 2:9 + h * 2 + 2], 16)
            result = pack('B', b)
            # end if
            cnt = cnt + 1
            bin_buff.append(result)
            fout.write(result)
            result = ''

    temp = [int.from_bytes(bin_buff[516], 'big'),
            int.from_bytes(bin_buff[517], 'big'),
            int.from_bytes(bin_buff[518], 'big'),
            int.from_bytes(bin_buff[519], 'big')]
    # print(temp[0])
    # print(type((bin_buff[516]).to_byes(length=1,byteorder='little')))
    temp1 = bytes(temp)
    # print(type(0x12))
    # print(bin_buff[516], bin_buff[517], bin_buff[518], bin_buff[519])
    # print(temp1)
    addr_tuple = struct.unpack('<I', temp1)
    hsm_boot_epilog_addr = int(addr_tuple[0])
    total_size_from_begin = int(hsm_boot_epilog_addr) - hsm_boot_start_addr + 16
    print(hsm_boot_epilog_addr)
    print(type(hsm_boot_start_addr))
    print("0x%x" % int(hsm_boot_epilog_addr))

    bin_buff = bin_buff[0:total_size_from_begin]
    bin_buff = bin_buff[0x100:total_size_from_begin]
    # print(type(temp))
    # print(int.from_bytes(bin_buff[516]))
    # print(type(temp2[0]))
    # print(hex(temp2))
    # del bin_buff[:0x100]
    # end for
    fin.close()
    fout.close()
    myWin.textEdit.insertPlainText(str(cnt))
    print(len(bin_buff))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

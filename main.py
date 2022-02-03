# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import struct

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
from cryptography.hazmat.primitives.asymmetric import ec

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


class MyMainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    file_path: str = "./"
    global cnt

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.select_hex_file.clicked.connect(self.select_hex_file_slot)
        self.clear.clicked.connect(self.slot_create_array)

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
        # print("'0x' + str(fin.read(1), 16")
        # print(temp)

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
    # hash_end_addr = struct.unpack('I', bin_buff[516:520])
    # print("hash_end_addr=%x" % hash_end_addr)
    # hash_end_addr = bin_buff[516:520]
    # temp = bytes(bin_buff[516:520])
    # temp = [bin_buff[516].encode(), bin_buff[517].encode(), bin_buff[518].encode(), bin_buff[519].encode()]
    # temp = [0x12, 0x34, 0x56, 0x78]
    # temp = [int.from_bytes(bin_buff[516]), int.from_bytes(bin_buff[517]), int.from_bytes(bin_buff[518]),
    #         int.from_bytes(bin_buff[519])]
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

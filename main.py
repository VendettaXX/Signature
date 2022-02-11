# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import struct
import hashlib
import tkinter.filedialog

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
hsm_app_start_addr = 0x80018000
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
        self.create_signature_using_key.clicked.connect(self.slot_create_signature_using_key)
        # self.create_bin2hash.setVisible(False)

    def slot_create_signature_using_key(self):
        global bin_buff
        global bin_file

        print("1111111111111111111111 %d" % len(bin_buff))
        private_value = int(self.private_key.text(), 16)
        value = 0x63bd3b01c5ce749d87f5f7481232a93540acdb0f7b5c014ecd9cd32b041d6f33
        # value = 0xE353637894118B8691A17B51C300A65CC85DCAF4A04935181E979F2F9A1301B1
        # print('private_value %s ' % type(private_value))
        curve = ec.SECP256R1()
        signature_algorithm = ec.ECDSA(hashes.SHA256())
        # private_key_test = ec.derive_private_key(value, curve, default_backend())
        # public_key_test = private_key_test.public_key()
        # print(hex(public_key_test.public_numbers().x))
        # print(hex(public_key_test.public_numbers().y))

        priv_key = ec.derive_private_key(private_value, curve, default_backend())
        public_key = priv_key.public_key()
        data = b"this is some  data  to sign"
        bin_buff_new = [0] * len(bin_buff)
        for index, item in enumerate(bin_buff):
            bin_buff_new[index] = int.from_bytes(item, 'big')
        print('bin_buff %s' % type(bin_buff))
        temp = bytes(bin_buff_new)
        # print(temp)
        signature = priv_key.sign(temp, signature_algorithm)
        print('Signature: 0x%s' % signature.hex())
        print('lenof signature=%d' % len(signature))
        # for iter in signature:
        #     print(hex(iter))
        #     self.textEdit.insertPlainText(hex(iter) + ',')

        try:
            public_key.verify(signature, temp, signature_algorithm)
            print('Verification OK')
        except InvalidSignature:
            print('Verification failed')

        out_file = bin_file[:-5] + 's' + '.txt'
        fout = open(out_file, 'w')
        fout.truncate()
        fout.seek(0, 0)

        fout.write("#define MEMLAY_IB_DUMMY_SIGNATURE { \\")
        for iter in range(4, 256):
            if len(signature) <= iter < 256:
                if iter % 16 != 0:
                    fout.write("0x00,")
                else:
                    fout.write('\n')
                    fout.write('0x00,')
            elif iter < len(signature):
                if iter % 16 != 0:
                    temp = "0x%.2x" % signature[iter]
                    fout.write(temp + ',')
                else:
                    fout.write('\n')
                    temp = "0x%.2x" % signature[iter]
                    fout.write(temp + ',')
            elif iter > 256:
                break
            else:
                pass
            iter = iter + 1
        fout.write("}")

        fout.close()

    # def slot_create_signature_using_key(self):

    def slot_create_signature_without_key(self):
        global file_path

        curve = ec.SECP256R1()
        signature_algorithm = ec.ECDSA(hashes.SHA256())
        sender_private_key = ec.generate_private_key(curve, default_backend())
        sender_public_key = sender_private_key.public_key()

        print(hex(sender_public_key.public_numbers().x))
        print(hex(sender_public_key.public_numbers().y))
        # print(hex(sender_private_key.public_key()))
        print(hex(sender_private_key.private_numbers().private_value))
        # print(hex(sender_private_key.private_numbers().private_key()))

        print(hex(sender_private_key.private_numbers().private_value))
        self.textEdit.insertPlainText('\n' + '私钥为:' + '\n' + hex(sender_private_key.private_numbers().private_value))

        data = b"this is some  data  to sign"
        print("1111111111111111111111 %d" % len(bin_buff))

        bin_buff_new = [0] * len(bin_buff)
        for index, item in enumerate(bin_buff):
            bin_buff_new[index] = int.from_bytes(item, 'big')
        print('bin_buff %s' % type(bin_buff))
        temp = bytes(bin_buff_new)
        print(temp)
        signature = sender_private_key.sign(temp, signature_algorithm)
        print('Signature: 0x%s' % signature.hex())
        signature_display = '\n' + '签名为: 0x%s' % signature.hex()
        # self.textEdit.insertPlainText('\n'+'签名为:'+signature.hex())
        # print('\n'+'hello')
        self.textEdit.insertPlainText(signature_display)
        # print('hello world:0x%d' % signature[0])
        # print(len(signature))
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

        # fout.write("const uint8 boot_data={ \\")
        # SecICHsm_SecuFlash_Boot_BlockData[SECICHSM_SECUFLASH_HSM_BOOT_LEN] =
        if bin_file.find('boot') != -1:
            fout.write("#include \"SecICHsm_SrvTypes.h\" " + '\n')
            fout.write("#include \"SecICHsm_SecuFlash_test.h\"" + '\n')
            fout.write("const uint8 SecICHsm_SecuFlash_Boot_BlockData[SECICHSM_SECUFLASH_HSM_BOOT_LEN] = {\\")
        else:
            fout.write("#include \"SecICHsm_SrvTypes.h\" " + '\n')
            fout.write("#include \"SecICHsm_SecuFlash_test.h\"" + '\n')
            fout.write("const uint8 SecICHsm_SecuFlash_App_BlockData[SECICHSM_SECUFLASH_HSM_APP_LEN] = {\\")

        for i in range(size):
            if i % 32 != 0:
                temp = "0x%.2X," % ord(fin.read(1))
                fout.write(temp + ' ')
            else:
                fout.write('\n')
                fout.write(' ' + ' ' + ' ' + ' ')
                temp = "0x%.2X," % ord(fin.read(1))
                fout.write(temp + ' ')
        fout.write("};")

        fin.close()
        fout.close()

        self.textEdit.insertPlainText('\n' + "已生成C标准数组，存入文件" + out_file)

        # print("'0x' + str(fin.read(1), 16")
        # print(temp)

    def slot_create_SHA256_Hash(self):
        global bin_buff
        global file_path
        # print("file_path = %s" % file_path)
        bin_buff_hash = []

        for item in bin_buff:
            bin_buff_hash.append(int.from_bytes(item, 'big'))

        temp = bytes(bin_buff_hash)
        s = hashlib.sha256()
        s.update(temp)
        b = s.hexdigest()
        self.textEdit.insertPlainText('\n' + 'hash=' + b)
        # print(len(bin_buff))
        # print(b)
        # print(file_path)
        # file = open('D:/C++/SecIC_Hsm_boot.hex'[:-4] + '1.bin', 'wb')
        # file = open(bin_file[:-4] + '1.bin', 'wb')
        # for item in bin_buff:
        #     s = struct.pack('B', item)
        #     file.write(s)
        # file.close()

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
    global hsm_app_start_addr
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
        for h in range(0, size):
            b = int(hexstr[9 + h * 2:9 + h * 2 + 2], 16)
            result = pack('B', b)
            cnt = cnt + 1
            bin_buff.append(result)
            fout.write(result)
            result = ''
    if bin_file.find('boot') != -1:
        temp = [int.from_bytes(bin_buff[516], 'big'),
                int.from_bytes(bin_buff[517], 'big'),
                int.from_bytes(bin_buff[518], 'big'),
                int.from_bytes(bin_buff[519], 'big')]
    else:
        temp = [int.from_bytes(bin_buff[260], 'big'),
                int.from_bytes(bin_buff[261], 'big'),
                int.from_bytes(bin_buff[262], 'big'),
                int.from_bytes(bin_buff[263], 'big')]
    temp1 = bytes(temp)
    addr_tuple = struct.unpack('<I', temp1)
    hsm_boot_epilog_addr = int(addr_tuple[0])
    if bin_file.find('boot') != -1:
        total_size_from_begin = int(hsm_boot_epilog_addr) - hsm_boot_start_addr + 16
    else:
        total_size_from_begin = int(hsm_boot_epilog_addr) - hsm_app_start_addr + 16
    print(hsm_boot_epilog_addr)
    print(type(hsm_boot_start_addr))
    print("0x%x" % int(hsm_boot_epilog_addr))
    if bin_file.find('boot') != -1:
        bin_buff = bin_buff[0:total_size_from_begin]
        bin_buff = bin_buff[0x100:total_size_from_begin]
    else:
        bin_buff = bin_buff[0:total_size_from_begin]
    fin.close()
    fout.close()
    myWin.textEdit.insertPlainText('文件共' + str(cnt) + "字节")
    print(len(bin_buff))

    bin_file_hash = bin_file[:-5] + '.bin1'
    file = open(bin_file_hash, 'wb')
    for ele in bin_buff:
        file.write(ele)
    file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

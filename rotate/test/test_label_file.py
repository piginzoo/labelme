import unittest,os
from common.file import AssignFileProcessor,LabelDoneProcessor,ReadFile
from common import utils
class TestDict(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        utils.init_logger()

    def read(self,path):
        with open(path) as f:
            lines = f.readlines()
        return lines

    def setUp(self):
        self.file_path = "label_test.txt"
        self.file = open(self.file_path,"w")
        self.line_num = 100
        for i in range(self.line_num):
            self.file.write("data/images/{}.png".format(i))
            self.file.write("\n")
        self.file.close()
        print("创建了测试文件")

    # def test_a(self):
    #     pass

    def tearDown(self):
        pass
        #os.remove(self.file_path)

    def test_read_oneline(self):
        fp = ReadFile(self.file_path)
        line,num = fp.read_one_line()
        self.assertEquals("data/images/0.png",line)
        self.assertEquals(self.line_num - 1, num)

    # 测试，如果只取10行，源文件
    def test_assign_file_processor(self):
        dst_file_path="test_dst.txt"
        fp1 = AssignFileProcessor(src_path=self.file_path,dst_path=dst_file_path,assign_num=10)
        fp1.process()
        dst_lines = self.read(dst_file_path)

        self.assertEquals(10,len(dst_lines))
        src_lines=self.read(self.file_path)

        self.assertEquals(self.line_num - 10, len(src_lines))

    # 测试，如果大于源文件行数，那么源文件会被取空
    def test_assign_file_processor_too_much(self):
        dst_file_path = "test_dst.txt"
        fp1 = AssignFileProcessor(src_path=self.file_path, dst_path=dst_file_path, assign_num=self.line_num+10)
        fp1.process()
        dst_lines = self.read(dst_file_path)
        self.assertEquals(self.line_num, len(dst_lines))
        src_lines = self.read(self.file_path)
        self.assertEquals(0, len(src_lines))

    # def test_update_label_file(self):
    #     lf = LabelFile(self.file_path,"data/images/0.png","90")
    #     lf.process()

if __name__ == '__main__':
    unittest.main()
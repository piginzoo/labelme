import unittest,os
from commons.file import AssignFileProcessor,LabelDoneProcessor,ReadFile
from commons import utils
class TestDict(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        utils.init_logger()

    def read(self,path):
        with open(path) as f:
            lines = f.readlines()
        return lines

    def setUp(self):
        self.label_path = "label.txt"
        self.label_file = open(self.label_path,"w")
        self.label_num = 100
        for i in range(self.label_num):
            self.label_file.write("data/images/{}.png".format(i))
            self.label_file.write("\n")
        self.label_file.close()
        print("创建了标注文件")

        self.done_path = "done.txt"
        self.done_file = open(self.done_path,"w")
        self.done_num = 33
        for i in range(self.label_num,self.label_num + self.done_num):
            self.done_file.write("data/images/{}.png".format(i))
            self.done_file.write("  270")
            self.done_file.write("\n")
        self.done_file.close()
        print("创建了标注完成done文件")

    # def test_a(self):
    #     pass

    def tearDown(self):
        pass
        #os.remove(self.label_path)

    def test_read_oneline(self):
        fp = ReadFile(self.label_path)
        line,num = fp.read_one_line()
        self.assertEquals("data/images/{}.png".format(self.label_num-1),line)
        self.assertEquals(self.label_num - 1, num)

    # 测试，如果只取10行，源文件
    def test_assign_file_processor(self):
        dst_label_path="done.txt"
        fp1 = AssignFileProcessor(src_path=self.label_path,dst_path=dst_label_path,assign_num=10)
        fp1.process()
        dst_lines = self.read(dst_label_path)

        self.assertEquals(10,len(dst_lines))
        src_lines=self.read(self.label_path)

        self.assertEquals(self.label_num - 10, len(src_lines))

    # 测试，如果大于源文件行数，那么源文件会被取空
    def test_assign_file_processor_too_much(self):
        dst_label_path = "done.txt"
        fp1 = AssignFileProcessor(src_path=self.label_path, dst_path=dst_label_path, assign_num=self.label_num+10)
        fp1.process()
        dst_lines = self.read(dst_label_path)
        self.assertEquals(self.label_num, len(dst_lines))
        src_lines = self.read(self.label_path)
        self.assertEquals(0, len(src_lines))

    def test_rollback(self):
        ldp = LabelDoneProcessor(src_path=self.done_path,dst_path=self.label_path)
        ldp.rollback()
        self.assertEquals(self.label_num+1,len(self.read(self.label_path)))
        self.assertEquals(self.done_num -1,len(self.read(self.done_path)))

        ldp.rollback()
        self.assertEquals(self.label_num+2,len(self.read(self.label_path)))
        self.assertEquals(self.done_num -2,len(self.read(self.done_path)))

        ldp.rollback()
        self.assertEquals(self.label_num+3,len(self.read(self.label_path)))
        self.assertEquals(self.done_num -3,len(self.read(self.done_path)))


if __name__ == '__main__':
    unittest.main()
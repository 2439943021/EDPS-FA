import os
import shutil


def del_file(path):
    """
    文件删除
    @param path:
    @return:
    """
    if not os.listdir(path):
        return
    else:
        for i in os.listdir(path):
            path_file = os.path.join(path, i)  # 取文件绝对路径
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                del_file(path_file)
                shutil.rmtree(path_file)

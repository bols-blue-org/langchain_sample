import os

# ディレクトリ内のすべてのファイルに対して処理をするためのクラスを作成するユーティリティ関数
def file_loader(path):
    files = os.listdir(path)
    classes = []
    for name in files:
        classes.append(FilePath(os.path.join(path, name)))
    return classes


class FilePath:
    def __init__(self, path):
        self.absolute_path = os.path.abspath(path)
        self.directory, self.filename = os.path.split(path)  # パスをディレクトリとファイル名に分割
        self.name, self.extension = os.path.splitext(self.filename)  # ファイル名を名称と拡張子に分割

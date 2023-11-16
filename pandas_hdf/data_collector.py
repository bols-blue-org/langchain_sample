import pandas as pd


class HDFDataProcessor:
    def __init__(self, existing_file_path, key='data'):
        self.file_path = existing_file_path
        self.key = key

        # 既存のHDFデータを読み込み
        try:
            self.existing_data = pd.read_hdf(self.file_path)
        except FileNotFoundError as e:
            print(e)
            self.existing_data = None

    def is_duplicate(self, record, key):
        if self.existing_data is None:
            return False
        data = self.existing_data[key]
        index = self.find_index(data, record)
        if index is None:
            return False
        else:
            return True

    # 案2
    def find_index(self, data, item):
        match_items = data[data == item]
        if match_items.empty:
            return None
        return match_items.index[0]

    def add_record(self, new_record):
        if self.existing_data is None:
            self.existing_data = pd.DataFrame([new_record])  # データが存在しない場合は空のDataFrameを作成
        else:
            self.existing_data = pd.concat([self.existing_data, pd.DataFrame([new_record])])

    def save_file(self):
        # 4. 更新されたデータをHDF形式で保存
        self.existing_data.to_hdf(self.file_path, key=self.key, mode='w')
        print("データが正常に追加されました。")


# クラスの使用例
if __name__ == "__main__":
    existing_file_path = 'existing_data.h5'
    processor = HDFDataProcessor(existing_file_path, key='column2')

    if not processor.is_duplicate(123, "column2"):
        # 追加する新しいレコードのデータを作成
        new_record = {
            'column1': 'Value1',
            'column2': 123,
            'column3': 4.56
        }
        # 新しいレコードを追加して保存
        processor.add_record(new_record)

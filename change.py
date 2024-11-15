import pandas as pd

class CoordinateFormatter:
    def __init__(self, x_coords, y_coords, z_coords, identifier):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.z_coords = z_coords
        self.identifier = identifier

    def format_coordinates(self):
        identifier_map = {
            'P150A': '1',
            'DS18(Fc24)': '2',
            'RG12': '3',
            '7C11': '4',
            'F21A': '5',
            'F41A': '6',
            'F22A': '7',
            'SB30': '8',
            'F31A': '9',
            'F51A': '0'
        }
        formatted_string = identifier_map.get(self.identifier, "")
        if not formatted_string:
            return ""

        previous_z = None
        for x, y, z in zip(self.x_coords, self.y_coords, self.z_coords):
            if previous_z is not None and z != previous_z:
                formatted_string += "\n" + identifier_map.get(self.identifier, "")
            formatted_string += f" {x} {y}"
            previous_z = z
        return formatted_string.strip()  # 最後の改行を削除

# CSVファイルのパスを指定
csv_path = 'C:/yolov8/bim/main_zahyou.csv'

# CSVファイルの読み込み
data = pd.read_csv(csv_path)

# 識別子列の取得（例: 第2列、0ベースで1番目）
identifiers = data.iloc[:, 1].str.strip()  # 前後の空白を削除

# x座標とy座標とz座標の取得
x_coords = data.iloc[:, 2]  # x座標列（0ベースで2番目の列）
y_coords = data.iloc[:, 3]  # y座標列（0ベースで3番目の列）
z_coords = data.iloc[:, 0]   # z座標列（0ベースで0番目の列）

# 出力用の文字列を初期化
output_strings = []

# 各行について処理
previous_identifier = None
previous_z = None
formatted_string = ""

for identifier, x, y, z in zip(identifiers, x_coords, y_coords, z_coords):
    header = {
        'P150A': '1',
        'DS18(Fc24)': '2',
        'RG12': '3',
        '7C11': '4',
        'F21A': '5',
        'F41A': '6',
        'F22A': '7',
        'SB30': '8',
        'F31A': '9',
        'F51A': '0'
    }.get(identifier, "")

    if header == "":
        continue

    if identifier != previous_identifier:
        if formatted_string:
            output_strings.append(formatted_string)
        formatted_string = header
        previous_z = None
    if previous_z is not None and z != previous_z:
        output_strings.append(formatted_string)
        formatted_string = header
    formatted_string += f" {x} {y}"
    previous_z = z
    previous_identifier = identifier

if formatted_string:
    output_strings.append(formatted_string)

# テキストファイルに保存
output_file_path = 'C:/yolov8/bim/z.txt'
with open(output_file_path, 'w') as file:
    file.write("\n".join(output_strings))

print(f"Formatted coordinates have been saved to {output_file_path}")

# デバッグ情報の表示
print(f"Total lines processed: {len(output_strings)}")
print(f"Total lines in Excel: {len(data)}")

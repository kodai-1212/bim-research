import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('C:/yolov8/bim/beams_geometry.csv')

# 出力ファイル
output_file = '00.txt'

# Group by 'Element ID'と'Name'
grouped = df.groupby(['Element ID', 'Name'])

# 中点、幅、高さを計算する関数
def calculate_properties(group):
    x_coords = group['X']
    y_coords = group['Y']
    midpoint_x = (x_coords.min() + x_coords.max()) / 2
    midpoint_y = (y_coords.min() + y_coords.max()) / 2
    width = x_coords.max() - x_coords.min()
    height = y_coords.max() - y_coords.min()
    return pd.Series({'Midpoint_X': midpoint_x, 'Midpoint_Y': midpoint_y, 'Width': width, 'Height': height})

# 各グループに対して計算を適用
results = grouped.apply(calculate_properties).reset_index()

# 出力ファイル作成
with open(output_file, 'w') as f:
    current_id = None
    name_counter = -1
    current_name = None

    for _, row in results.iterrows():
        if row['Element ID'] != current_id:
            f.write('\n')  # Element IDが変わったら改行
            current_id = row['Element ID']
            name_counter = -1  # 新しいElement IDでリセット
            current_name = None

        if row['Name'] != current_name:
            name_counter += 1
            current_name = row['Name']

        f.write(f"{name_counter} {row['Midpoint_X']} {row['Midpoint_Y']} {row['Width']} {row['Height']}")
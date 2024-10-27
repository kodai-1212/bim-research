import pandas as pd

# ファイルパスのリストと対応する最初の数字
file_info = [
    ('C:/yolov8/bim/beams_geometry.csv', 0),
    ('C:/yolov8/bim/columns_geometry.csv', 1)
]

# 出力ファイル
output_file = '01.txt'

# 中点、幅、高さを計算する関数
def calculate_properties(group):
    x_coords = group['X'] * 12 + 600
    y_coords = (3600 - (group['Y'] * 12)) - 600
    midpoint_x = (x_coords.min() + x_coords.max()) / 2
    midpoint_y = (y_coords.min() + y_coords.max()) / 2
    width = x_coords.max() - x_coords.min()
    height = y_coords.max() - y_coords.min()
    return pd.Series({'Midpoint_X': midpoint_x, 'Midpoint_Y': midpoint_y, 'Width': width, 'Height': height})

# 出力ファイル作成
with open(output_file, 'w') as f:
    first_file = True
    
    for file_path, initial_number in file_info:
        df = pd.read_csv(file_path)

        # Group by 'Element ID'と'Name'
        grouped = df.groupby(['Element ID', 'Name'])

        # 各グループに対して計算を適用
        results = grouped.apply(calculate_properties).reset_index()

        if not first_file:  # 最初のファイルではない場合改行追加
            f.write('\n')
        first_file = False 

        current_id = None
        name_counter = initial_number - 1
        current_name = None

        for _, row in results.iterrows():
            if row['Element ID'] != current_id:
                if current_id is not None:
                    f.write('\n')  # Element IDが変わったら改行
                current_id = row['Element ID']
                name_counter = initial_number - 1  # 新しいElement IDでリセット
                current_name = None

            if row['Name'] != current_name:
                name_counter += 1
                current_name = row['Name']

            f.write(f"{name_counter} {row['Midpoint_X']} {row['Midpoint_Y']} {row['Width']} {row['Height']}")
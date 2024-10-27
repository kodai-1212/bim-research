import matplotlib.pyplot as plt

# 出力ファイルからデータを読み込む
with open('01.txt', 'r') as f:
    lines = f.readlines()

# 描画の準備
fig, ax = plt.subplots()

# データ処理と描画
for line in lines:
    line = line.strip()
    if line:  # 空行を無視する
        parts = line.split()
        counter = int(parts[0])
        midpoint_x = float(parts[1])
        midpoint_y = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        # 四角形の左下の座標を計算
        bottom_left_x = midpoint_x - width / 2
        bottom_left_y = midpoint_y - height / 2

        # 四角形を描画
        rectangle = plt.Rectangle((bottom_left_x, bottom_left_y), width, height, fill=None, edgecolor='blue')
        ax.add_patch(rectangle)

# 軸の設定
ax.set_aspect('equal', 'box')
plt.xlim(0, 3600)  # 適切に調整
plt.ylim(0, 3600)  # 適切に調整

# グラフを表示
plt.xlabel('X')
plt.ylabel('Y')
plt.title('hashira-columns_geometry')
plt.grid(True)
plt.savefig("test-columns.png")
plt.show()

import json
from pathlib import Path

# 保存したQテーブルを読み込む
file_path = Path(__file__).parent / "q_table.json"

with open(file_path, "r", encoding="utf-8") as f:
    q_table = json.load(f)

print("=== 保存したQテーブルを読み込みました ===")

# スタートは0、ゴールは4
position = 0
goal = 4
route = [position]

# 学習したQ値を使って行動を選択
for step in range(10):
    left_q, right_q = q_table[position]

    if right_q > left_q:
        action = "右"
        position = min(goal, position + 1)
    else:
        action = "左"
        position = max(0, position - 1)

    print(f"{step + 1}歩目：{action}へ進む")
    route.append(position)

    if position == goal:
        break

print("移動経路：", " → ".join(map(str, route)))

if position == goal:
    print("ゴール到達！")
else:
    print("ゴール未到達")




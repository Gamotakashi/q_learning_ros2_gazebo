
import random

# 5マスの一本道
GOAL = 4
ACTIONS = [-1, 1]  # 左、右

# Qテーブル：各マスで左右どちらが良いかを記録
q_table = [[0.0, 0.0] for _ in range(5)]

alpha = 0.2       # 学習率
gamma = 0.9       # 将来の報酬の重視度
epsilon = 0.3     # ランダムに試す確率

# 1000回練習する
for episode in range(1000):
    position = 0

    for step in range(30):
        # ときどきランダムに行動して探索する
        if random.random() < epsilon:
            action_index = random.randint(0, 1)
        else:
            # Q値が同じ場合もランダムに選ぶ
            best_value = max(q_table[position])
            candidates = [
                i for i, value in enumerate(q_table[position])
                if value == best_value
            ]
            action_index = random.choice(candidates)

        # 左または右に1マス移動
        next_position = position + ACTIONS[action_index]
        next_position = max(0, min(GOAL, next_position))

        # ゴールなら大きな報酬
        reward = 10 if next_position == GOAL else -1

        # Q値を更新
        future_value = (
            0 if next_position == GOAL
            else max(q_table[next_position])
        )

        old_value = q_table[position][action_index]
        q_table[position][action_index] = old_value + alpha * (
            reward + gamma * future_value - old_value
        )

        position = next_position

        if position == GOAL:
            break

# 学習結果を表示
print("=== Q学習の結果 ===")
for position in range(GOAL):
    left, right = q_table[position]
    direction = "右" if right > left else "左"
    print(f"{position}マス目：{direction}へ進む")

# 学習したQ値を使ってゴールまで移動
print("\n=== 学習後の走行テスト ===")
position = 0
route = [position]

for step in range(10):
    action_index = max(
        range(2),
        key=lambda i: q_table[position][i]
    )
    position = max(
        0, min(GOAL, position + ACTIONS[action_index])
    )
    route.append(position)

    if position == GOAL:
        break

print("移動経路：", " → ".join(map(str, route)))
print("ゴール到達！" if position == GOAL else "ゴール未到達")


import json

with open("/home/gamo/ai_warehouse_courier/gazebo_3d/q_table.json", "w", encoding="utf-8") as f:
    json.dump(q_table, f, indent=2)





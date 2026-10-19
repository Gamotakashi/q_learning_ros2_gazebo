
import json
import time
from pathlib import Path

import rclpy
from geometry_msgs.msg import Twist


# 学習済みのQテーブルを読み込む
file_path = Path(__file__).parent / "q_table.json"

with open(file_path, "r", encoding="utf-8") as f:
    q_table = json.load(f)


def send_speed(publisher, speed):
    msg = Twist()
    msg.linear.x = speed
    publisher.publish(msg)


def main():
    rclpy.init()
    node = rclpy.create_node("mamori_q_gazebo")

    green = node.create_publisher(
        Twist, "/model/vehicle_green/cmd_vel", 10
    )

    position = 0
    goal = 4

    try:
        print("Q学習の結果を使って緑のロボットを動かします")
        time.sleep(2)

        for step in range(10):
            left_q, right_q = q_table[position]

            # Q値が大きい行動を選ぶ
            if right_q > left_q:
                action = "右"
                speed = 0.2
                next_position = min(goal, position + 1)
            else:
                action = "左"
                speed = -0.2
                next_position = max(0, position - 1)

            print(f"{step + 1}歩目：{action}へ進む")

            # 1マス分の行動をGazeboで実行
            start = time.monotonic()

            while time.monotonic() - start < 3.5:
                send_speed(green, speed)
                time.sleep(0.1)

            position = next_position

            if position == goal:
                print("仮想環境でゴール到達！")
                break

    finally:
        for _ in range(10):
            send_speed(green, 0.0)
            time.sleep(0.1)

        node.destroy_node()
        rclpy.shutdown()
        print("緑のロボットを停止しました")


if __name__ == "__main__":
    main()



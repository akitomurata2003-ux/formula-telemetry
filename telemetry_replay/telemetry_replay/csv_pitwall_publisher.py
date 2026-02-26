import os
import csv

import rclpy
from rclpy.node import Node
from telemetry_msgs.msg import PitwallFrame


class CsvPublisher(Node):
    def __init__(self):
        super().__init__('csv_publisher')

        self.pub = self.create_publisher(PitwallFrame, '/telemetry/pitwall_frame', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.data = []
        self.index = 0
        self.seq = 0  # ★追加：seq初期化

        csv_path = os.path.expanduser('~/formula_ws/data/csv/Ecopa20Hz.csv')
        with open(csv_path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)  # 1行目スキップ
            for row in reader:
                values = [float(x) for x in row[:19]]
                self.data.append(values)

        self.get_logger().info(f'Loaded {len(self.data)} rows from CSV')

    def timer_callback(self):
        if self.index >= len(self.data):
            self.get_logger().info('CSV publish finished')
            self.timer.cancel()
            return

        values = self.data[self.index]  # ★追加：この行がないと埋められない

        msg = PitwallFrame()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"

        msg.seq = self.seq
        self.seq += 1

        # values[0] = t_csv という仮定（CSVの列順に合わせて要調整）
        msg.t_csv = float(values[0])

        msg.steering_angle   = float(values[1])
        msg.brake_pressure   = float(values[2])
        msg.accel_opening    = float(values[3])
        msg.torque_request   = float(values[4])
        msg.ready_to_drive   = bool(int(values[5]))

        msg.motor_temperature = float(values[6])
        msg.motor_rpm         = float(values[7])
        msg.inverter_voltage  = float(values[8])
        msg.igbt_temperature  = float(values[9])

        msg.stroke_rr = float(values[10])
        msg.stroke_rl = float(values[11])
        msg.stroke_fr = float(values[12])
        msg.stroke_fl = float(values[13])

        msg.longitude = float(values[14])
        msg.latitude  = float(values[15])

        msg.gyro_x = float(values[16])
        msg.gyro_y = float(values[17])
        msg.gyro_z = float(values[18])

        self.pub.publish(msg)
        self.index += 1  # ★追加：行を進める


def main(args=None):
    rclpy.init(args=args)
    node = CsvPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
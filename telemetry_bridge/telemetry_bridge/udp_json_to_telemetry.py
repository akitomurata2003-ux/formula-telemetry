#!/usr/bin/env python3
import json
import socket
from typing import Any, Dict

import rclpy
from rclpy.node import Node

from telemetry_msgs.msg import TelemetryFrame


def _get(d: Dict[str, Any], key: str, default: float = 0.0) -> float:
    v = d.get(key, default)
    try:
        return float(v)
    except Exception:
        return float(default)


class UdpJsonToTelemetry(Node):
    def __init__(self):
        super().__init__("udp_json_to_telemetry")

        self.declare_parameter("bind_ip", "0.0.0.0")
        self.declare_parameter("bind_port", 5005)
        self.declare_parameter("topic", "/telemetry/frame")

        bind_ip = self.get_parameter("bind_ip").value
        bind_port = int(self.get_parameter("bind_port").value)
        topic = self.get_parameter("topic").value

        self.pub = self.create_publisher(TelemetryFrame, topic, 10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((bind_ip, bind_port))
        self.sock.setblocking(False)

        self.timer = self.create_timer(0.001, self._poll)

        self.get_logger().info(f"Listening UDP JSON on {bind_ip}:{bind_port} -> {topic}")

    def _poll(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(8192)
            except BlockingIOError:
                break
            except Exception as e:
                self.get_logger().warn(f"UDP recv error: {e}")
                break

            try:
                obj = json.loads(data.decode("utf-8"))
            except Exception as e:
                self.get_logger().warn(f"JSON decode error from {addr}: {e}")
                continue

            msg = TelemetryFrame()
            msg.stamp = self.get_clock().now().to_msg()

            # あなたのTelemetryFrame.msgに合わせて埋める（無いフィールドは削る/追加する）
            msg.tbc_voltage = _get(obj, "tbc_voltage")
            msg.rpm = int(obj.get("rpm", 0))
            msg.inverter_temp = _get(obj, "inverter_temp")
            msg.igbt_temp = _get(obj, "igbt_temp")

            self.pub.publish(msg)


def main():
    rclpy.init()
    node = UdpJsonToTelemetry()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

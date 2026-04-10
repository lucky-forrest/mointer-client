#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Socket 客户端测试模块
用于测试 SocketServerV2 服务端是否正常工作
"""

import socket
import json
import time
from datetime import datetime


class SocketClient:
    """Socket 客户端类"""

    ENCODING = 'utf-8'
    MAX_BUFFER_SIZE = 65536

    def __init__(self, host='127.0.0.1', port=8888):
        """
        初始化 Socket 客户端
        Args:
            host: 服务器地址,默认 127.0.0.1
            port: 服务器端口,默认 8888
        """
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False

        # 自动生成当前时间戳
        self.get_timestamp = lambda: datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]

    def connect(self, timeout=10):
        """
        连接到服务器
        Args:
            timeout: 连接超时时间(秒)
        Returns:
            bool: 是否连接成功
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(timeout)
            self.client_socket.connect((self.host, self.port))

            self.connected = True
            print(f"[INFO] 成功连接到服务器: {self.host}:{self.port}")
            return True

        except Exception as e:
            print(f"[ERROR] 连接服务器失败: {str(e)}")
            self.connected = False
            return False

    def disconnect(self):
        """断开与服务器的连接"""
        if self.client_socket:
            try:
                self.client_socket.close()
                print("[INFO] 已断开与服务器的连接")
            except Exception as e:
                print(f"[ERROR] 断开连接时出错: {str(e)}")
            finally:
                self.client_socket = None
                self.connected = False

    def _create_message(self, message_name, body=None, machine_name="TestClient"):
        """
        创建标准格式的消息
        Args:
            message_name: 消息名称
            body: 消息体
            machine_name: 机器名称
        Returns:
            dict: 标准格式的消息对象
        """
        message = {
            "Request": {
                "Header": {
                    "MachineName": machine_name,
                    "TransactionID": str(int(datetime.now().timestamp() * 1000)),
                    "MessageName": message_name,
                    "UserName": "test",
                    "EventTime": self.get_timestamp()
                },
                "Body": body or {}
            }
        }
        return message

    def _format_for_send(self, message):
        """
        格式化消息用于发送：纯 JSON，以换行符结束
        Args:
            message: 要发送的消息对象
        Returns:
            bytes: 格式化后的字节流
        """
        message_str = json.dumps(message, ensure_ascii=False)
        # 添加换行符表示结束（Unix风格）
        message_str += '\n'
        # 确保所有换行符都是 '\n' 而不是 '\r\n'
        message_bytes = message_str.encode(self.ENCODING)
        # 替换所有 \r\n 为 \n
        message_bytes = message_bytes.replace(b'\r\n', b'\n')
        return message_bytes

    def _parse_received_data(self, full_data):
        """
        解析接收到的数据（纯 JSON，以换行符结束）
        Args:
            full_data: 接收到的所有数据
        Returns:
            tuple: (message_dict, remaining_data) or (None, full_data) if incomplete
        """
        if b'\n' not in full_data:
            # 未收到换行符，数据不完整
            return None, full_data

        # 拆分出完整的消息（前面是 JSON，后面是换行符和数据）
        message_str = full_data.split(b'\n', 1)[0]
        remaining_data = full_data[full_data.index(b'\n') + 1:]

        # 解析消息
        return json.loads(message_str.decode(self.ENCODING)), remaining_data

    def _send_and_receive(self, message):
        """
        发送消息并接收响应
        Args:
            message: 要发送的消息对象
        Returns:
            dict: 解析后的响应,失败返回 None
        """
        try:
            if not self.connected:
                print("[ERROR] 未连接到服务器")
                return None

            # 格式化消息（添加长度前缀）
            formatted_data = self._format_for_send(message)

            # 获取消息类型
            header = message.get('Request', {}).get('Header', {})
            message_name = header.get('MessageName', 'unknown')
            print(f"\n[SEND] 消息名称: {message_name}")
            print(f"[SEND] 请求数据长度: {len(formatted_data)} 字节")

            # 发送消息
            self.client_socket.sendall(formatted_data)
            print(f"[SEND] 已发送 {len(formatted_data)} 字节")

            # 接收响应（可能需要多次接收以获取完整数据）
            full_response = b''
            elapsed_time = 0
            start_time = time.time()

            while elapsed_time < 10:  # 最多等待10秒
                try:
                    chunk = self.client_socket.recv(self.MAX_BUFFER_SIZE)
                    if not chunk:
                        print("[ERROR] 连接已关闭")
                        return None

                    full_response += chunk

                    # 尝试解析数据
                    parsed_message, remaining = self._parse_received_data(full_response)

                    if parsed_message is not None:
                        # 收到完整消息
                        if parsed_message.get('Response'):
                            response_return = parsed_message.get('Response', {}).get('Return', {})
                            if response_return:
                                return_msg = response_return.get('ReturnMessage', 'unknown')
                            else:
                                return_msg = 'unknown'

                            print(f"[RECV] 响应: {return_msg}")
                            return parsed_message

                        # 没有嵌套 Response，以整个消息作为响应
                        print(f"[RECV] 响应: 收到消息")
                        return parsed_message

                    # 数据不完整，更新超时
                    full_response = remaining
                    elapsed_time = time.time() - start_time
                    print(f"[DEBUG] 等待更多数据... 已接收 {len(full_response)} 字节")
                    time.sleep(0.1)

                except socket.timeout:
                    elapsed_time = time.time() - start_time
                    print(f"[DEBUG] 接收超时... 已接收 {len(full_response)} 字节")
                    time.sleep(0.1)

            print(f"[ERROR] 接收超时或连接关闭，总接收 {len(full_response)} 字节")
            return None

        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON 解析失败: {str(e)}")
            print(f"[ERROR] 原始数据: {full_response[:200] if full_response else 'None'}")
            return None
        except Exception as e:
            print(f"[ERROR] 发送/接收消息时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    # ==================== 执行测试 ====================

    def test_connection(self):
        """测试连接是否正常"""
        print("\n" + "="*60)
        print("测试 1: 连接测试")
        print("="*60)

        if self.connect():
            time.sleep(0.5)
            self.disconnect()
            print("[PASS] 连接测试成功\n")
            return True
        else:
            print("[FAIL] 连接测试失败\n")
            return False

    def test_load_data(self):
        """测试加载数据接口"""
        print("\n" + "="*60)
        print("测试 5: 加载数据 (load_data)")
        print("="*60)

        if not self.connect():
            return False

        try:
            # 构造加载数据请求
            body = {"load_condition": "default"}

            message = self._create_message("load_data", body=body)
            print(f"[INFO] 发送消息类型: load_data")
            response = self._send_and_receive(message)

            if response is None:
                print("[FAIL] 未收到响应")
                return False

            # 验证响应结构
            if 'Response' not in response:
                print("[FAIL] 响应格式错误: 缺少 Response")
                return False

            return_info = response.get('Response', {}).get('Return', {})
            if not return_info:
                print("[FAIL] 响应格式错误: 缺少 Return")
                return False

            load_data = response.get('Response', {}).get('Body', {})

            # 验证响应格式
            success = return_info.get('ReturnCode') == 'OK'
            if success and load_data is not None:
                print(f"[PASS] 加载数据成功")
                print(f"  - 加载状态: {load_data.get('loaded')}")
                print(f"  - 记录ID: {load_data.get('record_id')}")
                if load_data.get('loaded'):
                    product = load_data.get('data', {}).get('产品信息', {})
                    recipe = load_data.get('data', {}).get('配方信息', {})
                    print(f"  - 加载的产品: {product.get('name')} ({product.get('type')})")
                    print(f"  - 加载的配方: {recipe.get('name')}")
            else:
                print(f"[FAIL] 加载数据失败: {return_info.get('ReturnMessage')}")

            return success

        except Exception as e:
            print(f"[ERROR] 测试过程中出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.disconnect()

    def test_reset_data(self):
        """测试重置数据接口"""
        print("\n" + "="*60)
        print("测试 6: 重置数据 (reset_data)")
        print("="*60)

        if not self.connect():
            return False

        try:
            # 构造重置数据请求
            body = {"user_confirm": True}

            message = self._create_message("reset_data", body=body)
            print(f"[INFO] 发送消息类型: reset_data")
            response = self._send_and_receive(message)

            if response is None:
                print("[FAIL] 未收到响应")
                return False

            # 验证响应结构
            if 'Response' not in response:
                print("[FAIL] 响应格式错误: 缺少 Response")
                return False

            return_info = response.get('Response', {}).get('Return', {})
            if not return_info:
                print("[FAIL] 响应格式错误: 缺少 Return")
                return False

            reset_data = response.get('Response', {}).get('Body', {})

            # 验证响应格式
            success = return_info.get('ReturnCode') == 'OK'
            if success and reset_data is not None:
                print(f"[PASS] 重置数据成功")
                print(f"  - 重置时间: {reset_data.get('reset_time')}")
            else:
                print(f"[FAIL] 重置数据失败: {return_info.get('ReturnMessage')}")

            return success

        except Exception as e:
            print(f"[ERROR] 测试过程中出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.disconnect()

    def run_all_tests(self):
        """运行所有测试用例"""
        print("\n" + "#"*60)
        print("# Socket 服务端测试客户端")
        print("#"*60)
        print(f"测试服务器: {self.host}:{self.port}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("#"*60)

        results = {}

        # 执行测试
        results['connection'] = self.test_connection()
        if not results['connection']:
            print("\n[WARN] 连接测试失败,后续测试可能无法进行")
            print("请确保 socket_server.py 已启动...")
            return results

        results['load_data'] = self.test_load_data()
        results['reset_data'] = self.test_reset_data()

        # 输出测试汇总
        print("\n" + "#"*60)
        print("# 测试结果汇总")
        print("#"*60)

        total = len(results)
        passed = sum(1 for v in results.values() if v)
        failed = total - passed

        for test_name, result in results.items():
            status = "PASS ✓" if result else "FAIL ✗"
            print(f"  {test_name:20s} : {status}")

        print("#"*60)
        print(f"总计: {passed}/{total} 测试通过")
        print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("#"*60 + "\n")

        # 返回测试结果
        return results


def main():
    """主函数"""
    # 可以通过命令行参数指定服务器地址和端口
    import sys

    host = '127.0.0.1'
    port = 8888

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    print(f"从参数加载配置: host={host}, port={port}")

    # 创建客户端
    client = SocketClient(host=host, port=port)

    # 运行所有测试
    results = client.run_all_tests()

    # 返回退出码
    if all(results.values()):
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())

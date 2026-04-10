#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Socket 服务端模块 v2 (纯 JSON 版)
基于 B0304_EQP_Socket 标准接口文档 v1.0.3 实现
使用标准消息格式: 纯 JSON，以换行符 (\n) 结尾
"""

import socket
import threading
import json
from datetime import datetime

class SocketServerV2:
    """Socket 服务端类 (纯 JSON 通信)"""

    # 定义最大接收缓冲区大小 (例如 64KB)，防止内存溢出
    MAX_BUFFER_SIZE = 65536

    def __init__(self, host='0.0.0.0', port=8888):
        """
        初始化 Socket 服务端
        Args:
            host: 监听地址
            port: 监听端口
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False

        # 获取当前时间: yyyyMMddHHmmss.fff
        self.get_timestamp = lambda: datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]

    def start(self):
        """启动 Socket 服务端"""
        try:
            # 创建 TCP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 绑定地址和端口
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"{'='*60}")
            print("Socket 服务端启动成功 (纯 JSON 模式)")
            print(f"监听地址: {self.host}:{self.port}")
            print(f"{'='*60}\n")
            
            # 接受客户端连接
            self.accept_connection()
            
        except Exception as e:
            print(f"[ERROR] 启动服务端失败: {str(e)}")
            raise

    def accept_connection(self):
        """接受客户端连接"""
        try:
            self.server_socket.settimeout(1.0)
            while self.running:
                try:
                    self.client_socket, self.client_address = self.server_socket.accept()
                    self.client_socket.settimeout(30.0) # 设置 30 秒超时
                    print(f"\n[INFO] 客户端已连接: {self.client_address}")
                    
                    # 启动单独的线程处理客户端请求
                    self.client_thread = threading.Thread(
                        target=self.handle_client,
                        daemon=True
                    )
                    self.client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] 接受连接时出错: {str(e)}")
        except Exception as e:
            print(f"[ERROR] 接受连接循环出错: {str(e)}")
        finally:
            print("[INFO] 等待连接循环结束")

    def _receive_request(self):
        """
        接收并解析客户端请求消息
        消息格式: 纯 JSON，以换行符 (\n) 结尾
        """
        try:
            # 1. 读取完整的一行（包括换行符）
            received_data = b''
            while True:
                try:
                    chunk = self.client_socket.recv(1024)
                    if not chunk:
                        print("[WARNING] 客户端断开连接或未发送数据")
                        return None

                    received_data += chunk

                    # 检查是否收到换行符
                    if b'\n' in received_data:
                        break

                    # 防止无限循环，限制最大接收长度
                    if len(received_data) > self.MAX_BUFFER_SIZE:
                        return None

                except socket.timeout:
                    return None

            # 2. 按第一个换行符分割，得到纯 JSON 字符串（去除换行符）
            message_data = received_data.split(b'\n', 1)[0]
            # 如果分割后包含 \r，则去掉它
            if message_data.endswith(b'\r'):
                message_data = message_data[:-1]
            message_data = message_data.decode('utf-8').strip()

            # 3. 解析 JSON
            try:
                request = json.loads(message_data)
                print(f"[DEBUG] 解析成功: MessageName={request.get('Request', {}).get('Header', {}).get('MessageName', 'unknown')}")
                return request
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON 解析失败: {str(e)}")

                # 构造错误响应
                error_response = {
                    "Response": {
                        "Header": {
                            "MachineName": "unknown",
                            "TransactionID": "unknown",
                            "MessageName": "ERROR",
                            "UserName": "unknown",
                            "EventTime": self.get_timestamp()
                        },
                        "Body": None,
                        "Return": {
                            "ReturnCode": "NA",
                            "ReturnMessage": f"JSON 解析失败: {str(e)}"
                        }
                    }
                }
                self.send_response(error_response)
                return None

        except Exception as e:
            print(f"[ERROR] 接收请求时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def handle_client(self):
        """处理客户端请求"""
        print(f"[INFO] 客户端已连接: {self.client_address}")

        try:
            while self.running:
                try:
                    # 接收请求消息（纯 JSON）
                    request = self._receive_request()
                    if not request:
                        break

                    # 处理消息并返回响应
                    response = self.process_request(request)

                    # 发送响应
                    self.send_response(response)

                except socket.timeout:
                    if not self.running:
                        break
                    continue
                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"[ERROR] 处理客户端数据时出错: {str(e)}")
                    break

        except Exception as e:
            print(f"[ERROR] 处理客户端线程异常: {str(e)}")
        finally:
            if self.client_socket:
                try:
                    self.client_socket.close()
                    print("[INFO] 客户端连接已关闭")
                except:
                    pass

    def process_request(self, request):
        """
        处理请求消息
        Args:
            request: 完整的请求消息对象
        Returns:
            dict: 标准格式的响应消息
        """
        try:
            tempRequest = request.get('Request', {})
            request_header = tempRequest.get('Header', {})
            request_body = tempRequest.get('Body', {})
            message_name = request_header.get('MessageName', '')

            # 构造响应 Header
            response_header = {
                "MachineName": request_header.get("MachineName", "Server"),
                "TransactionID": request_header.get("TransactionID", ""),
                "MessageName": message_name,
                "UserName": request_header.get("UserName", "unknown"),
                "EventTime": self.get_timestamp()
            }

            # 根据消息类型处理
            response_body = None
            return_info = None

            if message_name == "save_data":
                return_info = self.handle_save_data(request_body)
            elif message_name == "load_data":
                return_info = self.handle_load_data(request_body)
            elif message_name == "reset_data":
                return_info = self.handle_reset_data(request_body)
            else:
                return_info = {
                    "ReturnCode": "NA",
                    "ReturnMessage": f"Unknown message type: {message_name}"
                }

            # 构造完整响应
            response = {
                "Response": {
                    "Header": response_header,
                    "Body": response_body,
                    "Return": return_info
                }
            }
            return response

        except Exception as e:
            print(f"[ERROR] 处理请求时出错: {str(e)}")
            print(f"[ERROR] 原始请求: {request}")
            return {
                "Response": {
                    "Header": {
                        "MachineName": "unknown",
                        "TransactionID": "unknown",
                        "MessageName": "ERROR",
                        "UserName": "unknown",
                        "EventTime": self.get_timestamp()
                    },
                    "Body": None,
                    "Return": {
                        "ReturnCode": "NG",
                        "ReturnMessage": f"处理请求失败: {str(e)}"
                    }
                }
            }

    # ==================== 工具方法 ====================
    def _create_error_response(self, error_message):
        """
        创建错误响应
        Args:
            error_message: 错误信息
        Returns:
            dict: 错误响应对象
        """
        return {
            "Response": {
                "Header": {
                    "MachineName": "Server",
                    "TransactionID": "",
                    "MessageName": "ERROR",
                    "UserName": "unknown",
                    "EventTime": self.get_timestamp()
                },
                "Body": None,
                "Return": {
                    "ReturnCode": "NG",
                    "ReturnMessage": error_message
                }
            }
        }

    # ==================== 消息处理器 ====================
    def handle_save_data(self, body):
        """处理保存数据请求"""
        try:
            product_info = body.get("产品信息", {})
            recipe_info = body.get("配方信息", {})
            print(f"[INFO] Saving recipe data: {recipe_info.get('name')}")

            save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record_id = f"REC-{int(time.time())}"
            
            return {
                "ReturnCode": "OK",
                "ReturnMessage": "Save Data Success",
                "data": {
                    "save_time": save_time,
                    "record_id": record_id,
                    "product_name": product_info.get("name", ""),
                    "recipe_name": recipe_info.get("name", "")
                }
            }
        except Exception as e:
            print(f"[ERROR] Save data failed: {str(e)}")
            return {
                "ReturnCode": "NG",
                "ReturnMessage": f"Save data failed: {str(e)}"
            }

    def handle_load_data(self, body):
        """处理加载数据请求"""
        try:
            print(f"[INFO] Loading data")
            return {
                "ReturnCode": "OK",
                "ReturnMessage": "Load Data Success",
                "data": {
                    "loaded": True,
                    "record_id": None,
                    "data": {
                        "产品信息": {
                            "name": "Sample Product",
                            "type": "liquid",
                            "description": "Loaded product from database"
                        },
                        "配方信息": {
                            "name": "Sample Recipe",
                            "number": "001",
                            "ingredients": ["ingredient A", "ingredient C"],
                            "additive": "additive X",
                            "temperature": 50,
                            "time": 60,
                            "notes": "Loaded notes from database"
                        }
                    }
                }
            }
        except Exception as e:
            print(f"[ERROR] Load data failed: {str(e)}")
            return {
                "ReturnCode": "NG",
                "ReturnMessage": f"Load data failed: {str(e)}"
            }

    def handle_reset_data(self, body):
        """处理重置数据请求"""
        print(f"[INFO] Resetting data")
        return {
            "ReturnCode": "OK",
            "ReturnMessage": "Reset Data Success",
            "data": {
                "reset_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

    # ==================== 工具方法 ====================
    def send_response(self, response):
        """
        发送响应数据 (纯 JSON，以换行符结束)
        Args:
            response: 要发送的响应数据
        """
        try:
            # 将响应转换为 JSON 字符串
            response_str = json.dumps(response, ensure_ascii=False)

            # 添加换行符表示结束
            response_str += '\n'

            # 直接发送 JSON 字符串 (无需长度前缀)
            encoded = response_str.encode('utf-8')
            self.client_socket.sendall(encoded)

        except Exception as e:
            print(f"[ERROR] 发送响应失败: {str(e)}")

    def stop(self):
        """停止 Socket 服务端"""
        print("\n[INFO] 正在停止服务端...")
        self.running = False
        
        # 关闭客户端连接
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
                
        # 关闭服务端 socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("[INFO] 服务端已停止")

def main():
    """主函数"""
    # 创建并启动服务端
    server = SocketServerV2(host='0.0.0.0', port=8888)
    try:
        # 启动服务端
        server.start()
        print("\n按 Ctrl+C 停止服务端\n")
        print("="*60)
        
        # 主线程保持运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n收到停止信号...")
        server.stop()
    except Exception as e:
        print(f"\n服务端发生错误: {str(e)}")
        server.stop()

if __name__ == "__main__":
    main()
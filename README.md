# Mointer Client - 配方管理客户端

基于 Python 开发的配方管理客户端应用程序，包含 GUI 界面和 Socket 通信功能。

## 项目结构

```
mointer-client/
├── main.py              # 主入口文件（配方管理 GUI）
├── socket_client.py     # Socket 客户端测试模块
├── socket_server.py     # Socket 服务端模块
├── config.py            # 配置文件（预留）
├── .gitignore           # Git 忽略文件
├── CLAUDE.md            # Claude Code 项目配置
├── requirements.txt     # Python 依赖列表
├── README.md            # 项目说明文档
└── 需求.md              # 完整需求文档
```

## 主要功能

### 1. 配方管理 GUI（main.py）
- 产品信息管理
- 配方信息配置
- 数据保存/加载/重置
- 进度条状态显示
- 可滚动界面设计
- 菜单栏支持

### 2. Socket 通信模块
- `socket_server.py` - 提供标准 API 接口的服务端
- `socket_client.py` - 用于测试服务端的客户端
- 支持 save_data、load_data、reset_data 消息类型
- 标准 JSON 通信格式
- 多线程处理

## 功能特性

- 基于 tkinter 的图形界面
- Socket 通信功能
- 实时数据加载显示
- 进度条可视化
- 完整的数据验证
- 模块化设计
- 命令行参数支持

## 开发环境

- Python 3.x
- tkinter（通常随 Python 一起安装）
- JSON 模块（内置）

## 安装和使用

### 1. 克隆仓库
```bash
git clone https://github.com/lucky-forrest/mointer-client.git
cd mointer-client
```

### 2. 运行配方管理 GUI
```bash
python main.py
```

GUI 界面包含：
- 产品信息区域（输入框、下拉框、文本框）
- 配方信息区域（多行输入、复选框、滑块、旋转框）
- 操作按钮（保存、重置、加载、退出）
- 状态显示和进度条

### 3. 启动 Socket 服务端
```bash
python socket_server.py
```

服务端特性：
- 监听端口 8888
- 支持多客户端连接
- 标准消息格式
- 详细日志输出

### 4. 运行 Socket 客户端测试
```bash
python socket_client.py [host] [port]
```

不传参数使用默认 host=127.0.0.1, port=8888

测试内容包括：
1. 连接测试
2. 加载数据测试 (load_data)
3. 重置数据测试 (reset_data)

## 扩展功能

GUI 菜单支持：
- 文件菜单：保存、加载、退出
- 编辑菜单：重置、全选、启动/停止 Socket 服务端
- 帮助菜单：关于信息

Socket 通信协议：
- 消息格式：`{Request/Response: {Header: {...}, Body: {...}, Return: {...}}}`
- 通信方式：纯 JSON 字符串，以换行符 `\n` 结尾
- 服务端仅在 GUI 启动 Socket 服务端菜单时运行

## 开发规范

### 代码风格
- 遵循 PEP 8 编码规范
- 使用 4 个空格缩进
- 使用 UTF-8 编码
- 每行代码不超过 88 字符

### 命名规范
- 变量和函数：蛇形命名法（snake_case）
- 类：帕斯卡命名法（PascalCase）
- 常量：大写下划线（UPPER_SNAKE_CASE）

### tkinter 控件命名
| 控件类型 | 前缀 | 示例 |
|---------|------|------|
| Entry | entry_ | entry_product_name |
| Text | txt_ | txt_description |
| Combobox | combo_ | combo_product_type |
| Checkbutton | chk_ | chk_ingredient_a |
| Scale | scale_ | scale_temperature |
| Spinbox | spinbox_ | spinbox_time |
| Button | btn_ | btn_save |
| Label | lbl_ | lbl_status |
| Frame | frame_ | frame_product |
| Progressbar | progress_ | progress_bar |

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

*本项目使用 [Claude Code](https://claude.ai/code) 开发*

## 安装和使用

1. 克隆仓库：
```bash
git clone https://github.com/lucky-forrest/mointer-client.git
cd mointer-client
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 运行程序：
```bash
python main.py
```

## 开发规范

### 代码风格
- 遵循 PEP 8 编码规范
- 使用 4 个空格缩进
- 每行代码不超过 88 字符

### 命名规范
- 变量和函数：蛇形命名法（snake_case）
- 类：帕斯卡命名法（PascalCase）
- 常量：大写下划线（UPPER_SNAKE_CASE）

### tkinter 控件命名
- Entry: `entry_`
- Text: `txt_`
- Combobox: `combo_`
- Button: `btn_`
- Label: `lbl_`
- Frame: `frame_`
- 等等...

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

*本项目使用 [Claude Code](https://claude.ai/code) 开发*
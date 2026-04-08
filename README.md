# Mointer Client

一个基于 tkinter 的 Python 客户端应用程序。

## 项目结构

```
mointer-client/
├── main.py           # 主入口文件
├── config.py         # 配置文件
├── .gitignore        # Git 忽略文件
├── README.md         # 项目说明文档
└── CLAUDE.md         # Claude Code 配置文件
```

## 功能特性

- 基于 tkinter 的图形界面
- 配置文件管理
- 模块化设计

## 开发环境

- Python 3.x
- tkinter（通常随 Python 一起安装）

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
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python 开发规范

### 代码风格
- 遵循 PEP 8 编码规范
- 使用 4 个空格缩进
- 使用 UTF-8 编码
- 每行代码不超过 88 字符

### 命名规范
- 变量和函数：蛇形命名法（snake_case）
- 类：帕斯卡命名法（PascalCase）
- 常量：大写下划线（UPPER_SNAKE_CASE）
- GUI 控件：使用描述性前缀，如 `entry_product_name`、`btn_save`、`combo_product_type`

### tkinter 控件命名前缀规范
| 控件类型 | 前缀 | 示例 |
|---------|------|------|
| Entry | entry_ | entry_product_name |
| Text | txt_ | txt_description |
| Combobox | combo_ | combo_product_type |
| Checkbutton | chk_ | chk_ingredient_a |
| Radiobutton | radio_ | radio_option_a |
| Button | btn_ | btn_save |
| Label | lbl_ | lbl_status |
| Scale | scale_ | scale_temperature |
| Spinbox | spinbox_ | spinbox_time |
| Progressbar | progress_ | progress_bar |
| Frame | frame_ | frame_product |
| LabelFrame | labelframe_ | labelframe_recipe |
| Menu | menu_ | menu_file |
| Scrollbar | scrollbar_ | scrollbar_text |

### tkinter 开发注意事项
1. 所有控件必须显式命名，不能省略
2. 所有控件需要配置完整的基本属性（width、height、font、state 等）
3. 使用布局管理器（pack、grid、place）时需要指定布局参数
4. 事件处理函数命名：`on_<控件>_<动作>`，如 `on_btn_save_click`
5. 窗口尺寸默认设置为 800x600 或根据内容自适应

### 文件结构
```
mointer-client/
├── main.py           # 主入口文件
├── config.py         # 配置文件
├── widgets/          # 自定义控件模块（可选）
├── utils/            # 工具函数模块（可选）
└── resources/        # 资源文件（可选）
```

### 注释规范
- 每个模块顶部包含模块说明
- 每个类和函数需要 docstring
- 复杂逻辑需要行内注释

### 调试
- 使用 `print()` 输出调试信息
- 遇到异常时输出完整的堆栈跟踪

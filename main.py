#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配方管理客户端 GUI
基于 Python tkinter 开发的配方管理演示软件
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json


class RecipeManagerApp:
    """配方管理客户端主应用类"""

    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title("配方管理客户端")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 设置窗口图标（可选）
        # self.root.iconbitmap("resources/icon.ico")

        # 数据存储
        self.product_data = {
            'name': '',
            'type': '',
            'description': ''
        }

        self.recipe_data = {
            'name': '',
            'number': '',
            'ingredients': [],
            'additive': '',
            'temperature': 20,
            'time': 30,
            'notes': ''
        }

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建所有控件"""
        # 创建主滚动容器
        self.create_scrollable_container()

        # 创建三个主要区域
        self.create_product_info_section()
        self.create_recipe_info_section()
        self.create_operation_section()

        # 创建菜单
        self.create_menu()

    def create_scrollable_container(self):
        """创建可滚动的容器"""
        # 创建滚动条
        self.scrollbar_y = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建Canvas
        self.canvas = tk.Canvas(self.root, yscrollcommand=self.scrollbar_y.set,
                               highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 配置滚动条
        self.scrollbar_y.config(command=self.canvas.yview)

        # 创建可滚动的内容框架
        self.content_frame = tk.Frame(self.canvas, padx=10, pady=10)
        self.canvas_window = self.canvas.create_window((0, 0),
                                                        window=self.content_frame,
                                                        anchor="nw",
                                                        width=self.canvas.winfo_reqwidth())

        # 绑定事件
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_frame_configure(self, event):
        """当内容框架大小改变时更新滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """当Canvas大小改变时更新内容宽度"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        """处理鼠标滚轮滚动"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_product_info_section(self):
        """创建产品信息区域"""
        # 产品信息框架
        product_frame = tk.LabelFrame(self.content_frame, text="产品信息",
                                     font=("Arial", 12, "bold"))
        product_frame.pack(fill=tk.X, pady=(0, 10))

        # 使用grid布局
        product_frame.grid_columnconfigure(1, weight=1)

        # 产品名称
        tk.Label(product_frame, text="产品名称:", width=15, anchor="e").grid(
            row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_product_name = tk.Entry(product_frame, width=50, font=("Arial", 10))
        self.entry_product_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # 产品类型
        tk.Label(product_frame, text="产品类型:", width=15, anchor="e").grid(
            row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_product_type = ttk.Combobox(product_frame, width=20,
                                              font=("Arial", 10), state="readonly")
        self.combo_product_type['values'] = ["液体", "固体", "气体", "粉末"]
        self.combo_product_type.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # 产品描述
        tk.Label(product_frame, text="产品描述:", width=15, anchor="e").grid(
            row=2, column=0, padx=5, pady=5, sticky="ne")
        self.txt_description = tk.Text(product_frame, width=50, height=5,
                                     font=("Arial", 10))
        self.txt_description.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # 添加滚动条
        scrollbar_desc = tk.Scrollbar(product_frame, command=self.txt_description.yview)
        scrollbar_desc.grid(row=2, column=2, padx=(0, 5), pady=5, sticky="ns")
        self.txt_description.config(yscrollcommand=scrollbar_desc.set)

    def create_recipe_info_section(self):
        """创建配方信息区域"""
        # 配方信息框架
        recipe_frame = tk.LabelFrame(self.content_frame, text="配方信息",
                                    font=("Arial", 12, "bold"))
        recipe_frame.pack(fill=tk.X, pady=(0, 10))

        # 使用grid布局
        recipe_frame.grid_columnconfigure(1, weight=1)

        # 配方名称
        tk.Label(recipe_frame, text="配方名称:", width=15, anchor="e").grid(
            row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_recipe_name = tk.Entry(recipe_frame, width=50, font=("Arial", 10))
        self.entry_recipe_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 配方编号
        tk.Label(recipe_frame, text="配方编号:", width=15, anchor="e").grid(
            row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_recipe_number = tk.Entry(recipe_frame, width=50, font=("Arial", 10))
        self.entry_recipe_number.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # 原料多选框区域
        ingredient_frame = tk.LabelFrame(recipe_frame, text="原料选择",
                                        font=("Arial", 10, "bold"))
        ingredient_frame.grid(row=2, column=0, columnspan=3, padx=5,
                             pady=5, sticky="ew")

        self.chk_ingredients = []
        self.chk_vars = []  # 存储Checkbutton的变量
        ingredients = ["原料A", "原料B", "原料C", "原料D", "原料E"]

        for i, ingredient in enumerate(ingredients):
            var = tk.IntVar()
            chk = tk.Checkbutton(ingredient_frame, text=ingredient, variable=var,
                               font=("Arial", 10))
            chk.grid(row=i//3, column=i%3, padx=10, pady=2, sticky="w")
            self.chk_ingredients.append(chk)
            self.chk_vars.append(var)

        # 添加剂和温度
        tk.Label(recipe_frame, text="添加剂:", width=15, anchor="e").grid(
            row=3, column=0, padx=5, pady=5, sticky="e")
        self.combo_additive = ttk.Combobox(recipe_frame, width=20,
                                          font=("Arial", 10), state="readonly")
        self.combo_additive['values'] = ["添加剂X", "添加剂Y", "添加剂Z"]
        self.combo_additive.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # 温度设置
        tk.Label(recipe_frame, text="温度设置:", width=15, anchor="e").grid(
            row=4, column=0, padx=5, pady=5, sticky="e")
        self.scale_temperature = tk.Scale(recipe_frame, from_=0, to=100,
                                        orient=tk.HORIZONTAL,
                                        length=200, font=("Arial", 10), label="°C")
        self.scale_temperature.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # 时间设置
        tk.Label(recipe_frame, text="时间设置:", width=15, anchor="e").grid(
            row=5, column=0, padx=5, pady=5, sticky="e")
        self.spinbox_time = tk.Spinbox(recipe_frame, from_=1, to=999, width=10,
                                      font=("Arial", 10))
        self.spinbox_time.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # 备注
        tk.Label(recipe_frame, text="备注:", width=15, anchor="e").grid(
            row=6, column=0, padx=5, pady=5, sticky="ne")
        self.txt_notes = tk.Text(recipe_frame, width=50, height=3,
                               font=("Arial", 10))
        self.txt_notes.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        # 添加滚动条
        scrollbar_notes = tk.Scrollbar(recipe_frame, command=self.txt_notes.yview)
        scrollbar_notes.grid(row=6, column=2, padx=(0, 5), pady=5, sticky="ns")
        self.txt_notes.config(yscrollcommand=scrollbar_notes.set)

    def create_operation_section(self):
        """创建操作区域"""
        # 操作按钮框架
        operation_frame = tk.Frame(self.content_frame)
        operation_frame.pack(fill=tk.X, pady=(0, 10))

        # 按钮使用grid布局
        tk.Button(operation_frame, text="保存", width=10, font=("Arial", 10),
                 command=self.on_save_click).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(operation_frame, text="重置", width=10, font=("Arial", 10),
                 command=self.on_reset_click).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(operation_frame, text="加载", width=10, font=("Arial", 10),
                 command=self.on_load_click).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(operation_frame, text="退出", width=10, font=("Arial", 10),
                 command=self.on_exit_click).grid(row=0, column=3, padx=5, pady=5)

        # 状态显示框架
        status_frame = tk.Frame(self.content_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        # 状态标签
        self.lbl_status = tk.Label(status_frame, text="就绪", font=("Arial", 10),
                                  fg="green")
        self.lbl_status.pack(side=tk.LEFT, padx=5)

        # 进度条
        self.progress_bar = ttk.Progressbar(status_frame, length=400,
                                           mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="保存", command=self.on_save_click)
        file_menu.add_command(label="加载", command=self.on_load_click)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_exit_click)
        menubar.add_cascade(label="文件", menu=file_menu)

        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="重置", command=self.on_reset_click)
        edit_menu.add_separator()
        edit_menu.add_command(label="全选", command=self.on_select_all)
        menubar.add_cascade(label="编辑", menu=edit_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.on_about_click)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)

    def on_save_click(self):
        """保存按钮点击事件"""
        self.update_status("正在保存...")

        # 模拟保存进度
        self.progress_bar['value'] = 0
        self.root.update()

        # 收集数据
        self.collect_data()

        # 模拟进度
        import time
        for i in range(1, 101, 10):
            self.progress_bar['value'] = i
            self.root.update()
            time.sleep(0.05)

        # 格式化JSON数据
        json_data = self.format_data_to_json()

        # 弹出JSON数据对话框
        self.show_json_dialog(json_data)

        self.update_status("保存成功！", "green")

    def on_load_click(self):
        """加载按钮点击事件"""
        self.update_status("正在加载...")

        # 模拟加载进度
        self.progress_bar['value'] = 0
        self.root.update()

        # 模拟进度
        import time
        for i in range(1, 101, 10):
            self.progress_bar['value'] = i
            self.root.update()
            time.sleep(0.05)

        # 模拟加载数据
        self.load_sample_data()

        self.update_status("加载成功！", "green")
        messagebox.showinfo("加载成功", "配方信息已加载！")

    def on_reset_click(self):
        """重置按钮点击事件"""
        # 重置所有输入
        self.entry_product_name.delete(0, tk.END)
        self.combo_product_type.set("")
        self.txt_description.delete(1.0, tk.END)

        self.entry_recipe_name.delete(0, tk.END)
        self.entry_recipe_number.delete(0, tk.END)

        for var in self.chk_vars:
            var.set(0)

        self.combo_additive.set("")
        self.scale_temperature.set(20)
        self.spinbox_time.delete(0, tk.END)
        self.spinbox_time.insert(0, "30")
        self.txt_notes.delete(1.0, tk.END)

        self.update_status("已重置所有输入", "blue")

    def on_exit_click(self):
        """退出按钮点击事件"""
        if messagebox.askyesno("退出", "确定要退出程序吗？"):
            self.root.quit()

    def on_select_all(self):
        """全选功能"""
        # 选中所有原料
        for var in self.chk_vars:
            var.set(1)

    def on_about_click(self):
        """关于对话框"""
        messagebox.showinfo("关于",
                          "配方管理客户端 v1.0\n\n基于 Python tkinter 开发\n仅供演示使用")

    def update_status(self, message, color="black"):
        """更新状态标签"""
        self.lbl_status.config(text=message, fg=color)

    def collect_data(self):
        """收集表单数据"""
        # 收集产品数据
        self.product_data['name'] = self.entry_product_name.get()
        self.product_data['type'] = self.combo_product_type.get()
        self.product_data['description'] = self.txt_description.get(1.0, tk.END).strip()

        # 收集配方数据
        self.recipe_data['name'] = self.entry_recipe_name.get()
        self.recipe_data['number'] = self.entry_recipe_number.get()

        # 收集选中的原料
        self.recipe_data['ingredients'] = []
        for i, var in enumerate(self.chk_vars):
            if var.get() == 1:
                self.recipe_data['ingredients'].append(f"原料{chr(65+i)}")

        self.recipe_data['additive'] = self.combo_additive.get()
        self.recipe_data['temperature'] = self.scale_temperature.get()
        self.recipe_data['time'] = int(self.spinbox_time.get())
        self.recipe_data['notes'] = self.txt_notes.get(1.0, tk.END).strip()

    def format_data_to_json(self):
        """格式化数据为JSON"""
        data = {
            "产品信息": self.product_data,
            "配方信息": self.recipe_data
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def show_json_dialog(self, json_data):
        """显示JSON数据对话框"""
        # 创建对话框窗口
        dialog = tk.Toplevel(self.root)
        dialog.title("保存的数据")
        dialog.geometry("600x450")
        dialog.resizable(True, True)

        # 将对话框居中显示在主窗体中央
        dialog.update_idletasks()

        # 获取主窗体位置和大小
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # 获取对话框大小
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()

        # 计算居中位置
        x = root_x + (root_width // 2) - (dialog_width // 2)
        y = root_y + (root_height // 2) - (dialog_height // 2)

        # 确保对话框不会超出屏幕边界
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        if x < 0:
            x = 0
        elif x + dialog_width > screen_width:
            x = screen_width - dialog_width

        if y < 0:
            y = 0
        elif y + dialog_height > screen_height:
            y = screen_height - dialog_height

        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        # 创建主容器
        main_frame = tk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 文本框框架
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # 添加文本框显示JSON数据
        txt_json = tk.Text(text_frame, font=("Consolas", 10))
        txt_json.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar = tk.Scrollbar(text_frame, command=txt_json.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        txt_json.config(yscrollcommand=scrollbar.set)
        txt_json.insert(1.0, json_data)
        txt_json.config(state=tk.DISABLED)

        # 按钮框架
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # 添加关闭按钮
        btn_close = tk.Button(button_frame, text="关闭", width=12,
                            command=dialog.destroy)
        btn_close.pack()

        # 设置对话框为模态
        dialog.transient(self.root)
        dialog.grab_set()

    def load_sample_data(self):
        """加载示例数据"""
        # 设置产品数据
        self.entry_product_name.insert(0, "示例产品")
        self.combo_product_type.set("液体")
        self.txt_description.insert(1.0, "这是一个示例产品的描述")

        # 设置配方数据
        self.entry_recipe_name.insert(0, "示例配方")
        self.entry_recipe_number.insert(0, "001")

        # 选择原料
        self.chk_vars[0].set(1)
        self.chk_vars[2].set(1)

        self.combo_additive.set("添加剂X")
        self.scale_temperature.set(50)
        self.spinbox_time.delete(0, tk.END)
        self.spinbox_time.insert(0, "60")
        self.txt_notes.insert(1.0, "这是一个示例配方的备注")


def main():
    """主函数"""
    root = tk.Tk()
    app = RecipeManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
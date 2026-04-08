#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
包含配方管理客户端的配置信息
"""

# 产品类型配置
PRODUCT_TYPES = ["液体", "固体", "气体", "粉末"]

# 原料配置
INGREDIENTS = ["原料A", "原料B", "原料C", "原料D", "原料E"]

# 添加剂配置
ADDITIVES = ["添加剂X", "添加剂Y", "添加剂Z"]

# 窗口配置
WINDOW_CONFIG = {
    "title": "配方管理客户端",
    "width": 800,
    "height": 600,
    "resizable": True
}

# 字体配置
FONT_CONFIG = {
    "default": ("Arial", 10),
    "bold": ("Arial", 12, "bold"),
    "small": ("Arial", 9)
}

# 颜色配置
COLOR_CONFIG = {
    "default": "black",
    "success": "green",
    "error": "red",
    "warning": "orange",
    "info": "blue"
}
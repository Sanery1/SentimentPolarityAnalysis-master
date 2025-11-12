#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单运行脚本 - 测试情感分析功能
"""

import sys
import os

# 确保可以导入 spa 模块
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from spa.classifiers import DictClassifier


def test_dict_classifier():
    """测试基于词典的分类器"""
    print("=" * 60)
    print("测试基于词典的情感分类器 (DictClassifier)")
    print("=" * 60)
    
    # 初始化分类器
    print("\n正在初始化分类器...")
    ds = DictClassifier()
    print("分类器初始化完成！")
    
    # 测试句子
    test_sentences = [
        "剁椒鸡蛋好咸,土豆丝很好吃",
        "要是米饭再多点儿就好了",
        "要是米饭再多点儿就更好了",
        "不太好吃，相当难吃，要是米饭再多点儿就好了",
        "味道很好，服务也不错",
        "太难吃了，再也不来了",
        "一般般，没什么特色",
        "非常满意，下次还会再来"
    ]
    
    print("\n开始测试句子分类:")
    print("-" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        result = ds.analyse_sentence(sentence)
        sentiment = "正面 (Positive)" if result == 1 else "负面 (Negative)"
        print(f"\n句子 {i}: {sentence}")
        print(f"分类结果: {sentiment} ({result})")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


def main():
    """主函数"""
    try:
        test_dict_classifier()
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

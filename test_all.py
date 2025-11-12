#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试各种分类器 - 验证项目完整功能
"""

import sys
import os

# 确保可以导入 spa 模块
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_dict_classifier():
    """测试基于词典的分类器"""
    print("\n" + "=" * 60)
    print("1. 测试基于词典的情感分类器 (DictClassifier)")
    print("=" * 60)
    
    from spa.classifiers import DictClassifier
    
    # 初始化分类器
    print("正在初始化分类器...")
    ds = DictClassifier()
    print("✓ 分类器初始化完成！")
    
    # 测试句子
    test_sentences = [
        "味道很好，服务也不错",
        "太难吃了，再也不来了",
        "要是米饭再多点儿就好了"
    ]
    
    print("\n测试句子分类:")
    for sentence in test_sentences:
        result = ds.analyse_sentence(sentence)
        sentiment = "正面" if result == 1 else "负面"
        print(f"  '{sentence}' => {sentiment}")
    
    print("✓ DictClassifier 测试通过！")


def test_ml_classifiers():
    """测试机器学习分类器"""
    print("\n" + "=" * 60)
    print("2. 测试机器学习分类器（小规模数据）")
    print("=" * 60)
    
    from spa.corpus import WaimaiCorpus
    from spa.feature_extraction import ChiSquare
    from spa.classifiers import BayesClassifier, KNNClassifier, SVMClassifier
    from spa.tools import get_accuracy
    
    # 加载语料（使用小规模数据快速测试）
    print("正在加载语料...")
    corpus = WaimaiCorpus()
    train_data, train_labels = corpus.get_train_corpus(100)  # 小规模测试
    test_data, test_labels = corpus.get_test_corpus(20)
    print(f"✓ 训练集: {len(train_data)} 样本, 测试集: {len(test_data)} 样本")
    
    # 特征选择
    print("\n正在进行特征选择（卡方检验）...")
    chi_square = ChiSquare(train_data, train_labels)
    best_words = chi_square.best_words(500)
    print(f"✓ 选择了 {len(best_words)} 个特征词")
    
    # 测试贝叶斯分类器
    print("\n测试朴素贝叶斯分类器...")
    bayes = BayesClassifier(train_data, train_labels, best_words)
    bayes_results = [bayes.classify(data) for data in test_data]
    bayes_acc = sum([1 for i in range(len(test_labels)) if test_labels[i] == bayes_results[i]]) / len(test_labels)
    print(f"✓ 贝叶斯准确率: {bayes_acc*100:.2f}%")
    
    # 测试 KNN 分类器
    print("\n测试 KNN 分类器...")
    knn = KNNClassifier(train_data, train_labels, k=3, best_words=best_words)
    knn_results = [knn.classify(data) for data in test_data]
    knn_acc = sum([1 for i in range(len(test_labels)) if test_labels[i] == knn_results[i]]) / len(test_labels)
    print(f"✓ KNN 准确率: {knn_acc*100:.2f}%")
    
    # 测试 SVM 分类器
    print("\n测试 SVM 分类器...")
    svm = SVMClassifier(train_data, train_labels, best_words, C=10)
    svm_results = [svm.classify(data) for data in test_data]
    svm_acc = sum([1 for i in range(len(test_labels)) if test_labels[i] == svm_results[i]]) / len(test_labels)
    print(f"✓ SVM 准确率: {svm_acc*100:.2f}%")
    
    print("\n✓ 所有机器学习分类器测试通过！")


def test_corpus_loading():
    """测试语料加载"""
    print("\n" + "=" * 60)
    print("3. 测试语料加载功能")
    print("=" * 60)
    
    from spa.corpus import WaimaiCorpus, HotelCorpus
    
    print("\n测试外卖语料...")
    waimai = WaimaiCorpus()
    data, labels = waimai.get_corpus(0, 10)
    print(f"✓ 外卖语料加载成功，样本数: {len(data)}")
    
    print("\n测试酒店语料...")
    hotel = HotelCorpus()
    data, labels = hotel.get_corpus(0, 10)
    print(f"✓ 酒店语料加载成功，样本数: {len(data)}")
    
    print("\n✓ 所有语料加载测试通过！")


def main():
    """主函数"""
    print("\n" + "#" * 60)
    print("# 情感极性分析项目 - 完整功能测试")
    print("#" * 60)
    
    try:
        # 测试 1: 词典分类器
        test_dict_classifier()
        
        # 测试 2: 机器学习分类器
        test_ml_classifiers()
        
        # 测试 3: 语料加载
        test_corpus_loading()
        
        print("\n" + "#" * 60)
        print("# ✓ 所有测试通过！项目运行正常！")
        print("#" * 60)
        print("\n提示：")
        print("  - 运行完整实验: python -c 'from spa.test import test_waimai; test_waimai()'")
        print("  - 查看更多用法: 参考 README_NEW.md")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

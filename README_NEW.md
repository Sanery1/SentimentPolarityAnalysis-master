# 情感极性分析 (Sentiment Polarity Analysis)

中英文情感分析项目，支持多种机器学习算法和基于词典的规则方法。

## 📋 项目结构

```
SentimentPolarityAnalysis-master/
├── spa/                          # 主要代码包
│   ├── __init__.py              # 包初始化文件
│   ├── classifiers.py           # 分类器实现（词典、KNN、贝叶斯、MaxEnt、SVM）
│   ├── corpus.py                # 语料加载工具
│   ├── feature_extraction.py   # 特征选择（卡方检验）
│   ├── tools.py                 # 评估指标和文件I/O
│   ├── test.py                  # 实验脚本
│   ├── f_corpus/                # 训练/测试语料
│   │   ├── ch_hotel_corpus.txt
│   │   ├── ch_waimai_corpus.txt
│   │   ├── en_movie_corpus.txt
│   │   └── ...
│   ├── f_dict/                  # 情感词典资源
│   │   ├── positive_dict.txt
│   │   ├── negative_dict.txt
│   │   ├── phrase_dict.txt
│   │   ├── adverb_dict.txt
│   │   ├── denial_dict.txt
│   │   └── user.dict
│   └── f_runout/                # 实验结果输出目录
├── run_demo.py                  # 快速演示脚本
├── requirements.txt             # Python 依赖
└── README.md                    # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- numpy
- scikit-learn
- jieba（中文分词）
- xlwt（Excel 输出）

### 2. 运行演示

```bash
python run_demo.py
```

这会运行基于词典的情感分类器，对几个示例句子进行分析。

### 3. 使用示例

#### 基于词典的分类器（推荐用于中文）

```python
from spa.classifiers import DictClassifier

# 初始化分类器
classifier = DictClassifier()

# 分析单个句子
sentence = "味道很好，服务也不错"
result = classifier.analyse_sentence(sentence)
print("正面" if result == 1 else "负面")
```

#### 基于机器学习的分类器

```python
from spa.corpus import WaimaiCorpus
from spa.feature_extraction import ChiSquare
from spa.classifiers import BayesClassifier, KNNClassifier, SVMClassifier

# 加载语料
corpus = WaimaiCorpus()
train_data, train_labels = corpus.get_train_corpus(3000)
test_data, test_labels = corpus.get_test_corpus(1000)

# 特征选择（卡方检验）
chi_square = ChiSquare(train_data, train_labels)
best_words = chi_square.best_words(5000)

# 训练分类器（选择一个）
# 1. 朴素贝叶斯
classifier = BayesClassifier(train_data, train_labels, best_words)

# 2. KNN
classifier = KNNClassifier(train_data, train_labels, k=13, best_words=best_words)

# 3. SVM
classifier = SVMClassifier(train_data, train_labels, best_words, C=150)

# 分类
for data in test_data:
    result = classifier.classify(data)
    print("正面" if result == 1 else "负面")
```

## 🔬 支持的分类器

### 1. DictClassifier（基于词典）
- **适用场景**：中文情感分析
- **特点**：
  - 使用情感词典 + 规则
  - 支持副词、否定词、连词的权重修正
  - 识别特殊句式（如"如果…就好了"）
  - 无需训练数据

### 2. BayesClassifier（朴素贝叶斯）
- **特点**：快速、简单、效果好
- **适用场景**：文本分类基线

### 3. KNNClassifier（K近邻）
- **特点**：支持单个或多个 K 值
- **参数**：k（邻居数量）

### 4. MaxEntClassifier（最大熵）
- **特点**：GIS 算法实现
- **参数**：max_iter（最大迭代次数）
- **注意**：纯 Python 实现，训练较慢

### 5. SVMClassifier（支持向量机）
- **特点**：基于 sklearn.svm.SVC
- **参数**：C（正则化参数）

## 📊 评估指标

使用 `spa.tools.get_accuracy` 可以计算：
- Precision（精确率）
- Recall（召回率）
- F1-score
- 总体准确率

结果自动保存为 Excel 文件（.xls）。

## 🗂️ 数据集

项目内置多个数据集：
- **中文**：
  - 外卖评论（WaimaiCorpus, Waimai2Corpus）
  - 酒店评论（HotelCorpus）
- **英文**：
  - 电影评论（MovieCorpus, Movie2Corpus）

语料格式：每行以 `pos` 或 `neg` 开头，后接分词后的 token。

## 🛠️ 运行实验

编辑 `spa/test.py` 中的函数来运行不同实验：

```python
# 运行酒店语料实验
from spa.test import test_hotel
test_hotel()

# 运行外卖语料实验
from spa.test import test_waimai
test_waimai()

# 测试词典分类器
from spa.test import test_dict
test_dict()
```

## 📝 技术要点

### 特征工程
- **卡方检验（Chi-Square）**：选择与正类最相关的 top-N 特征词
- **词频向量化**：将文本转换为基于 best_words 的计数向量

### 词典规则（DictClassifier）
- **情感词典**：正向词、负向词，每个词带权重
- **修饰词**：副词（程度）、否定词（取反）
- **局部窗口**：向前检查 3 个词的副词/否定词影响
- **句式识别**：正则匹配特殊句式并调整分值
- **子句分割**：按标点拆分后逐子句分析

### 文本预处理
- **中文**：jieba 分词 + 用户词典
- **英文**：正则表达式提取 token

## ⚙️ 配置与自定义

### 修改超参数

在 `spa/test.py` 中调整：
```python
train_num = 3000      # 训练样本数
test_num = 1000       # 测试样本数
feature_num = 5000    # 特征词数量
max_iter = 500        # MaxEnt 迭代次数
C = 150               # SVM 正则化参数
k = 13                # KNN 的 K 值
```

### 添加新词典

编辑 `spa/f_dict/` 下的词典文件：
- 格式：`词语<空格>权重`
- 例如：`很 2.0`（副词，程度加强）

## 📈 性能提示

1. **特征选择很重要**：使用卡方检验选择 3000-5000 个特征可显著提升性能
2. **词典分类器**：适合中文且无需训练，但规则维护成本高
3. **朴素贝叶斯**：速度快，基线好，推荐首先尝试
4. **SVM**：通常效果最好，但训练时间较长
5. **MaxEnt**：纯 Python 实现较慢，建议用 sklearn 的 LogisticRegression 替代

## 🔧 常见问题

### 问题：找不到模块 'jieba'
```bash
pip install jieba
```

### 问题：路径错误
确保从项目根目录运行，或使用：
```python
import sys
sys.path.insert(0, '/path/to/SentimentPolarityAnalysis-master')
```

### 问题：中文显示乱码
确保文件编码为 UTF-8，控制台支持中文显示。

## 📄 License

本项目用于学习和研究目的。

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📚 参考

- jieba 中文分词：https://github.com/fxsjy/jieba
- scikit-learn：https://scikit-learn.org/

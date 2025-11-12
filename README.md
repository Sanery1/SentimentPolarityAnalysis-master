# 🎭 情感极性分析系统

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

基于情感词典和机器学习的中英文文本情感分析系统，支持命令行和 Web 界面两种使用方式。

## 📋 目录

- [功能特点](#功能特点)
- [快速开始](#快速开始)
- [系统要求](#系统要求)
- [安装部署](#安装部署)
- [使用方法](#使用方法)
- [项目结构](#项目结构)
- [技术说明](#技术说明)
- [常见问题](#常见问题)

## ✨ 功能特点

### 核心功能
- 🎯 **多算法支持**：词典规则、朴素贝叶斯、KNN、SVM、最大熵
- 🌐 **双语支持**：中文和英文情感分析
- 💻 **Web 界面**：美观的交互式网页，支持单句和批量分析
- 📊 **批量处理**：支持批量文本分析和结果导出
- 📈 **完整评估**：Precision、Recall、F1-score 等指标

### 技术特色
- 🔍 **卡方特征选择**：智能筛选最有效的特征词
- 📝 **中文分词**：基于 jieba 的高性能分词
- 🎨 **可视化结果**：彩色界面展示分析结果
- 🚀 **高性能**：分类器单例模式，响应速度快
- 📱 **响应式设计**：自适应 PC、平板、手机屏幕

## 🚀 快速开始

### 方法一：Web 界面（推荐）⭐

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务器
python app.py

# 3. 在浏览器打开
# http://localhost:5000
```

**Windows 用户**可以直接双击 `启动Web服务.bat` 一键启动！

### 方法二：命令行使用

```python
from spa.classifiers import DictClassifier

# 初始化分类器
classifier = DictClassifier()

# 分析文本
result = classifier.analyse_sentence("味道很好，服务也不错")
print("正面" if result == 1 else "负面")  # 输出：正面
```

## 💻 系统要求

### 最低配置
- **操作系统**：Windows 10+ / macOS 10.14+ / Linux
- **Python**：3.7 或更高版本
- **内存**：至少 2GB RAM
- **存储**：至少 500MB 可用空间

### 推荐配置
- **Python**：3.8 - 3.10
- **内存**：4GB+ RAM
- **处理器**：多核 CPU（用于并行处理）

## 📦 安装部署

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

依赖包列表：
- `numpy>=1.19.0` - 数值计算
- `scikit-learn>=0.24.0` - 机器学习算法
- `jieba>=0.42.0` - 中文分词
- `xlwt>=1.3.0` - Excel 输出
- `flask>=2.0.0` - Web 框架
- `flask-cors>=3.0.0` - 跨域支持

### 2. 验证安装

```bash
# 测试命令行版本
python run_demo.py

# 测试 Web 版本
python app.py
# 然后访问 http://localhost:5000
```

### 3. 生产环境部署（可选）

使用 Gunicorn 部署：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务（4个工作进程）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

使用 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 📖 使用方法

### Web 界面使用

1. **启动服务器**
   ```bash
   python app.py
   ```

2. **访问界面**
   - 在浏览器打开 http://localhost:5000
   - 你会看到一个漂亮的紫色渐变界面

3. **单句分析**
   - 在文本框输入要分析的句子
   - 点击「🔍 分析情感」按钮
   - 查看结果（正面/负面）

4. **批量分析**
   - 在批量分析区域输入多个句子
   - 点击「➕ 添加」添加到列表
   - 点击「🚀 批量分析」一次性分析所有文本

5. **快速示例**
   - 点击页面上的示例按钮快速体验

### API 调用

#### 单句分析

```python
import requests

url = "http://localhost:5000/api/analyze"
data = {"text": "味道很好，服务也不错"}
response = requests.post(url, json=data)
result = response.json()

print(result['label'])  # 输出：正面 😊
```

#### 批量分析

```python
import requests

url = "http://localhost:5000/api/batch_analyze"
data = {
    "texts": [
        "味道很好，服务也不错",
        "太难吃了，再也不来了",
        "一般般，没什么特色"
    ]
}
response = requests.post(url, json=data)
results = response.json()

for item in results['results']:
    print(f"{item['text']} => {item['label']}")
```

### 命令行使用

#### 基于词典的分类器

```python
from spa.classifiers import DictClassifier

# 初始化
classifier = DictClassifier()

# 单句分析
result = classifier.analyse_sentence("味道很好，服务也不错")
print("正面" if result == 1 else "负面")

# 分析文件
results = classifier.analysis_file(
    filepath_in="input.txt",
    filepath_out="output.txt",
    encoding="utf-8"
)
```

#### 机器学习分类器

```python
from spa.corpus import WaimaiCorpus
from spa.feature_extraction import ChiSquare
from spa.classifiers import BayesClassifier, KNNClassifier, SVMClassifier

# 1. 加载语料
corpus = WaimaiCorpus()
train_data, train_labels = corpus.get_train_corpus(1000)
test_data, test_labels = corpus.get_test_corpus(200)

# 2. 特征选择
chi_square = ChiSquare(train_data, train_labels)
best_words = chi_square.best_words(2000)

# 3. 训练分类器
# 朴素贝叶斯
classifier = BayesClassifier(train_data, train_labels, best_words)

# 或 KNN
# classifier = KNNClassifier(train_data, train_labels, k=13, best_words=best_words)

# 或 SVM
# classifier = SVMClassifier(train_data, train_labels, best_words, C=150)

# 4. 预测
for data in test_data[:5]:
    result = classifier.classify(data)
    print("正面" if result == 1 else "负面")
```

#### 运行完整实验

```python
# 编辑 spa/test.py 中的函数
from spa.test import test_waimai, test_hotel, test_dict

# 运行不同数据集的实验
test_waimai()   # 外卖数据集
test_hotel()    # 酒店数据集
test_dict()     # 词典方法
```

## 📂 项目结构

```
SentimentPolarityAnalysis/
├── app.py                      # Flask Web 服务器
├── run_demo.py                 # 命令行演示脚本
├── requirements.txt            # Python 依赖列表
├── README.md                   # 项目说明文档
├── 使用指南.md                  # 详细使用指南
├── 启动Web服务.bat              # Windows 启动脚本
│
├── templates/                  # Web 模板
│   └── index.html             # 前端页面
│
├── spa/                        # 核心代码包
│   ├── __init__.py            # 包初始化
│   ├── classifiers.py         # 分类器实现
│   │   ├── DictClassifier     # 基于词典
│   │   ├── BayesClassifier    # 朴素贝叶斯
│   │   ├── KNNClassifier      # K近邻
│   │   ├── MaxEntClassifier   # 最大熵
│   │   └── SVMClassifier      # 支持向量机
│   │
│   ├── corpus.py              # 语料加载
│   │   ├── WaimaiCorpus       # 外卖评论
│   │   ├── HotelCorpus        # 酒店评论
│   │   ├── MovieCorpus        # 电影评论（英文）
│   │   └── Movie2Corpus       # 电影评论v2
│   │
│   ├── feature_extraction.py # 特征选择
│   │   └── ChiSquare          # 卡方检验
│   │
│   ├── tools.py               # 工具函数
│   │   ├── get_accuracy       # 计算准确率
│   │   └── Write2File         # 文件输出
│   │
│   ├── test.py                # 实验脚本
│   │
│   ├── f_corpus/              # 训练/测试语料
│   │   ├── ch_hotel_corpus.txt
│   │   ├── ch_waimai_corpus.txt
│   │   ├── ch_waimai2_corpus.txt
│   │   ├── en_movie_corpus.txt
│   │   └── en_movie2_corpus.txt
│   │
│   ├── f_dict/                # 情感词典资源
│   │   ├── positive_dict.txt  # 正向词典
│   │   ├── negative_dict.txt  # 负向词典
│   │   ├── adverb_dict.txt    # 副词词典
│   │   ├── denial_dict.txt    # 否定词词典
│   │   ├── conjunction_dict.txt  # 连词词典
│   │   ├── punctuation_dict.txt  # 标点词典
│   │   ├── phrase_dict.txt    # 短语词典
│   │   └── user.dict          # 用户词典
│   │
│   └── f_runout/              # 实验结果输出
│
└── files/                      # 其他资源文件
    └── pic/                   # 图片资源
```

## 🔬 技术说明

### 支持的分类器

| 分类器 | 类名 | 特点 | 适用场景 |
|--------|------|------|----------|
| 词典规则 | `DictClassifier` | 无需训练，基于规则 | 中文情感分析，快速部署 |
| 朴素贝叶斯 | `BayesClassifier` | 快速、简单、效果好 | 文本分类基线 |
| K近邻 | `KNNClassifier` | 直观、易理解 | 小规模数据集 |
| 最大熵 | `MaxEntClassifier` | 理论完善 | 研究和学习 |
| 支持向量机 | `SVMClassifier` | 效果通常最好 | 生产环境 |

### 词典规则方法（DictClassifier）

**核心机制：**
1. **情感词典**：包含正向词和负向词，每个词带权重
2. **副词修正**：程度副词增强情感强度（如"很"、"非常"）
3. **否定词处理**：否定词反转情感极性（如"不"、"没有"）
4. **局部窗口**：检查情感词前3个词的修饰作用
5. **句式识别**：识别特殊句式（如"如果...就好了"）
6. **子句分析**：按标点拆分句子，逐个分析

**优点：**
- ✅ 无需训练数据
- ✅ 可解释性强
- ✅ 适合中文分析
- ✅ 快速部署

**局限：**
- ❌ 词典维护成本高
- ❌ 难以处理复杂语境
- ❌ 准确率依赖词典质量

### 机器学习方法

**特征工程：**
- **卡方检验（Chi-Square）**：选择与分类最相关的 top-N 特征词
- **词频向量化**：将文本转换为基于特征词的数值向量

**分类算法：**
- **朴素贝叶斯**：基于词频概率，使用 log 概率避免下溢
- **KNN**：基于欧氏距离，支持单个或多个 K 值
- **SVM**：使用 sklearn.svm.SVC，支持参数 C 调优
- **最大熵**：GIS 算法实现（纯 Python，较慢）

### 数据集

| 数据集 | 语言 | 类别 | 规模 | 说明 |
|--------|------|------|------|------|
| 外卖评论 | 中文 | 正/负 | 8000条 | WaimaiCorpus |
| 酒店评论 | 中文 | 正/负 | 6000条 | HotelCorpus |
| 电影评论 | 英文 | 正/负 | 2000条 | MovieCorpus |

**语料格式：**
```
pos	味道	很	好	服务	也	不错
neg	太	难吃	了	再也	不	来	了
```

每行以 `pos`（正面）或 `neg`（负面）开头，后接分词后的 token。

### 评估指标

```python
from spa.tools import get_accuracy

results = get_accuracy(
    origin_labels=test_labels,
    classify_labels=predictions,
    parameters=[train_num, test_num, feature_num]
)
```

**输出指标：**
- **Precision（精确率）**：预测为正的样本中实际为正的比例
- **Recall（召回率）**：实际为正的样本中被正确预测的比例
- **F1-score**：精确率和召回率的调和平均
- **总体准确率**：正确预测的样本占总样本的比例

## 🐛 常见问题

### Q1: 启动时报错 "ModuleNotFoundError: No module named 'flask'"

**解决方法：**
```bash
pip install flask flask-cors
```

### Q2: 页面显示空白或无法访问

**检查清单：**
1. 确认服务器已启动（终端有输出）
2. 检查访问地址是否正确（http://localhost:5000）
3. 检查防火墙设置
4. 尝试使用 http://127.0.0.1:5000

### Q3: 中文显示乱码

**解决方法：**
- 确保所有文件使用 UTF-8 编码
- Windows 用户在终端运行：`chcp 65001`

### Q4: 词典分类器找不到词典文件

**原因：** 路径问题（已修复）

**验证：**
```python
from spa.classifiers import DictClassifier
classifier = DictClassifier()  # 应该能正常初始化
```

### Q5: 分析速度很慢

**优化建议：**
1. **首次加载慢**：分类器初始化需要时间，后续会快很多
2. **使用缓存**：保持服务器运行，利用单例模式
3. **减少特征数**：特征选择时使用较少的特征词（如 2000-3000）
4. **使用更快的算法**：朴素贝叶斯 > SVM > KNN

### Q6: 如何在局域网内访问

**方法：**
1. 确保服务器绑定到 `0.0.0.0`（已默认）
2. 查看本机 IP 地址：
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` 或 `ip addr`
3. 在其他设备访问：`http://<你的IP>:5000`

### Q7: 如何添加自己的词典

**步骤：**
1. 编辑 `spa/f_dict/` 下的相应文件
2. 格式：`词语 权重`（用空格或制表符分隔）
3. 示例：
   ```
   很好 2.0
   非常棒 2.5
   难吃 -2.0
   ```

### Q8: 如何使用自己的数据集

**方法一：使用现有格式**
1. 准备数据文件，格式与 `f_corpus/*.txt` 相同
2. 每行：`pos/neg <tab> token1 <tab> token2 ...`
3. 参考 `spa/corpus.py` 创建自己的 Corpus 类

**方法二：直接使用**
```python
from spa.classifiers import BayesClassifier
from spa.feature_extraction import ChiSquare

# 准备数据
train_data = [["词1", "词2", "词3"], ["词4", "词5"]]  # 分词后的列表
train_labels = [1, 0]  # 1=正面，0=负面

# 特征选择
chi = ChiSquare(train_data, train_labels)
best_words = chi.best_words(1000)

# 训练
classifier = BayesClassifier(train_data, train_labels, best_words)
```

## 📊 性能参考

### 词典方法
- **准确率**：70-80%（取决于词典质量）
- **速度**：非常快（< 0.1秒/句）
- **无需训练**

### 机器学习方法

**外卖数据集（3000训练/1000测试）：**
- 朴素贝叶斯：~80-85%
- KNN (k=13)：~75-80%
- SVM (C=150)：~85-90%

**酒店数据集（2200训练/800测试）：**
- 朴素贝叶斯：~85-88%
- SVM：~88-92%

**电影数据集（英文）：**
- 朴素贝叶斯：~75-80%
- SVM：~80-85%

## 🤝 分享和协作

### 分享给他人

**方式一：发送整个项目文件夹**
1. 压缩项目文件夹
2. 发送给对方
3. 对方解压后运行 `pip install -r requirements.txt`
4. 运行 `python app.py`

**方式二：使用 Git**
```bash
# 初始化仓库
git init
git add .
git commit -m "Initial commit"

# 推送到 GitHub
git remote add origin https://github.com/yourusername/yourrepo.git
git push -u origin main

# 对方克隆
git clone https://github.com/yourusername/yourrepo.git
```

**方式三：部署到云服务器**
- 使用 Heroku、AWS、阿里云等云平台
- 提供公网访问地址

### 协作建议

**代码贡献：**
1. Fork 项目
2. 创建新分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "Add your feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

**报告问题：**
- 在 Issues 中描述问题
- 提供错误信息和复现步骤
- 附上系统环境信息

## 📝 License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 👥 作者

- 项目维护者：[您的名字]
- 联系方式：[您的邮箱]

## 🙏 致谢

- jieba 中文分词：https://github.com/fxsjy/jieba
- scikit-learn：https://scikit-learn.org/
- Flask：https://flask.palletsprojects.com/

## 📚 参考文献

如果本项目对您的研究有帮助，请引用：

```bibtex
@software{sentiment_analysis_2025,
  author = {Your Name},
  title = {Sentiment Polarity Analysis System},
  year = {2025},
  url = {https://github.com/yourusername/SentimentPolarityAnalysis}
}
```

---

**最后更新：2025年11月12日**

如有问题或建议，欢迎提交 Issue 或 Pull Request！

## 1、预处理
### （1）、特征提取
- 对应文件：feature_extraction.py

最后结果：

![chi1](files/pic/chi1.png)

X^2值前几名的词语。能看出这些词都是一些有效的情感词。“了”这样的词出现在其中，说明可以去除一些停用词，来进一步提高分类精度。

![chi2](files/pic/chi2.png)

X^2值后几名的词语。能看出这些词的分类作用不是很大。

### （2）、结果评价
- 对应文件：tools.py

结果展示

![evaluation](files/pic/evaluation.PNG)

## 2、基于情感词典的情感极性分析 
—— sentiment analysis based on sentiment dict

- 对应文件：classifier.py  DictClassifier

### 使用1：analyse_sentence
analyse_sentence(sentence, runout_filepath=None, print_show=False)

对单个句子进行情感极性分析

- sentence，待分析的句子

- 若runout_filepath指定，则将分析结果写入该文件；

- 若print_show为True，则在控制台输出分析结果。

运行实例：
    
    d = DictClassifier()
    a_sentence = "剁椒鸡蛋好咸,土豆丝很好吃"
    result = ds.analyse_sentence(a_sentence)
    print(result)

### 使用2:analysis_file
analysis_file(filepath_in, filepath_out, encoding="utf-8", print_show=False, start=0, end=-1)

- filepath_in，待分析的句子文件

- filepath_out，分析结果输出文件

- encoding，输入文件字符编码

- print_show，是否在控制台输出

- start，输入文件开始分析的句子行数

- end，输入文件结束分析的句子行数

输出实例：

    送餐快，态度好！味道不错。
    Score:6.0
    Sub-clause0: positive:快 
    Sub-clause1: positive:好 punctuation:！ 
    Sub-clause2: positive:不错 
    
    还可以，比预计时间晚了一小时到，不过还好
    Score:-0.56
    Sub-clause0: positive:还可以 
    Sub-clause1: negative:晚……小时:晚了一小时 小时 
    Sub-clause2: conjunction:不过 positive:还好


## 3、基于k-NN的情感极性分析 
—— sentiment analysis based on k-NN

### single_k_classify(input_data)

使用单个k值

    k = 3
    
    knn = KNNClassifier(train_data, train_labels, k=2, best_words=best_words)
    classify_labels = []

    print("KNNClassifiers is testing ...")
    for data in self.test_data:
        classify_labels.append(knn.classify(data))
    print("KNNClassifiers tests over.")

    filepath = "f_runout/KNN-train-%d-test-%d-k-%s-%s.xls" % \
               (train_num, test_num, k,
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    results = get_accuracy(test_labels, classify_labels)
    Write2File.write_contents(filepath, results)

### multiple_k_classify(input_data)

使用多个k值

    from spa.classifiers import KNNClassifier
    
    k = [1, 3, 5, 7, 9, 11, 13]
    
    knn = KNNClassifier(train_data, train_labels, k=2, best_words=best_words)
    classify_labels = []

    print("KNNClassifiers is testing ...")
    for data in self.test_data:
        classify_labels.append(knn.classify(data))
    print("KNNClassifiers tests over.")

    filepath = "f_runout/KNN-train-%d-test-%d-k-%s-%s.xls" % \
               (train_num, test_num, '-'.join([str(i) for i in k]),
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    results = get_accuracy(test_labels, classify_labels)
    Write2File.write_contents(filepath, results)

### 比较结论

在某些特定数据下，multiple_k比每个single_k效果要好。但并不是总是最好。


## 4、基于Bayes的情感极性分析 
—— sentiment analysis based on bayes
    
    from spa.classifiers import BayesClassifier
    
    bayes = BayesClassifier(self.train_data, self.train_labels, self.best_words)

    classify_labels = []
    print("BayesClassifier is testing ...")
    for data in self.test_data:
        classify_labels.append(bayes.classify(data))
    print("BayesClassifier tests over.")

    filepath = "f_runout/bayes-train-%d-test-%d-k-%s-%s.xls" % \
               (train_num, test_num, '-'.join([str(i) for i in k]),
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    results = get_accuracy(test_labels, classify_labels)
    Write2File.write_contents(filepath, results)


## 5、基于最大熵的情感极性分析 
—— sentiment analysis based on maximum entropy

### 使用1：得到每次迭代的准确率的变化

![maxent_iteration](files/pic/maxent_iteration.PNG)

    def test_maxent_iteration(self):
        print("MaxEntClassifier iteration")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("maxiter = %s" % self.max_iter)

        from spa.classifiers import MaxEntClassifier

        m = MaxEntClassifier(self.max_iter)
        iter_results = m.test(self.train_data, self.train_labels, self.best_words, self.test_data)

        filepath = "f_runout/MaxEnt-iteration-%s-train-%d-test-%d-f-%d-maxiter-%d-%s.xls" % \
                   (self.type,
                    self.train_num,
                    self.test_num,
                    self.feature_num,
                    self.max_iter,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        results = []
        for i in range(len(iter_results)):
            try:
                results.append(get_accuracy(self.test_labels, iter_results[i], self.parameters))
            except ZeroDivisionError:
                print("ZeroDivisionError")

        Write2File.write_contents(filepath, results)

### 使用2：单个句子的情感极性划分

    def test_maxent(self):
        print("MaxEntClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("maxiter = %s" % self.max_iter)

        from spa.classifiers import MaxEntClassifier

        m = MaxEntClassifier(self.max_iter)
        m.train(self.train_data, self.train_labels, self.best_words)

        print("MaxEntClassifier is testing ...")
        classify_results = []
        for data in self.test_data:
            classify_results.append(m.classify(data))
        print("MaxEntClassifier tests over.")

        filepath = "f_runout/MaxEnt-%s-train-%d-test-%d-f-%d-maxiter-%d-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.max_iter,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_results, 1)


## 6、基于SVM的情感极性分析 
—— sentiment analysis based on SVM

依赖于scikit-learn库。准确率较高！

    def test_svm(self):
        print("SVMClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("C = %s" % self.C)

        from spa.classifiers import SVMClassifier
        svm = SVMClassifier(self.train_data, self.train_labels, self.best_words, self.C)

        classify_labels = []
        print("SVMClassifier is testing ...")
        for data in self.test_data:
            classify_labels.append(svm.classify(data))
        print("SVMClassifier tests over.")

        filepath = "f_runout/SVM-%s-train-%d-test-%d-f-%d-C-%d-%s-lin.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.C,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 2)

## 7、几种情感分析方法比较

### 基于词典
- 准确率：准确率较高（80%以上），随着人工工作量的增加，准确率增加

- 优点：易于理解

- 缺点：人工工作量大

### 基于k_NN
- 准确率：很低（60% - 70%）

- 优点：思想简单、算法简单

- 缺点：准确率低；耗内存；耗时间

### 基于Bayes
- 准确率：还可以（70% - 80%）

- 优点：简单，高效，运算速度快，扩展性好

- 缺点：准确率不高，达不到实用

### 基于最大熵
- 准确率：比较高（83%以上）

- 优点：准确率高

- 缺点：训练时间久

### 基于SVM
- 准确率：最高（85%以上）

- 优点：准确率高

- 缺点：训练耗时

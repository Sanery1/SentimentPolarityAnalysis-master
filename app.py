#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
情感分析 Web 应用 - Flask 后端
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# 确保可以导入 spa 模块
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from spa.classifiers import DictClassifier

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局分类器实例（避免每次请求都重新初始化）
classifier = None


def get_classifier():
    """获取分类器实例（单例模式）"""
    global classifier
    if classifier is None:
        print("正在初始化情感分类器...")
        classifier = DictClassifier()
        print("分类器初始化完成！")
    return classifier


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    """
    情感分析 API
    接收 JSON: {"text": "要分析的文本"}
    返回 JSON: {"success": true, "text": "...", "sentiment": 0/1, "label": "正面/负面"}
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '请提供要分析的文本'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': '文本不能为空'
            }), 400
        
        # 获取分类器并进行分析
        clf = get_classifier()
        result = clf.analyse_sentence(text)
        
        # 构建响应
        response = {
            'success': True,
            'text': text,
            'sentiment': result,
            'label': '正面 😊' if result == 1 else '负面 😞',
            'color': 'success' if result == 1 else 'danger'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/batch_analyze', methods=['POST'])
def batch_analyze():
    """
    批量分析 API
    接收 JSON: {"texts": ["文本1", "文本2", ...]}
    返回 JSON: {"success": true, "results": [...]}
    """
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                'success': False,
                'error': '请提供要分析的文本列表'
            }), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list) or len(texts) == 0:
            return jsonify({
                'success': False,
                'error': '文本列表不能为空'
            }), 400
        
        # 获取分类器
        clf = get_classifier()
        
        # 批量分析
        results = []
        for text in texts:
            text = text.strip()
            if text:
                result = clf.analyse_sentence(text)
                results.append({
                    'text': text,
                    'sentiment': result,
                    'label': '正面' if result == 1 else '负面'
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'classifier': 'loaded' if classifier is not None else 'not_loaded'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("情感分析 Web 应用启动中...")
    print("=" * 60)
    
    # 预加载分类器
    get_classifier()
    
    print("\n服务器启动成功！")
    print("请在浏览器中打开: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

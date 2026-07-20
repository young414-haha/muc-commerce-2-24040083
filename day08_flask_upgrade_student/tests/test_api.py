import sys
import os

# 添加项目根目录到Python路径
# 获取当前文件所在目录的父目录（即项目根目录）
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

import pytest
from app import app

@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-key'
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """测试1：/health 返回200和正确的JSON"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['ok'] == True
    assert data['service'] == 'day08-flask-upgrade'

def test_metrics_unauthorized(client):
    """测试2：未登录访问 /api/metrics 被拦截"""
    response = client.get('/api/metrics')
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location', '')

def test_login_and_metrics(client):
    """测试3：登录后 /api/metrics 返回ok和metrics"""
    # 登录
    login_response = client.post('/login', data={
        'username': 'student',
        'password': 'day07'
    })
    assert login_response.status_code == 302
    
    # 访问指标API
    response = client.get('/api/metrics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['ok'] == True
    assert 'metrics' in data
    assert len(data['metrics']) == 4
    
    # 验证指标数据结构
    for metric in data['metrics']:
        assert 'label' in metric
        assert 'value' in metric
        assert 'note' in metric

def test_categories_filter(client):
    """测试4：/api/categories?category=Fashion 返回筛选结果"""
    # 登录
    client.post('/login', data={
        'username': 'student',
        'password': 'day07'
    })
    
    # 获取所有品类
    response_all = client.get('/api/categories')
    assert response_all.status_code == 200
    data_all = response_all.get_json()
    all_rows = data_all.get('rows', [])
    
    # 获取Fashion品类
    response_fashion = client.get('/api/categories?category=Fashion')
    assert response_fashion.status_code == 200
    data_fashion = response_fashion.get_json()
    assert data_fashion.get('category') == 'Fashion'
    fashion_rows = data_fashion.get('rows', [])
    
    # 验证筛选逻辑
    assert len(fashion_rows) <= len(all_rows)
    
    # 验证品类字段正确
    if len(fashion_rows) > 0:
        for row in fashion_rows:
            assert row.get('偏好品类') == 'Fashion'
# 快速开始指南

5 分钟快速上手 Browser MCP 自动化测试。

## 🚀 三步开始

### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2: 运行示例测试

```bash
pytest tests/test_example.py::TestBasicNavigation::test_navigate_to_website -v
```

### 步骤 3: 编写你的第一个测试

创建 `tests/test_my_test.py`：

```python
import pytest
from src.mcp_client import BrowserMCPClient

@pytest.mark.asyncio
async def test_my_first_test():
    async with BrowserMCPClient() as browser:
        await browser.navigate("https://example.com")
        title = await browser.get_title()
        assert title is not None
```

运行：

```bash
pytest tests/test_my_test.py -v
```

## 📋 常用命令

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_example.py

# 运行特定测试类
pytest tests/test_example.py::TestBasicNavigation

# 运行特定测试用例
pytest tests/test_example.py::TestBasicNavigation::test_navigate_to_website

# 显示详细输出
pytest -v

# 显示 print 输出
pytest -s

# 运行标记为 smoke 的测试
pytest -m smoke

# 并行运行测试（需要 pytest-xdist）
pytest -n auto
```

## 📖 下一步

- 阅读 [USAGE_GUIDE.md](USAGE_GUIDE.md) 了解详细用法
- 查看 [tests/test_example.py](tests/test_example.py) 学习更多示例
- 参考 [README.md](README.md) 了解项目结构

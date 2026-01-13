# Browser MCP 自动化测试框架

这是一个使用 Browser MCP (Model Context Protocol) 进行浏览器自动化测试的示例项目。本项目展示了如何通过 AI 和 MCP 协议来自动生成和执行浏览器测试用例。

## 📋 项目简介

本项目提供了一个完整的测试框架模板，展示了如何使用 Browser MCP 来：
- 自动化浏览器操作（导航、点击、输入等）
- 生成可重复执行的测试用例
- 验证网页功能和交互
- 生成测试报告

## 🚀 快速开始

### 前置要求

1. **Python 3.9+**
2. **Node.js 16+** (用于运行 Browser MCP 服务器)
3. **MCP 服务器配置** (cursor-browser-extension 或 cursor-ide-browser)

### 安装步骤

1. **安装 Python 依赖**
```bash
pip install -r requirements.txt
```

2. **配置 MCP 服务器**
   确保您的编辑器（如 Cursor）已配置 Browser MCP 服务器。通常配置在编辑器的 MCP 设置中。

3. **运行测试**
```bash
pytest tests/ -v
```

## 📁 项目结构

```
browsermcp-automation/
├── README.md                 # 项目说明文档
├── requirements.txt          # Python 依赖
├── .env.example              # 环境变量示例
├── src/
│   ├── __init__.py
│   ├── mcp_client.py         # MCP 客户端封装
│   └── test_utils.py         # 测试工具函数
└── tests/
    ├── __init__.py
    ├── test_example.py       # 示例测试用例
    └── conftest.py           # pytest 配置
```

## 📝 测试用例示例

### 基础测试用例结构

```python
import pytest
from src.mcp_client import BrowserMCPClient

@pytest.mark.asyncio
async def test_example():
    """示例测试用例"""
    async with BrowserMCPClient() as browser:
        # 导航到网页
        await browser.navigate("https://example.com")
        
        # 执行操作
        await browser.click("button#submit")
        
        # 验证结果
        assert await browser.get_text("h1") == "Success"
```

## 🎯 使用场景

1. **功能测试**：验证网页功能是否正常工作
2. **回归测试**：确保新版本没有破坏现有功能
3. **端到端测试**：测试完整的用户流程
4. **UI 测试**：验证界面元素和交互

## 📚 学习资源

- [Browser MCP 文档](https://modelcontextprotocol.io)
- [pytest 文档](https://docs.pytest.org/)
- [Playwright 文档](https://playwright.dev/python/)

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

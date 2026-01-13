# 项目结构说明

## 📁 目录结构

```
browsermcp-automation/
│
├── 📄 README.md                    # 项目主文档
├── 📄 QUICKSTART.md                # 快速开始指南
├── 📄 USAGE_GUIDE.md               # 详细使用指南
├── 📄 PROJECT_STRUCTURE.md         # 本文件：项目结构说明
│
├── 📄 requirements.txt             # Python 依赖包列表
├── 📄 pytest.ini                   # pytest 配置文件
├── 📄 .gitignore                   # Git 忽略文件
├── 📄 .env.example                 # 环境变量示例（如果创建）
│
├── 📁 src/                         # 源代码目录
│   ├── __init__.py                 # Python 包初始化文件
│   ├── mcp_client.py               # Browser MCP 客户端封装
│   └── test_utils.py               # 测试工具函数
│
└── 📁 tests/                       # 测试用例目录
    ├── __init__.py                 # Python 包初始化文件
    ├── conftest.py                 # pytest 配置和共享 fixtures
    └── test_example.py             # 示例测试用例（包含多种场景）
```

## 📝 文件说明

### 核心文件

#### `src/mcp_client.py`
- **作用**：封装 Browser MCP 客户端，提供浏览器操作的高级接口
- **主要类**：`BrowserMCPClient`
- **主要方法**：
  - `navigate()` - 页面导航
  - `click()` - 点击元素
  - `fill()` - 填写输入框
  - `get_text()` - 获取元素文本
  - `screenshot()` - 截取截图
  - `evaluate()` - 执行 JavaScript

#### `src/test_utils.py`
- **作用**：提供测试辅助函数，简化常见操作
- **主要函数**：
  - `wait_for_element_text()` - 等待元素文本
  - `verify_page_url()` - 验证页面 URL
  - `verify_page_title()` - 验证页面标题
  - `fill_form()` - 填写表单
  - `take_screenshot_on_failure()` - 失败时截图

#### `tests/test_example.py`
- **作用**：包含完整的测试用例示例，供学习和参考
- **测试类**：
  - `TestBasicNavigation` - 基础导航测试
  - `TestUserInteraction` - 用户交互测试
  - `TestElementVerification` - 元素验证测试
  - `TestCompleteUserFlow` - 完整用户流程测试
  - `TestErrorHandling` - 错误处理测试
  - `TestAdvancedFeatures` - 高级功能测试
  - `TestSmokeTests` - 冒烟测试

#### `tests/conftest.py`
- **作用**：pytest 配置文件，定义共享的 fixtures
- **主要 fixtures**：
  - `browser` - 浏览器客户端实例
  - `test_urls` - 测试 URL 配置

### 配置文件

#### `pytest.ini`
- pytest 测试框架配置
- 定义测试发现规则
- 配置测试标记（markers）
- 设置默认选项

#### `requirements.txt`
- Python 项目依赖包
- 包含 pytest、pytest-asyncio、mcp 等

#### `.gitignore`
- Git 版本控制忽略文件
- 排除 Python 缓存、虚拟环境、截图等

### 文档文件

#### `README.md`
- 项目概述
- 快速开始指南
- 项目结构说明
- 使用场景介绍

#### `QUICKSTART.md`
- 5 分钟快速上手
- 常用命令参考
- 下一步学习路径

#### `USAGE_GUIDE.md`
- 详细使用指南
- 完整代码示例
- 最佳实践
- 常见问题解答

## 🔄 工作流程

```
1. 编写测试用例 (tests/test_*.py)
   ↓
2. 使用 BrowserMCPClient 进行浏览器操作
   ↓
3. 使用 test_utils 中的工具函数简化操作
   ↓
4. 运行 pytest 执行测试
   ↓
5. 查看测试结果和报告
```

## 🎯 扩展建议

### 添加新功能

1. **新的工具函数**：添加到 `src/test_utils.py`
2. **新的测试用例**：创建 `tests/test_*.py` 文件
3. **新的 fixtures**：添加到 `tests/conftest.py`
4. **新的配置**：更新 `pytest.ini` 或创建配置文件

### 目录扩展

如果需要，可以添加以下目录：

```
browsermcp-automation/
├── config/              # 配置文件目录
│   └── test_config.py
├── fixtures/            # 测试数据目录
│   └── test_data.json
├── reports/             # 测试报告目录
│   └── html/
└── screenshots/         # 截图目录（自动生成）
```

## 📊 代码组织原则

1. **单一职责**：每个文件/函数只做一件事
2. **可复用性**：工具函数放在 `test_utils.py`
3. **清晰命名**：使用描述性的函数和变量名
4. **文档完善**：每个函数都有文档字符串
5. **易于测试**：测试用例结构清晰，易于理解

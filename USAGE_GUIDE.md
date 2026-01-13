# Browser MCP 测试用例使用指南

本指南详细说明如何使用 Browser MCP 编写自动化测试用例，适合 QA 团队学习和参考。

## 📖 目录

1. [基础概念](#基础概念)
2. [环境搭建](#环境搭建)
3. [编写第一个测试用例](#编写第一个测试用例)
4. [常用操作示例](#常用操作示例)
5. [最佳实践](#最佳实践)
6. [常见问题](#常见问题)

## 🎯 基础概念

### 什么是 Browser MCP？

Browser MCP (Model Context Protocol) 是一个协议，允许 AI 助手通过标准化的接口与浏览器进行交互。通过 Browser MCP，我们可以：

- 自动化浏览器操作（导航、点击、输入等）
- 获取页面信息（文本、属性、截图等）
- 执行 JavaScript 代码
- 验证页面状态

### 测试框架结构

```
src/
├── mcp_client.py      # MCP 客户端封装，提供浏览器操作接口
└── test_utils.py      # 测试工具函数，简化常见操作

tests/
├── conftest.py        # pytest 配置和共享 fixtures
└── test_*.py         # 测试用例文件
```

## 🚀 环境搭建

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 2. 配置 MCP 服务器

确保您的编辑器（Cursor/VS Code）已正确配置 Browser MCP 服务器。通常配置在编辑器的 MCP 设置中。

### 3. 验证安装

```bash
# 运行示例测试
pytest tests/test_example.py -v
```

## ✍️ 编写第一个测试用例

### 最简单的测试用例

创建一个新文件 `tests/test_my_first_test.py`：

```python
import pytest
from src.mcp_client import BrowserMCPClient

@pytest.mark.asyncio
async def test_my_first_test():
    """我的第一个测试用例"""
    async with BrowserMCPClient() as browser:
        # 导航到网页
        await browser.navigate("https://example.com")
        
        # 获取页面标题
        title = await browser.get_title()
        
        # 验证标题不为空
        assert title is not None
        print(f"页面标题: {title}")
```

### 运行测试

```bash
pytest tests/test_my_first_test.py -v
```

## 📝 常用操作示例

### 1. 页面导航

```python
# 导航到指定 URL
await browser.navigate("https://example.com")

# 获取当前 URL
current_url = await browser.get_url()
print(f"当前 URL: {current_url}")

# 获取页面标题
title = await browser.get_title()
print(f"页面标题: {title}")
```

### 2. 元素交互

```python
# 点击按钮
await browser.click("button#submit")

# 填写输入框
await browser.fill("input#username", "test_user")

# 等待元素出现
await browser.wait_for_selector("div#content", timeout=5000)

# 获取元素文本
text = await browser.get_text("h1")
```

### 3. 表单操作

```python
from src.test_utils import fill_form

# 使用工具函数填写表单
form_fields = {
    "input#email": "user@example.com",
    "input#password": "password123"
}
await fill_form(browser, form_fields)
```

### 4. 页面验证

```python
from src.test_utils import verify_page_url, verify_page_title

# 验证 URL
assert await verify_page_url(browser, "dashboard")

# 验证标题
assert await verify_page_title(browser, "Dashboard")
```

### 5. 等待操作

```python
from src.test_utils import wait_for_element_text

# 等待元素文本变为期望值
is_match = await wait_for_element_text(
    browser,
    "div#status",
    "Success",
    timeout=10000
)
assert is_match is True
```

### 6. 截图

```python
# 截取页面截图
screenshot_path = await browser.screenshot("screenshots/test.png")

# 失败时自动截图
from src.test_utils import take_screenshot_on_failure

try:
    # 执行可能失败的操作
    await browser.click("button#non-existent")
except Exception as e:
    await take_screenshot_on_failure(browser, "test_name", str(e))
```

### 7. 执行 JavaScript

```python
# 在页面上下文中执行 JavaScript
result = await browser.evaluate("""
    document.querySelector('h1').textContent
""")
print(f"H1 文本: {result}")
```

## 🎨 完整测试用例示例

### 示例 1: 登录流程测试

```python
import pytest
from src.mcp_client import BrowserMCPClient
from src.test_utils import verify_page_url

@pytest.mark.asyncio
async def test_login_flow():
    """测试登录流程"""
    async with BrowserMCPClient() as browser:
        # 1. 导航到登录页
        await browser.navigate("https://example.com/login")
        assert await verify_page_url(browser, "login")
        
        # 2. 填写登录信息
        await browser.fill("input#email", "user@example.com")
        await browser.fill("input#password", "password123")
        
        # 3. 点击登录按钮
        await browser.click("button#login")
        
        # 4. 等待页面跳转
        await browser.wait_for_navigation(timeout=10000)
        
        # 5. 验证登录成功
        assert await verify_page_url(browser, "dashboard")
        
        # 6. 验证欢迎消息
        welcome_text = await browser.get_text("div#welcome")
        assert "Welcome" in welcome_text
```

### 示例 2: 搜索功能测试

```python
@pytest.mark.asyncio
async def test_search_functionality():
    """测试搜索功能"""
    async with BrowserMCPClient() as browser:
        # 导航到主页
        await browser.navigate("https://example.com")
        
        # 输入搜索关键词
        await browser.fill("input#search", "test query")
        
        # 点击搜索按钮
        await browser.click("button#search-submit")
        
        # 等待搜索结果
        await browser.wait_for_selector("div#results", timeout=10000)
        
        # 验证结果存在
        results = await browser.get_text("div#results")
        assert len(results) > 0
```

### 示例 3: 使用 Fixture

```python
# 使用 conftest.py 中定义的 fixture
@pytest.mark.asyncio
async def test_with_fixture(browser):
    """使用 browser fixture"""
    await browser.navigate("https://example.com")
    title = await browser.get_title()
    assert title is not None
```

## ✅ 最佳实践

### 1. 测试用例组织

- **按功能模块分组**：将相关测试放在同一个类中
- **使用描述性名称**：测试函数名应该清楚说明测试内容
- **添加文档字符串**：说明测试的目的和步骤

```python
class TestLogin:
    """登录功能测试"""
    
    @pytest.mark.asyncio
    async def test_successful_login(self, browser):
        """测试：成功登录"""
        # 测试代码
        pass
```

### 2. 等待策略

- **总是等待元素出现**：在操作元素前先等待
- **设置合理的超时时间**：根据网络和页面加载速度调整
- **使用显式等待**：避免使用固定延迟（如 `time.sleep()`）

```python
# 好的做法
await browser.wait_for_selector("button#submit", timeout=5000)
await browser.click("button#submit")

# 不好的做法
import asyncio
await asyncio.sleep(2)  # 固定延迟
await browser.click("button#submit")
```

### 3. 错误处理

- **使用 try-except 处理预期错误**
- **失败时截取截图**：便于调试
- **提供清晰的错误信息**

```python
try:
    await browser.click("button#submit")
except Exception as e:
    await take_screenshot_on_failure(browser, "test_name", str(e))
    raise
```

### 4. 测试数据管理

- **使用配置文件**：将测试数据放在配置文件中
- **使用环境变量**：敏感信息使用环境变量
- **数据驱动测试**：使用 `pytest.mark.parametrize`

```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
@pytest.mark.asyncio
async def test_login_with_different_users(browser, username, password):
    """使用不同用户测试登录"""
    await browser.navigate("https://example.com/login")
    await browser.fill("input#username", username)
    await browser.fill("input#password", password)
    await browser.click("button#login")
```

### 5. 测试标记

使用 pytest 标记来组织测试：

```python
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_homepage_loads(browser):
    """冒烟测试：主页加载"""
    pass

# 运行特定标记的测试
# pytest -m smoke
```

## ❓ 常见问题

### Q1: 如何选择元素选择器？

**A:** 优先使用 ID 选择器，其次是 class 和 data 属性：

```python
# 推荐：ID 选择器
await browser.click("button#submit")

# 推荐：data 属性
await browser.click("button[data-testid='submit']")

# 可用：class 选择器
await browser.click("button.submit-btn")

# 避免：复杂的选择器
await browser.click("div.container > form > button:last-child")
```

### Q2: 测试运行很慢怎么办？

**A:** 
- 减少不必要的等待
- 使用并行执行：`pytest -n auto`
- 只运行相关测试：`pytest tests/test_specific.py`

### Q3: 如何处理动态内容？

**A:** 使用等待函数等待内容加载：

```python
# 等待文本出现
await wait_for_element_text(browser, "div#status", "Loading...", timeout=10000)

# 等待元素可见
await browser.wait_for_selector("div#content", visible=True, timeout=5000)
```

### Q4: 如何调试失败的测试？

**A:**
1. 使用 `-v` 参数查看详细输出：`pytest -v`
2. 使用 `-s` 参数显示 print 输出：`pytest -s`
3. 失败时自动截图
4. 使用 `pytest --pdb` 进入调试模式

### Q5: 如何与 MCP 服务器实际连接？

**A:** 当前实现是示例框架。实际使用时需要：
1. 确保 MCP 服务器在编辑器中正确配置
2. 根据实际的 MCP 协议实现 `BrowserMCPClient` 中的方法
3. 使用 MCP SDK 或客户端库与服务器通信

## 📚 参考资源

- [pytest 官方文档](https://docs.pytest.org/)
- [pytest-asyncio 文档](https://pytest-asyncio.readthedocs.io/)
- [Browser MCP 协议文档](https://modelcontextprotocol.io)
- 项目中的 `tests/test_example.py` 包含更多示例

## 🎓 学习路径

1. **入门**：运行示例测试，理解基本结构
2. **基础**：编写简单的导航和点击测试
3. **进阶**：实现完整的用户流程测试
4. **高级**：使用数据驱动、参数化测试、自定义 fixtures

---

**提示**：遇到问题时，查看 `tests/test_example.py` 中的示例代码，那里包含了各种常见场景的完整示例。

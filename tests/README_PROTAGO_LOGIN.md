# Protago 登录测试使用说明

## 📋 测试概述

本测试文件 (`test_protago_login.py`) 包含针对 **https://xyz-beta.protago-dev.com/** 网站的登录功能测试用例。

## 🎯 测试用例列表

### TestProtagoLogin 类

1. **test_navigate_to_login_page** - 导航到登录页面
   - 验证能够成功访问网站首页

2. **test_login_page_elements_visible** - 验证登录页面元素可见
   - 验证用户名输入框、密码输入框、登录按钮是否可见

3. **test_login_with_credentials** - 使用不同凭证登录（参数化测试）
   - 使用多组用户名和密码组合测试登录功能

4. **test_login_flow_complete** - 完整的登录流程
   - 端到端测试，从访问首页到完成登录

5. **test_login_with_invalid_credentials** - 使用无效凭证登录
   - 验证错误处理功能

6. **test_login_form_validation** - 登录表单验证
   - 验证表单验证功能（如空字段提交）

7. **test_login_page_accessibility** - 登录页面可访问性
   - 验证页面基本可访问性

### TestProtagoLoginE2E 类

8. **test_smoke_login_page_loads** - 冒烟测试
   - 快速验证登录页面能够正常加载

## 🚀 运行测试

### 运行所有 Protago 登录测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行所有登录测试
pytest tests/test_protago_login.py -v

# 运行冒烟测试
pytest tests/test_protago_login.py -m smoke -v

# 运行端到端测试
pytest tests/test_protago_login.py -m e2e -v
```

### 运行特定测试用例

```bash
# 运行单个测试用例
pytest tests/test_protago_login.py::TestProtagoLogin::test_navigate_to_login_page -v

# 运行完整登录流程测试
pytest tests/test_protago_login.py::TestProtagoLogin::test_login_flow_complete -v -s
```

## ⚙️ 配置

### 环境变量配置

创建 `.env` 文件（参考 `.env.example`）：

```bash
# Protago 测试环境 URL
PROTAGO_BASE_URL=https://xyz-beta.protago-dev.com

# 测试账号
PROTAGO_TEST_EMAIL=your_test_email@example.com
PROTAGO_TEST_PASSWORD=your_test_password

# 管理员账号（可选）
PROTAGO_ADMIN_EMAIL=admin@example.com
PROTAGO_ADMIN_PASSWORD=admin_password

# 超时配置（毫秒）
DEFAULT_TIMEOUT=10000
NAVIGATION_TIMEOUT=15000
```

### 配置文件

测试使用 `config.py` 文件管理配置，支持从环境变量读取配置。

## 📝 注意事项

### 1. 选择器调整

**重要**：测试中的 CSS 选择器可能需要根据实际页面结构调整。

当前使用的选择器策略（按优先级）：
- `input[type='email']` - 通过类型选择
- `input[name='email']` - 通过 name 属性选择
- `input#email` - 通过 ID 选择
- `input[placeholder*='email' i]` - 通过 placeholder 选择（不区分大小写）

如果页面结构不同，需要调整选择器。建议：
1. 使用浏览器开发者工具检查实际页面结构
2. 优先使用稳定的选择器（如 `data-testid` 属性）
3. 避免使用可能变化的 CSS 类名

### 2. 真实 MCP 服务器连接

当前实现使用模拟的 Browser MCP 客户端。实际运行时需要：
1. 确保 Browser MCP 服务器已正确配置
2. 在编辑器中启用 Browser MCP 扩展
3. 验证 MCP 服务器连接正常

### 3. 测试账号

- 使用真实的测试账号进行测试
- 不要使用生产环境的真实用户账号
- 建议创建专门的测试账号
- 敏感信息通过环境变量管理，不要提交到代码仓库

### 4. 网络和性能

- 测试可能需要等待页面加载，已设置合理的超时时间
- 如果网络较慢，可以增加超时时间
- 截图功能可以帮助调试测试失败

## 🔧 调试技巧

### 1. 查看详细输出

```bash
# 显示 print 输出
pytest tests/test_protago_login.py -v -s

# 显示更详细的错误信息
pytest tests/test_protago_login.py -v --tb=long
```

### 2. 使用截图

测试失败时会自动截图，保存在 `screenshots/` 目录：
- `screenshots/before_login.png` - 登录前截图
- `screenshots/after_login.png` - 登录后截图
- `screenshots/failure_*.png` - 失败时截图

### 3. 检查页面元素

如果测试失败，可以：
1. 查看截图了解页面状态
2. 使用浏览器开发者工具检查实际的选择器
3. 调整选择器后重新运行测试

## 📊 测试结果示例

```
============================= test session starts ==============================
collected 9 items

tests/test_protago_login.py::TestProtagoLogin::test_navigate_to_login_page PASSED
tests/test_protago_login.py::TestProtagoLogin::test_login_page_elements_visible PASSED
tests/test_protago_login.py::TestProtagoLogin::test_login_with_credentials PASSED
tests/test_protago_login.py::TestProtagoLogin::test_login_flow_complete PASSED
tests/test_protago_login.py::TestProtagoLogin::test_login_with_invalid_credentials PASSED
tests/test_protago_login.py::TestProtagoLogin::test_login_form_validation PASSED
tests/test_protago_login.py::TestProtagoLogin::test_login_page_accessibility PASSED
tests/test_protago_login.py::TestProtagoLoginE2E::test_smoke_login_page_loads PASSED

============================== 8 passed in 15.23s ==============================
```

## 🔄 持续集成

可以将这些测试集成到 CI/CD 流程中：

```yaml
# 示例 GitHub Actions 配置
- name: Run Protago Login Tests
  run: |
    source venv/bin/activate
    pytest tests/test_protago_login.py -v --junitxml=test-results.xml
  env:
    PROTAGO_TEST_EMAIL: ${{ secrets.PROTAGO_TEST_EMAIL }}
    PROTAGO_TEST_PASSWORD: ${{ secrets.PROTAGO_TEST_PASSWORD }}
```

## 📚 相关文档

- [主 README](../README.md) - 项目总体说明
- [使用指南](../USAGE_GUIDE.md) - 详细使用指南
- [快速开始](../QUICKSTART.md) - 快速上手

## ❓ 常见问题

### Q: 测试失败，提示找不到元素？

A: 检查选择器是否正确。使用浏览器开发者工具检查实际页面结构，调整选择器。

### Q: 如何获取实际的页面元素选择器？

A: 
1. 在浏览器中打开网站
2. 按 F12 打开开发者工具
3. 使用元素选择器工具选择目标元素
4. 在 Elements 面板中查看元素的属性
5. 选择最稳定的选择器（优先使用 ID 或 data-testid）

### Q: 测试运行很慢？

A: 
- 检查网络连接
- 适当增加超时时间
- 考虑使用并行测试（需要 pytest-xdist）

### Q: 如何添加新的测试用例？

A: 参考现有测试用例的结构，在 `TestProtagoLogin` 类中添加新的测试方法。

---

**提示**：在实际使用前，请确保已正确配置 Browser MCP 服务器和测试账号信息。

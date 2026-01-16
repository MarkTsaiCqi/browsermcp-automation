# Browser MCP 服务器配置指南

## 🤔 什么是 Browser MCP 服务器？

Browser MCP 服务器是一个**服务程序**，它：
- 运行在后台
- 提供浏览器自动化功能（打开网页、点击、输入等）
- 通过 MCP (Model Context Protocol) 协议与客户端通信
- 通常通过 Cursor 编辑器集成，不需要单独安装

## 📍 你不需要单独安装！

好消息：**通常不需要在本机单独安装 Browser MCP 服务器**。

### 为什么？

Browser MCP 服务器通常有两种方式：

1. **通过 Cursor 编辑器集成**（推荐）
   - Cursor 内置了 Browser MCP 服务器
   - 只需要在 Cursor 设置中启用即可
   - 不需要单独安装

2. **作为独立服务运行**（高级用法）
   - 如果需要独立运行，可能需要安装
   - 但大多数情况下不需要

## 🔧 如何在 Cursor 中配置？

### 方法 1: 检查 Cursor 是否已启用 Browser MCP

1. **打开 Cursor 设置**
   - 按 `Cmd/Ctrl + ,` 打开设置
   - 或点击菜单：`File > Preferences > Settings`

2. **搜索 "MCP" 或 "Browser"**
   - 查看是否有 Browser MCP 相关设置

3. **检查 MCP 服务器列表**
   - 在设置中查找 "MCP Servers" 或类似选项
   - 查看是否有 `cursor-browser-extension` 或 `cursor-ide-browser`

### 方法 2: 检查 Cursor 的 MCP 配置文件

Cursor 的 MCP 配置通常在以下位置：

**macOS/Linux:**
```
~/.cursor/mcp.json
或
~/.config/cursor/mcp.json
```

**Windows:**
```
%APPDATA%\Cursor\mcp.json
```

### 方法 3: 查看 Cursor 的 MCP 状态

在 Cursor 中：
1. 打开命令面板（`Cmd/Ctrl + Shift + P`）
2. 搜索 "MCP" 或 "Browser"
3. 查看是否有相关命令或状态显示

## 🚀 如何验证 Browser MCP 是否可用？

### 方法 1: 在 Cursor 中测试

如果你在 Cursor 中使用 AI 助手（就是我），我可以尝试使用 Browser MCP 工具来访问网页。如果我能成功访问，说明 Browser MCP 已经配置好了。

### 方法 2: 检查 MCP 工具列表

在 Cursor 的 AI 对话中，我可以使用的工具包括：
- `browser_navigate` - 导航到网页
- `browser_click` - 点击元素
- `browser_fill` - 填写表单
- 等等...

如果你看到我能使用这些工具，说明 Browser MCP 已经可用。

## 📝 当前项目的状态

### 当前实现：模拟（Mock）

你的项目目前使用的是**模拟实现**，这意味着：

```python
# src/mcp_client.py 中的代码
async def navigate(self, url: str) -> Dict[str, Any]:
    # 这是模拟实现，不是真实的 MCP 调用
    self._current_url = url
    result = {
        "success": True,
        "url": url,
        "title": "Page Title"  # 模拟值
    }
    return result
```

### 为什么使用模拟？

1. **开发阶段**：不需要真实服务器也能开发和测试代码结构
2. **CI/CD**：可以在没有浏览器环境的情况下运行测试
3. **学习**：可以理解测试框架的工作原理

### 如何切换到真实 MCP？

要使用真实的 Browser MCP，需要修改 `src/mcp_client.py`：

```python
# 需要改为真实的 MCP 协议调用
async def navigate(self, url: str) -> Dict[str, Any]:
    # 这里需要调用真实的 MCP 服务器
    # 例如使用 MCP SDK 或客户端库
    response = await mcp_client.call_tool(
        "browser_navigate",
        {"url": url}
    )
    return response
```

## 🎯 你需要做什么？

### 选项 1: 使用 Cursor 内置的 Browser MCP（推荐）

**步骤**：
1. ✅ 确保你在使用 Cursor 编辑器
2. ✅ 检查 Cursor 是否已启用 Browser MCP（通常默认启用）
3. ✅ 我可以帮你测试 Browser MCP 是否可用
4. ⚠️ 如果需要，修改 `src/mcp_client.py` 使用真实的 MCP 调用

**优点**：
- 不需要额外安装
- 与 Cursor 集成良好
- 使用方便

### 选项 2: 继续使用模拟实现

**适用场景**：
- 学习和理解测试框架
- 开发测试用例结构
- 不需要真正访问网站

**优点**：
- 不需要配置
- 运行快速
- 适合开发阶段

## 🔍 如何检查你的 Cursor 是否支持 Browser MCP？

让我帮你检查一下！我可以尝试使用 Browser MCP 工具来访问一个网页，看看是否可用。

或者，你可以：

1. **在 Cursor 中问我**：
   ```
   你能使用 Browser MCP 访问 https://example.com 吗？
   ```

2. **查看 Cursor 设置**：
   - 打开设置
   - 搜索 "MCP" 或 "Browser"
   - 查看相关配置

3. **查看 Cursor 文档**：
   - 查看 Cursor 的官方文档
   - 了解 Browser MCP 的配置方法

## 💡 建议

### 对于你的项目：

1. **当前阶段**：继续使用模拟实现
   - 测试代码结构已经完成
   - 可以学习和理解框架
   - 不需要额外配置

2. **下一步**：如果需要真正测试网站
   - 检查 Cursor 的 Browser MCP 是否可用
   - 如果可用，我可以帮你修改代码使用真实的 MCP
   - 如果不可用，我们可以继续使用模拟或寻找替代方案

## ❓ 常见问题

### Q: 我需要在服务器上安装 Browser MCP 吗？

A: 不需要。Browser MCP 通常通过 Cursor 编辑器集成，不需要单独安装。

### Q: 如何知道 Browser MCP 是否可用？

A: 在 Cursor 中，我可以尝试使用 Browser MCP 工具。如果我能访问网页，说明可用。

### Q: 如果 Cursor 没有 Browser MCP 怎么办？

A: 可以：
1. 继续使用模拟实现（适合学习和开发）
2. 使用其他浏览器自动化工具（如 Playwright、Selenium）
3. 等待 Cursor 更新支持 Browser MCP

### Q: 模拟实现和真实 MCP 有什么区别？

A:
- **模拟实现**：返回假数据，不真正访问网站
- **真实 MCP**：真正打开浏览器，访问网站，执行操作

## 📚 相关资源

- [MCP 协议文档](https://modelcontextprotocol.io)
- [Cursor 文档](https://cursor.sh/docs)
- 项目中的 `WHAT_WAS_TESTED.md` - 了解当前测试状态

---

**总结**：你**不需要**在本机单独安装 Browser MCP 服务器。它通常通过 Cursor 编辑器集成。如果你想使用真实的 Browser MCP，我们可以检查 Cursor 是否支持，然后修改代码使用真实的 MCP 调用。

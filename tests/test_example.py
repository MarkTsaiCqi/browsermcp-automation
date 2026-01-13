"""Browser MCP 测试用例示例

本文件展示了如何使用 Browser MCP 编写自动化测试用例。
这些测试用例可以作为模板供其他 QA 学习使用。
"""
import pytest
from src.mcp_client import BrowserMCPClient, browser_client
from src.test_utils import (
    wait_for_element_text,
    verify_page_url,
    verify_page_title,
    fill_form,
    take_screenshot_on_failure
)


class TestBasicNavigation:
    """基础导航测试用例"""
    
    @pytest.mark.asyncio
    async def test_navigate_to_website(self, browser):
        """测试：导航到网站
        
        验证浏览器能够成功导航到指定 URL。
        """
        # 导航到目标网站
        result = await browser.navigate("https://example.com")
        
        # 验证导航成功
        assert result["success"] is True
        assert "example.com" in result["url"]
        
        # 验证当前 URL
        current_url = await browser.get_url()
        assert "example.com" in current_url
    
    @pytest.mark.asyncio
    async def test_get_page_title(self, browser):
        """测试：获取页面标题"""
        await browser.navigate("https://example.com")
        
        title = await browser.get_title()
        assert title is not None
        assert len(title) > 0


class TestUserInteraction:
    """用户交互测试用例"""
    
    @pytest.mark.asyncio
    async def test_click_button(self, browser):
        """测试：点击按钮
        
        验证能够成功点击页面上的按钮元素。
        """
        await browser.navigate("https://example.com")
        
        # 等待按钮出现
        await browser.wait_for_selector("button#submit", timeout=5000)
        
        # 点击按钮
        result = await browser.click("button#submit")
        
        # 验证点击成功
        assert result["success"] is True
        assert result["action"] == "click"
    
    @pytest.mark.asyncio
    async def test_fill_input_field(self, browser):
        """测试：填写输入框
        
        验证能够在输入框中填入文本。
        """
        await browser.navigate("https://example.com")
        
        # 填写输入框
        result = await browser.fill("input#username", "test_user")
        
        # 验证填写成功
        assert result["success"] is True
        assert result["text"] == "test_user"
    
    @pytest.mark.asyncio
    async def test_fill_form(self, browser):
        """测试：填写完整表单
        
        使用工具函数填写包含多个字段的表单。
        """
        await browser.navigate("https://example.com/login")
        
        # 定义表单字段
        form_fields = {
            "input#email": "test@example.com",
            "input#password": "password123"
        }
        
        # 填写表单
        results = await fill_form(browser, form_fields)
        
        # 验证所有字段都填写成功
        assert len(results) == len(form_fields)
        for selector, result in results.items():
            assert result["success"] is True


class TestElementVerification:
    """元素验证测试用例"""
    
    @pytest.mark.asyncio
    async def test_get_element_text(self, browser):
        """测试：获取元素文本
        
        验证能够成功获取页面元素的文本内容。
        """
        await browser.navigate("https://example.com")
        
        # 等待元素出现
        await browser.wait_for_selector("h1", timeout=5000)
        
        # 获取文本
        text = await browser.get_text("h1")
        
        # 验证文本不为空
        assert text is not None
        assert len(text) > 0
    
    @pytest.mark.asyncio
    async def test_wait_for_element_text(self, browser):
        """测试：等待元素文本变为期望值
        
        使用工具函数等待元素文本变化。
        """
        await browser.navigate("https://example.com")
        
        # 点击某个按钮，触发文本变化
        await browser.click("button#load-content")
        
        # 等待文本变为期望值
        is_match = await wait_for_element_text(
            browser,
            "div#content",
            "Content Loaded",
            timeout=10000
        )
        
        assert is_match is True
    
    @pytest.mark.asyncio
    async def test_verify_page_url(self, browser):
        """测试：验证页面 URL
        
        使用工具函数验证当前页面 URL。
        """
        await browser.navigate("https://example.com/dashboard")
        
        # 验证 URL 包含期望的部分
        is_correct = await verify_page_url(browser, "dashboard")
        assert is_correct is True


class TestCompleteUserFlow:
    """完整用户流程测试用例"""
    
    @pytest.mark.asyncio
    async def test_login_flow(self, browser):
        """测试：完整的登录流程
        
        这是一个端到端测试示例，展示如何测试完整的用户操作流程。
        """
        # 步骤 1: 导航到登录页面
        await browser.navigate("https://example.com/login")
        assert await verify_page_url(browser, "login")
        
        # 步骤 2: 填写登录表单
        await browser.fill("input#email", "user@example.com")
        await browser.fill("input#password", "secure_password")
        
        # 步骤 3: 点击登录按钮
        await browser.click("button#login")
        
        # 步骤 4: 等待页面跳转
        await browser.wait_for_navigation(timeout=10000)
        
        # 步骤 5: 验证登录成功（跳转到仪表盘）
        assert await verify_page_url(browser, "dashboard")
        
        # 步骤 6: 验证欢迎消息
        welcome_text = await browser.get_text("div#welcome-message")
        assert "Welcome" in welcome_text
    
    @pytest.mark.asyncio
    async def test_search_functionality(self, browser):
        """测试：搜索功能
        
        测试网站搜索功能的完整流程。
        """
        # 导航到主页
        await browser.navigate("https://example.com")
        
        # 在搜索框中输入关键词
        await browser.fill("input#search", "test query")
        
        # 点击搜索按钮
        await browser.click("button#search-submit")
        
        # 等待搜索结果加载
        await browser.wait_for_selector("div#search-results", timeout=10000)
        
        # 验证搜索结果存在
        results_text = await browser.get_text("div#search-results")
        assert len(results_text) > 0


class TestErrorHandling:
    """错误处理测试用例"""
    
    @pytest.mark.asyncio
    async def test_element_not_found(self, browser):
        """测试：处理元素不存在的情况"""
        await browser.navigate("https://example.com")
        
        # 尝试等待一个不存在的元素（应该超时）
        try:
            await browser.wait_for_selector("div#non-existent", timeout=2000)
            # 如果元素找到了，这个测试应该失败
            assert False, "元素不应该存在"
        except Exception:
            # 预期的异常，测试通过
            assert True
    
    @pytest.mark.asyncio
    async def test_screenshot_on_failure(self, browser):
        """测试：失败时截取截图
        
        演示如何在测试失败时自动截取截图用于调试。
        """
        await browser.navigate("https://example.com")
        
        try:
            # 执行可能失败的操作
            await browser.click("button#non-existent")
            assert False, "操作应该失败"
        except Exception as e:
            # 截取截图用于调试
            screenshot_path = await take_screenshot_on_failure(
                browser,
                "test_screenshot_on_failure",
                str(e)
            )
            assert screenshot_path is not None


class TestAdvancedFeatures:
    """高级功能测试用例"""
    
    @pytest.mark.asyncio
    async def test_javascript_execution(self, browser):
        """测试：执行 JavaScript
        
        演示如何在页面上下文中执行 JavaScript 代码。
        """
        await browser.navigate("https://example.com")
        
        # 执行 JavaScript 获取页面信息
        page_info = await browser.evaluate("""
            ({
                url: window.location.href,
                title: document.title,
                userAgent: navigator.userAgent
            })
        """)
        
        assert page_info is not None
    
    @pytest.mark.asyncio
    async def test_screenshot_capture(self, browser):
        """测试：截取页面截图"""
        await browser.navigate("https://example.com")
        
        # 截取截图
        screenshot_path = await browser.screenshot("screenshots/test_page.png")
        
        assert screenshot_path is not None
    
    @pytest.mark.asyncio
    async def test_context_manager_usage(self):
        """测试：使用上下文管理器
        
        演示如何使用 browser_client 便捷函数。
        """
        async with browser_client() as browser:
            await browser.navigate("https://example.com")
            title = await browser.get_title()
            assert title is not None


# 使用 pytest.mark 标记测试
@pytest.mark.smoke
class TestSmokeTests:
    """冒烟测试用例
    
    这些是快速验证系统基本功能的测试用例。
    """
    
    @pytest.mark.asyncio
    async def test_homepage_loads(self, browser):
        """冒烟测试：主页能够正常加载"""
        result = await browser.navigate("https://example.com")
        assert result["success"] is True
        
        title = await browser.get_title()
        assert title is not None

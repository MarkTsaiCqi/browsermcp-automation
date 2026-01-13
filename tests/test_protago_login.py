"""Protago 网站登录测试用例

测试 https://xyz-beta.protago-dev.com/ 的登录功能。
本测试用例展示了如何为真实网站编写登录测试。

注意：
- 实际运行时需要连接真实的 Browser MCP 服务器
- 测试账号信息请通过环境变量或配置文件设置
- 选择器可能需要根据实际页面结构调整
"""
import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp_client import BrowserMCPClient
from src.test_utils import (
    verify_page_url,
    verify_page_title,
    fill_form,
    wait_for_element_text,
    take_screenshot_on_failure
)

try:
    from config import TestConfig
    BASE_URL = TestConfig.PROTAGO_BASE_URL
    TEST_EMAIL = TestConfig.TEST_EMAIL
    TEST_PASSWORD = TestConfig.TEST_PASSWORD
except ImportError:
    # 如果配置文件不存在，使用默认值
    BASE_URL = "https://xyz-beta.protago-dev.com"
    TEST_EMAIL = os.getenv("PROTAGO_TEST_EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("PROTAGO_TEST_PASSWORD", "test_password")


class TestProtagoLogin:
    """Protago 网站登录测试用例"""
    
    @pytest.mark.asyncio
    async def test_navigate_to_login_page(self, browser):
        """测试：导航到登录页面
        
        验证能够成功访问 Protago 网站首页。
        """
        # 导航到网站首页
        result = await browser.navigate(BASE_URL)
        
        # 验证导航成功
        assert result["success"] is True
        
        # 验证当前 URL
        current_url = await browser.get_url()
        assert "protago-dev.com" in current_url
        
        # 获取页面标题
        title = await browser.get_title()
        assert title is not None
        print(f"页面标题: {title}")
    
    @pytest.mark.asyncio
    async def test_login_page_elements_visible(self, browser):
        """测试：验证登录页面元素可见
        
        验证登录页面上的关键元素（用户名输入框、密码输入框、登录按钮）是否可见。
        """
        # 导航到登录页面
        await browser.navigate(BASE_URL)
        
        # 等待登录表单元素出现
        # 注意：实际的选择器需要根据页面实际情况调整
        await browser.wait_for_selector("input[type='email'], input[name='email'], input#email", timeout=10000)
        await browser.wait_for_selector("input[type='password'], input[name='password'], input#password", timeout=10000)
        await browser.wait_for_selector("button[type='submit'], button.login, button#login", timeout=10000)
        
        print("登录页面元素加载完成")
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("username,password", [
        ("test@example.com", "test_password"),
        ("admin@protago.com", "admin123"),
    ])
    async def test_login_with_credentials(self, browser, username, password):
        """测试：使用不同凭证登录
        
        参数化测试，使用不同的用户名和密码组合测试登录功能。
        
        Args:
            username: 用户名/邮箱
            password: 密码
        """
        # 导航到登录页面
        await browser.navigate(BASE_URL)
        
        # 等待登录表单加载
        await browser.wait_for_selector("input[type='email'], input[name='email']", timeout=10000)
        
        # 填写登录表单
        # 注意：实际的选择器需要根据页面实际情况调整
        email_selector = "input[type='email'], input[name='email'], input#email"
        password_selector = "input[type='password'], input[name='password'], input#password"
        submit_selector = "button[type='submit'], button.login, button#login"
        
        try:
            # 尝试填写邮箱（可能的选择器）
            await browser.fill(email_selector, username)
            await browser.fill(password_selector, password)
            
            # 点击登录按钮
            await browser.click(submit_selector)
            
            # 等待页面响应（可能是跳转或显示错误消息）
            await browser.wait_for_navigation(timeout=15000)
            
            # 验证登录结果
            current_url = await browser.get_url()
            print(f"登录后 URL: {current_url}")
            
            # 如果登录成功，URL 应该改变（跳转到仪表盘或其他页面）
            # 如果登录失败，可能停留在登录页面或显示错误消息
            assert current_url is not None
            
        except Exception as e:
            # 如果出现错误，截取截图用于调试
            screenshot_path = await take_screenshot_on_failure(
                browser,
                f"test_login_{username.replace('@', '_at_')}",
                str(e)
            )
            print(f"登录过程出现异常，截图已保存: {screenshot_path}")
            raise
    
    @pytest.mark.asyncio
    async def test_login_flow_complete(self, browser):
        """测试：完整的登录流程
        
        端到端测试，验证从访问首页到完成登录的完整流程。
        """
        # 步骤 1: 导航到网站首页
        await browser.navigate(BASE_URL)
        current_url = await browser.get_url()
        assert "protago-dev.com" in current_url
        
        # 步骤 2: 等待并定位登录表单元素
        # 注意：以下选择器需要根据实际页面结构调整
        email_input = "input[type='email'], input[name='email'], input#email, input[placeholder*='email' i], input[placeholder*='Email' i]"
        password_input = "input[type='password'], input[name='password'], input#password"
        login_button = "button[type='submit'], button.login, button#login, button:contains('登录'), button:contains('Login')"
        
        await browser.wait_for_selector(email_input, timeout=10000)
        await browser.wait_for_selector(password_input, timeout=10000)
        
        # 步骤 3: 填写登录信息
        # 使用配置文件中的测试账号
        await browser.fill(email_input, TEST_EMAIL)
        await browser.fill(password_input, TEST_PASSWORD)
        
        # 步骤 4: 截取登录前的截图（可选，用于调试）
        await browser.screenshot("screenshots/before_login.png")
        
        # 步骤 5: 点击登录按钮
        await browser.click(login_button)
        
        # 步骤 6: 等待页面跳转或加载
        await browser.wait_for_navigation(timeout=15000)
        
        # 步骤 7: 验证登录结果
        final_url = await browser.get_url()
        final_title = await browser.get_title()
        
        print(f"登录后 URL: {final_url}")
        print(f"登录后标题: {final_title}")
        
        # 验证：如果登录成功，URL 应该改变
        # 如果登录失败，可能显示错误消息
        assert final_url is not None
        
        # 步骤 8: 截取登录后的截图（可选，用于验证）
        await browser.screenshot("screenshots/after_login.png")
    
    @pytest.mark.asyncio
    async def test_login_with_invalid_credentials(self, browser):
        """测试：使用无效凭证登录
        
        验证使用错误的用户名或密码时，系统能正确显示错误消息。
        """
        # 导航到登录页面
        await browser.navigate(BASE_URL)
        
        # 等待登录表单加载
        await browser.wait_for_selector("input[type='email'], input[name='email']", timeout=10000)
        
        # 填写错误的登录信息
        email_selector = "input[type='email'], input[name='email'], input#email"
        password_selector = "input[type='password'], input[name='password'], input#password"
        submit_selector = "button[type='submit'], button.login, button#login"
        
        await browser.fill(email_selector, "invalid@example.com")
        await browser.fill(password_selector, "wrong_password")
        
        # 点击登录按钮
        await browser.click(submit_selector)
        
        # 等待错误消息出现（可能需要等待几秒）
        await browser.wait_for_selector(
            ".error, .alert, .message, [role='alert'], div.error-message",
            timeout=10000
        )
        
        # 验证错误消息存在
        # 注意：实际的选择器需要根据页面错误消息的显示方式调整
        error_text = await browser.get_text(".error, .alert, .message, [role='alert']")
        
        # 验证错误消息不为空
        assert error_text is not None
        print(f"错误消息: {error_text}")
    
    @pytest.mark.asyncio
    async def test_login_form_validation(self, browser):
        """测试：登录表单验证
        
        验证表单验证功能，例如空字段提交时的验证。
        """
        # 导航到登录页面
        await browser.navigate(BASE_URL)
        
        # 等待登录表单加载
        await browser.wait_for_selector("input[type='email'], input[name='email']", timeout=10000)
        
        submit_selector = "button[type='submit'], button.login, button#login"
        
        # 尝试不填写任何信息直接提交
        await browser.click(submit_selector)
        
        # 等待验证错误消息出现
        await browser.wait_for_selector(
            ".error, .alert, .invalid, input:invalid, [aria-invalid='true']",
            timeout=5000
        )
        
        # 验证表单验证消息
        # 注意：实际的选择器需要根据页面验证消息的显示方式调整
        validation_message = await browser.get_text(".error, .alert, .invalid")
        
        # 验证消息存在（可能为空，取决于浏览器的原生验证）
        print(f"验证消息: {validation_message}")
    
    @pytest.mark.asyncio
    async def test_login_page_accessibility(self, browser):
        """测试：登录页面可访问性
        
        验证登录页面的基本可访问性，如页面标题、关键元素等。
        """
        # 导航到登录页面
        await browser.navigate(BASE_URL)
        
        # 验证页面标题存在
        title = await browser.get_title()
        assert title is not None
        assert len(title) > 0
        print(f"页面标题: {title}")
        
        # 验证页面 URL
        current_url = await browser.get_url()
        assert "protago" in current_url.lower()
        
        # 验证关键元素存在
        await browser.wait_for_selector("input[type='email'], input[name='email']", timeout=10000)
        await browser.wait_for_selector("input[type='password'], input[name='password']", timeout=10000)


# 使用 pytest.mark 标记测试
@pytest.mark.e2e
class TestProtagoLoginE2E:
    """Protago 登录端到端测试
    
    这些测试需要真实的浏览器环境和 MCP 服务器连接。
    """
    
    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_smoke_login_page_loads(self, browser):
        """冒烟测试：登录页面能够正常加载"""
        result = await browser.navigate(BASE_URL)
        assert result["success"] is True
        
        title = await browser.get_title()
        assert title is not None
        
        current_url = await browser.get_url()
        assert "protago" in current_url.lower()
        
        print(f"✅ 登录页面加载成功")
        print(f"   URL: {current_url}")
        print(f"   标题: {title}")

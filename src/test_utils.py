"""测试工具函数

提供常用的测试辅助函数和断言方法。
"""
from typing import Any, Dict, Optional
from src.mcp_client import BrowserMCPClient


async def wait_for_element_text(
    browser: BrowserMCPClient,
    selector: str,
    expected_text: str,
    timeout: int = 5000
) -> bool:
    """等待元素文本变为期望值
    
    Args:
        browser: 浏览器客户端实例
        selector: 元素选择器
        expected_text: 期望的文本内容
        timeout: 超时时间（毫秒）
        
    Returns:
        如果文本匹配则返回 True，否则返回 False
    """
    await browser.wait_for_selector(selector, timeout=timeout)
    actual_text = await browser.get_text(selector)
    return actual_text == expected_text


async def verify_page_url(browser: BrowserMCPClient, expected_url: str) -> bool:
    """验证当前页面 URL
    
    Args:
        browser: 浏览器客户端实例
        expected_url: 期望的 URL（可以是部分匹配）
        
    Returns:
        如果 URL 匹配则返回 True
    """
    current_url = await browser.get_url()
    return expected_url in current_url


async def verify_page_title(browser: BrowserMCPClient, expected_title: str) -> bool:
    """验证当前页面标题
    
    Args:
        browser: 浏览器客户端实例
        expected_title: 期望的标题（可以是部分匹配）
        
    Returns:
        如果标题匹配则返回 True
    """
    current_title = await browser.get_title()
    return expected_title in current_title


async def fill_form(
    browser: BrowserMCPClient,
    form_fields: Dict[str, str]
) -> Dict[str, Any]:
    """填充表单字段
    
    Args:
        browser: 浏览器客户端实例
        form_fields: 字段名和值的字典，键为选择器，值为要填入的文本
        
    Returns:
        操作结果字典
    """
    results = {}
    for selector, value in form_fields.items():
        result = await browser.fill(selector, value)
        results[selector] = result
    return results


async def take_screenshot_on_failure(
    browser: BrowserMCPClient,
    test_name: str,
    failure_message: str
) -> str:
    """在测试失败时截取截图
    
    Args:
        browser: 浏览器客户端实例
        test_name: 测试用例名称
        failure_message: 失败信息
        
    Returns:
        截图路径
    """
    screenshot_path = f"screenshots/failure_{test_name}.png"
    await browser.screenshot(screenshot_path)
    return screenshot_path

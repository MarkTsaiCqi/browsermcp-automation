"""pytest 配置和共享 fixtures"""
import pytest
from src.mcp_client import BrowserMCPClient


@pytest.fixture
async def browser():
    """提供浏览器客户端实例的 fixture"""
    async with BrowserMCPClient() as client:
        yield client


@pytest.fixture
def test_urls():
    """测试用的 URL 配置"""
    return {
        "example": "https://example.com",
        "google": "https://www.google.com",
        "github": "https://github.com"
    }

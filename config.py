"""测试配置文件

存储测试相关的配置信息，如测试 URL、测试账号等。
"""
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class TestConfig:
    """测试配置类"""
    
    # Protago 测试环境 URL
    PROTAGO_BASE_URL = os.getenv("PROTAGO_BASE_URL", "https://xyz-beta.protago-dev.com")
    
    # 测试账号配置（从环境变量读取，如果没有则使用默认值）
    TEST_EMAIL = os.getenv("PROTAGO_TEST_EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("PROTAGO_TEST_PASSWORD", "test_password")
    
    # 管理员账号（如果需要）
    ADMIN_EMAIL = os.getenv("PROTAGO_ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.getenv("PROTAGO_ADMIN_PASSWORD", "admin_password")
    
    # 超时配置（毫秒）
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "15000"))
    
    # 截图配置
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")
    
    @classmethod
    def get_test_credentials(cls) -> Dict[str, str]:
        """获取测试账号凭证
        
        Returns:
            包含 email 和 password 的字典
        """
        return {
            "email": cls.TEST_EMAIL,
            "password": cls.TEST_PASSWORD
        }
    
    @classmethod
    def get_admin_credentials(cls) -> Dict[str, str]:
        """获取管理员账号凭证
        
        Returns:
            包含 email 和 password 的字典
        """
        return {
            "email": cls.ADMIN_EMAIL,
            "password": cls.ADMIN_PASSWORD
        }

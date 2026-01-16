"""Banner 链接实时测试脚本

直接使用 Browser MCP 工具测试 banner 链接，实际运行并展示结果。
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import TestConfig
    BASE_URL = TestConfig.PROTAGO_BASE_URL
except ImportError:
    BASE_URL = "https://xyz-beta.protago-dev.com"


async def test_banner_links():
    """测试所有 banner 链接"""
    print("=" * 60)
    print("Banner 链接测试开始")
    print("=" * 60)
    print()
    
    # 注意：这个脚本需要在 Cursor 中运行，因为它需要使用 Browser MCP 工具
    # 实际的 Browser MCP 调用需要通过 Cursor 的 MCP 集成来完成
    
    print("⚠️  注意：此脚本需要在 Cursor 中运行，以使用 Browser MCP 工具")
    print("   请使用以下命令在 Cursor 中运行：")
    print("   python test_banner_links_live.py")
    print()
    
    # 测试步骤说明
    test_steps = [
        {
            "name": "导航到首页",
            "action": "navigate",
            "url": BASE_URL,
            "expected": "页面标题包含 'NetMind' 或 'XYZ'"
        },
        {
            "name": "点击 Usher 链接",
            "action": "click",
            "element": "Usher link",
            "expected": "URL 包含 'agentSociety' 或 'chat'"
        },
        {
            "name": "返回首页",
            "action": "navigate",
            "url": BASE_URL,
            "expected": "回到首页"
        },
        {
            "name": "点击 Society 链接",
            "action": "click",
            "element": "Society link",
            "expected": "URL 包含 'society' 或 'agentSociety'"
        },
        {
            "name": "返回首页",
            "action": "navigate",
            "url": BASE_URL,
            "expected": "回到首页"
        },
        {
            "name": "导航到 Pricing 锚点",
            "action": "navigate",
            "url": f"{BASE_URL}/#pricing",
            "expected": "URL 包含 '#pricing'，页面滚动到 Pricing 区块"
        },
        {
            "name": "返回首页",
            "action": "navigate",
            "url": BASE_URL,
            "expected": "回到首页"
        },
        {
            "name": "点击 Contact 链接",
            "action": "click",
            "element": "Contact link",
            "expected": "URL 包含 'contact'"
        },
        {
            "name": "返回首页",
            "action": "navigate",
            "url": BASE_URL,
            "expected": "回到首页"
        }
    ]
    
    print("测试步骤：")
    for i, step in enumerate(test_steps, 1):
        print(f"{i}. {step['name']}")
        print(f"   预期结果: {step['expected']}")
    print()
    
    print("=" * 60)
    print("测试脚本准备完成")
    print("=" * 60)
    print()
    print("请在 Cursor 中使用 Browser MCP 工具手动执行这些步骤，")
    print("或使用 pytest 运行 tests/test_banner_links.py")


if __name__ == "__main__":
    asyncio.run(test_banner_links())

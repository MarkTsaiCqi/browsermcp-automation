"""Login and check Account page 测试用例

完整的登录流程测试，从首页登录到验证 Account 页面：
1. 连接到首页
2. 点击 Sign Up/Log In 按钮
3. 等待弹窗出现
4. 输入 email 和 password
5. 登录
6. 导航到 Account 页面
7. 验证用户信息（用户名和 email）
"""
import pytest
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import TestConfig
    BASE_URL = TestConfig.PROTAGO_BASE_URL
    # 使用实际的测试账号
    TEST_EMAIL = os.getenv("PROTAGO_TEST_EMAIL", "xyzdev01@cqigames.com")
    TEST_PASSWORD = os.getenv("PROTAGO_TEST_PASSWORD", "Abc123123?")
except ImportError:
    BASE_URL = "https://xyz-beta.protago-dev.com"
    TEST_EMAIL = "xyzdev01@cqigames.com"
    TEST_PASSWORD = "Abc123123?"

# 创建截图目录
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


class TestLoginAndCheckAccountPage:
    """Login and check Account page 测试类"""
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_login_and_verify_account_page(self):
        """测试：登录并验证 Account 页面
        
        完整流程：
        1. 导航到首页
        2. 点击登录按钮并打开弹窗
        3. 输入 email 和 password
        4. 登录成功
        5. 导航到 Account 页面
        6. 验证用户信息
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # 步骤 1: 导航到首页
                print("\n步骤 1: 导航到首页")
                await page.goto(BASE_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step1_homepage.png", full_page=True)
                current_url = page.url
                assert BASE_URL in current_url, f"应该导航到 {BASE_URL}，实际: {current_url}"
                print(f"✅ 首页加载完成: {current_url}")
                
                # 步骤 2: 点击 Sign Up/Log In 按钮
                print("\n步骤 2: 点击 Sign Up/Log In 按钮")
                # 先查找按钮
                button_found = await page.evaluate("""
                    () => {
                        const allElements = document.querySelectorAll('*');
                        for (let el of allElements) {
                            const text = (el.textContent || el.innerText || '').trim();
                            if (text === 'Sign Up / Log In' || 
                                (text.includes('Sign Up') && text.includes('Log In') && text.length < 30)) {
                                let isLeaf = true;
                                for (let child of el.children) {
                                    const childText = (child.textContent || child.innerText || '').trim();
                                    if (childText === text || (childText.includes('Sign Up') && childText.includes('Log In'))) {
                                        isLeaf = false;
                                        break;
                                    }
                                }
                                if (isLeaf && el.tagName !== 'HTML' && el.tagName !== 'BODY') {
                                    return {found: true, tagName: el.tagName, className: el.className};
                                }
                            }
                        }
                        return {found: false};
                    }
                """)
                
                assert button_found.get('found'), "应该找到登录按钮"
                
                # 使用 Playwright 的 click 方法，通过文本定位
                try:
                    login_button = page.locator('text=Sign Up / Log In').first
                    await login_button.wait_for(state='visible', timeout=5000)
                    await login_button.click()
                except:
                    # 如果文本定位失败，使用 JavaScript 点击
                    await page.evaluate("""
                        () => {
                            const allElements = document.querySelectorAll('*');
                            for (let el of allElements) {
                                const text = (el.textContent || el.innerText || '').trim();
                                if (text === 'Sign Up / Log In' || 
                                    (text.includes('Sign Up') && text.includes('Log In') && text.length < 30)) {
                                    let isLeaf = true;
                                    for (let child of el.children) {
                                        const childText = (child.textContent || child.innerText || '').trim();
                                        if (childText === text || (childText.includes('Sign Up') && childText.includes('Log In'))) {
                                            isLeaf = false;
                                            break;
                                        }
                                    }
                                    if (isLeaf && el.tagName !== 'HTML' && el.tagName !== 'BODY') {
                                        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                        setTimeout(() => {
                                            el.click();
                                        }, 500);
                                        return true;
                                    }
                                }
                            }
                            return false;
                        }
                    """)
                
                await page.wait_for_timeout(2000)
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step2_after_click.png", full_page=True)
                print(f"✅ 登录按钮点击成功")
                
                # 步骤 3: 等待弹窗出现
                print("\n步骤 3: 等待弹窗出现")
                await page.wait_for_selector('[role="dialog"]', timeout=5000)
                await page.wait_for_timeout(1000)
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step3_modal_appeared.png", full_page=True)
                print("✅ 弹窗已出现")
                
                # 步骤 4: 输入 email
                print("\n步骤 4: 输入 email")
                email_input = page.locator('input[type="email"], input[placeholder*="email" i], input').first
                await email_input.wait_for(state='visible', timeout=5000)
                await email_input.fill(TEST_EMAIL)
                await page.wait_for_timeout(500)
                
                input_value = await email_input.input_value()
                assert input_value == TEST_EMAIL, f"Email 输入应该为 {TEST_EMAIL}，实际: {input_value}"
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step4_email_entered.png", full_page=True)
                print(f"✅ Email 输入成功: {TEST_EMAIL}")
                
                # 步骤 5: 点击下一步按钮
                print("\n步骤 5: 点击下一步按钮")
                next_button_result = await page.evaluate("""
                    () => {
                        const emailInput = document.querySelector('input[type="email"], input[placeholder*="email" i], input');
                        if (!emailInput) return {found: false};
                        
                        const parent = emailInput.parentElement;
                        const buttons = parent.querySelectorAll('button, [role="button"], svg, [class*="arrow" i]');
                        
                        for (let btn of buttons) {
                            const style = window.getComputedStyle(btn);
                            if (style.display !== 'none' && style.visibility !== 'hidden') {
                                const rect = btn.getBoundingClientRect();
                                const inputRect = emailInput.getBoundingClientRect();
                                if (rect.left > inputRect.right - 50 && rect.top < inputRect.bottom && rect.bottom > inputRect.top) {
                                    btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                    setTimeout(() => {
                                        btn.click();
                                    }, 500);
                                    return {found: true, tagName: btn.tagName};
                                }
                            }
                        }
                        return {found: false};
                    }
                """)
                
                if next_button_result.get('found'):
                    await page.wait_for_timeout(4000)
                    await page.screenshot(path=SCREENSHOT_DIR / "test_login_step5_after_next.png", full_page=True)
                    print("✅ 点击下一步按钮成功")
                else:
                    await email_input.press('Enter')
                    await page.wait_for_timeout(4000)
                    print("✅ 使用 Enter 键触发下一步")
                
                # 步骤 6: 输入 password
                print("\n步骤 6: 输入 password")
                password_input = page.locator('input[type="password"]').first
                await password_input.wait_for(state='visible', timeout=5000)
                await password_input.fill(TEST_PASSWORD)
                await page.wait_for_timeout(500)
                
                input_length = len(await password_input.input_value())
                assert input_length > 0, "Password 应该已输入"
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step6_password_entered.png", full_page=True)
                print(f"✅ Password 输入成功（长度: {input_length}）")
                
                # 步骤 7: 点击登录按钮
                print("\n步骤 7: 点击登录按钮")
                sign_in_button = None
                sign_in_found = False
                
                # 尝试多种方法查找登录按钮
                sign_in_selectors = [
                    'button:has-text("Sign In")',
                    'button:has-text("Log In")',
                    'button:has-text("登录")',
                    'button[type="submit"]',
                    'button.ant-btn-primary',
                    'button[class*="primary" i]'
                ]
                
                for selector in sign_in_selectors:
                    try:
                        test_button = page.locator(selector).first
                        await test_button.wait_for(state='visible', timeout=3000)
                        if await test_button.is_visible():
                            sign_in_button = test_button
                            sign_in_found = True
                            print(f"✅ 找到登录按钮（使用选择器: {selector}）")
                            break
                    except:
                        continue
                
                if not sign_in_found:
                    # 使用 JavaScript 查找并点击
                    print("   尝试使用 JavaScript 查找登录按钮...")
                    await page.wait_for_timeout(1000)
                    button_info = await page.evaluate("""
                        () => {
                            const buttons = document.querySelectorAll('button');
                            for (let btn of buttons) {
                                const style = window.getComputedStyle(btn);
                                if (style.display !== 'none' && style.visibility !== 'hidden') {
                                    const text = (btn.textContent || btn.innerText || '').trim().toLowerCase();
                                    if (text.includes('sign in') || text.includes('登录') || text.includes('log in')) {
                                        return {
                                            found: true,
                                            text: btn.textContent.trim(),
                                            className: btn.className
                                        };
                                    }
                                }
                            }
                            const submitBtn = document.querySelector('button[type="submit"]');
                            if (submitBtn) {
                                const style = window.getComputedStyle(submitBtn);
                                if (style.display !== 'none' && style.visibility !== 'hidden') {
                                    return {
                                        found: true,
                                        text: submitBtn.textContent.trim(),
                                        className: submitBtn.className,
                                        isSubmit: true
                                    };
                                }
                            }
                            return {found: false};
                        }
                    """)
                    print(f"   JavaScript 查找结果: {button_info}")
                    
                    if button_info.get('found'):
                        if button_info.get('isSubmit'):
                            sign_in_button = page.locator('button[type="submit"]').first
                        else:
                            # 尝试通过文本查找
                            button_text = button_info.get('text', '')
                            sign_in_button = page.locator(f'button:has-text("{button_text}")').first
                        try:
                            await page.wait_for_timeout(1000)
                            await sign_in_button.wait_for(state='visible', timeout=5000)
                            if await sign_in_button.is_visible():
                                sign_in_found = True
                                print("✅ 使用 JavaScript 找到登录按钮")
                        except:
                            # 如果还是找不到，直接使用 JavaScript 点击
                            await page.evaluate("""
                                () => {
                                    const buttons = document.querySelectorAll('button');
                                    for (let btn of buttons) {
                                        const style = window.getComputedStyle(btn);
                                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                                            const text = (btn.textContent || btn.innerText || '').trim().toLowerCase();
                                            if (text.includes('sign in') || text.includes('登录') || text.includes('log in')) {
                                                btn.click();
                                                return true;
                                            }
                                        }
                                    }
                                    const submitBtn = document.querySelector('button[type="submit"]');
                                    if (submitBtn) {
                                        const style = window.getComputedStyle(submitBtn);
                                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                                            submitBtn.click();
                                            return true;
                                        }
                                    }
                                    return false;
                                }
                            """)
                            sign_in_found = True
                            print("✅ 使用 JavaScript 直接点击登录按钮")
                
                if sign_in_found:
                    # 使用 JavaScript 直接点击，避免被遮罩层阻挡
                    click_success = await page.evaluate("""
                        () => {
                            const buttons = document.querySelectorAll('button');
                            for (let btn of buttons) {
                                const style = window.getComputedStyle(btn);
                                if (style.display !== 'none' && style.visibility !== 'hidden') {
                                    const text = (btn.textContent || btn.innerText || '').trim().toLowerCase();
                                    if (text.includes('sign in') || text.includes('登录') || text.includes('log in')) {
                                        btn.click();
                                        return true;
                                    }
                                }
                            }
                            const submitBtn = document.querySelector('button[type="submit"]');
                            if (submitBtn) {
                                const style = window.getComputedStyle(submitBtn);
                                if (style.display !== 'none' && style.visibility !== 'hidden') {
                                    submitBtn.click();
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)
                    assert click_success, "应该成功点击登录按钮"
                    print("✅ 使用 JavaScript 点击登录按钮成功")
                else:
                    raise AssertionError("应该找到登录按钮")
                
                await page.wait_for_timeout(5000)
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step7_after_login.png", full_page=True)
                
                # 步骤 8: 验证登录状态
                print("\n步骤 8: 验证登录状态")
                await page.wait_for_timeout(3000)
                page_text = await page.inner_text('body')
                has_user_info = "xyz" in page_text.lower() or "xyzdev01" in page_text.lower()
                sign_in_button_still_visible = await page.locator('text=Sign Up / Log In').count() > 0
                
                assert has_user_info or not sign_in_button_still_visible, "应该显示登录状态"
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step8_login_verified.png", full_page=True)
                print("✅ 登录状态验证通过")
                
                # 步骤 9: 导航到 Account 页面
                print("\n步骤 9: 导航到 Account 页面")
                account_url = f"{BASE_URL}/agentSociety/setting/account"
                await page.goto(account_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                
                current_url = page.url
                assert account_url in current_url, f"应该导航到 {account_url}，实际: {current_url}"
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step9_account_page.png", full_page=True)
                print(f"✅ 成功导航到 Account 页面: {current_url}")
                
                # 步骤 10: 验证用户信息
                print("\n步骤 10: 验证用户信息")
                await page.wait_for_timeout(2000)
                await page.evaluate("window.scrollTo(0, 0)")
                await page.wait_for_timeout(1000)
                
                page_text = await page.inner_text('body')
                username_found = "xyzdev01" in page_text
                email_found = TEST_EMAIL in page_text
                
                assert username_found, f"应该找到用户名 xyzdev01"
                assert email_found, f"应该找到 email {TEST_EMAIL}"
                
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_step10_account_info_verified.png", full_page=True)
                print(f"✅ 用户名验证通过: xyzdev01")
                print(f"✅ Email 验证通过: {TEST_EMAIL}")
                
                print("\n" + "=" * 60)
                print("测试完成：Login and check Account page")
                print("=" * 60)
                print(f"最终 URL: {current_url}")
                print(f"用户名验证: ✅")
                print(f"Email 验证: ✅")
                
            except Exception as e:
                await page.screenshot(path=SCREENSHOT_DIR / "test_login_error.png", full_page=True)
                print(f"\n❌ 测试失败: {e}")
                raise
            finally:
                await browser.close()

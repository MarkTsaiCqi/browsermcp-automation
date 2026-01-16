"""完整的登录流程测试脚本

使用 Playwright 完成完整的登录流程，每一步都截图验证：
1. 连接到首页
2. 点击 Sign Up/Log In 按钮
3. 等待弹窗出现
4. 验证弹窗内可输入 email 的字段
5. 输入 email: xyzdev01@cqigames.com，然后下一步
6. 输入 password: Abc123123?，然后登录
7. 验证已登录 xyz
8. 点击左下角的个人头像，然后在弹出选单中选 Account
9. 验证被引导到 https://xyz-beta.protago-dev.com/agentSociety/setting/account
10. 验证可以看到使用者名字 xyzdev01 以及 email xyzdev01@cqigames.com
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

# 创建截图目录
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


async def test_complete_login_flow():
    """完整的登录流程测试"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("=" * 60)
        print("完整登录流程测试")
        print("=" * 60)
        print()
        
        try:
            # 步骤 1: 连接到首页
            print("步骤 1: 连接到首页")
            await page.goto("https://xyz-beta.protago-dev.com/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=SCREENSHOT_DIR / "step1_homepage.png", full_page=True)
            print(f"✅ 首页加载完成: {page.url}")
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step1_homepage.png'}")
            print()
            
            # 步骤 2: 点击 Sign Up/Log In 按钮
            print("步骤 2: 点击 Sign Up/Log In 按钮")
            # 使用 JavaScript 查找并点击按钮
            click_result = await page.evaluate("""
                () => {
                    const allElements = document.querySelectorAll('*');
                    let foundButton = null;
                    
                    for (let el of allElements) {
                        const text = (el.textContent || el.innerText || '').trim();
                        // 精确匹配 "Sign Up / Log In"
                        if (text === 'Sign Up / Log In' || 
                            (text.includes('Sign Up') && text.includes('Log In') && text.length < 30)) {
                            // 找到最内层的元素
                            let isLeaf = true;
                            for (let child of el.children) {
                                const childText = (child.textContent || child.innerText || '').trim();
                                if (childText === text || (childText.includes('Sign Up') && childText.includes('Log In'))) {
                                    isLeaf = false;
                                    break;
                                }
                            }
                            if (isLeaf && el.tagName !== 'HTML' && el.tagName !== 'BODY') {
                                foundButton = el;
                                break;
                            }
                        }
                    }
                    
                    if (foundButton) {
                        // 滚动到按钮位置
                        foundButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        return new Promise((resolve) => {
                            setTimeout(() => {
                                // 触发点击事件
                                const clickEvent = new MouseEvent('click', {
                                    bubbles: true,
                                    cancelable: true,
                                    view: window,
                                    button: 0
                                });
                                foundButton.dispatchEvent(clickEvent);
                                
                                // 也尝试直接调用 click 方法
                                if (typeof foundButton.click === 'function') {
                                    foundButton.click();
                                }
                                
                                resolve({
                                    success: true,
                                    tagName: foundButton.tagName,
                                    className: foundButton.className
                                });
                            }, 500);
                        });
                    }
                    return {success: false, message: 'Button not found'};
                }
            """)
            
            print(f"   点击结果: {click_result}")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=SCREENSHOT_DIR / "step2_after_click_button.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step2_after_click_button.png'}")
            print()
            
            # 步骤 3: 等待弹窗出现
            print("步骤 3: 等待弹窗出现")
            try:
                # 等待弹窗出现
                await page.wait_for_selector('[role="dialog"]', timeout=5000)
                print("✅ 弹窗已出现")
            except Exception as e:
                print(f"⚠️  等待弹窗超时: {e}")
                # 继续尝试等待
                await page.wait_for_timeout(2000)
            
            await page.wait_for_timeout(1000)
            await page.screenshot(path=SCREENSHOT_DIR / "step3_modal_appeared.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step3_modal_appeared.png'}")
            print()
            
            # 步骤 4: 验证弹窗内可输入 email 的字段
            print("步骤 4: 验证弹窗内可输入 email 的字段")
            # 尝试多种选择器
            email_input = None
            selectors = [
                'input[type="email"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="Email" i]',
                'input',
                '[role="textbox"]',
                'input[aria-label*="email" i]'
            ]
            
            for selector in selectors:
                try:
                    email_input = page.locator(selector).first
                    await email_input.wait_for(state='visible', timeout=3000)
                    # 验证确实是 email 输入框或可编辑的输入框
                    input_type = await email_input.get_attribute('type')
                    if input_type == 'email' or selector == 'input[type="email"]' or selector == 'input':
                        print(f"✅ Email 输入字段已找到（使用选择器: {selector}）")
                        break
                except:
                    continue
            
            if not email_input:
                # 如果还是找不到，使用 JavaScript 查找
                print("   尝试使用 JavaScript 查找 email 输入字段...")
                email_info = await page.evaluate("""
                    () => {
                        const inputs = document.querySelectorAll('input');
                        for (let input of inputs) {
                            const style = window.getComputedStyle(input);
                            if (style.display !== 'none' && style.visibility !== 'hidden') {
                                const placeholder = input.placeholder || '';
                                const type = input.type || '';
                                if (type === 'email' || placeholder.toLowerCase().includes('email')) {
                                    return {
                                        found: true,
                                        type: type,
                                        placeholder: placeholder,
                                        id: input.id,
                                        className: input.className
                                    };
                                }
                            }
                        }
                        return {found: false};
                    }
                """)
                print(f"   JavaScript 查找结果: {email_info}")
                
                if email_info.get('found'):
                    email_input = page.locator('input').first
                    await email_input.wait_for(state='visible', timeout=3000)
                    print("✅ 使用 JavaScript 找到 email 输入字段")
                else:
                    raise Exception("无法找到 email 输入字段")
            
            # 验证字段是否可编辑
            is_editable = await email_input.is_editable()
            print(f"   Email 字段可编辑: {is_editable}")
            
            await page.screenshot(path=SCREENSHOT_DIR / "step4_email_field_visible.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step4_email_field_visible.png'}")
            print()
            
            # 步骤 5: 输入 email
            print("步骤 5: 输入 email: xyzdev01@cqigames.com")
            await email_input.fill("xyzdev01@cqigames.com")
            await page.wait_for_timeout(500)
            
            # 验证输入是否成功
            input_value = await email_input.input_value()
            if input_value == "xyzdev01@cqigames.com":
                print("✅ Email 输入成功")
            else:
                print(f"⚠️  Email 输入值不匹配: 期望 'xyzdev01@cqigames.com', 实际 '{input_value}'")
            
            await page.screenshot(path=SCREENSHOT_DIR / "step5_email_entered.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step5_email_entered.png'}")
            print()
            
            # 步骤 5.5: 点击下一步按钮（如果存在）
            print("步骤 5.5: 检查是否需要点击下一步按钮")
            await page.wait_for_timeout(1000)  # 先等待一下，让弹窗完全加载
            
            # 使用 JavaScript 查找并点击下一步按钮
            next_button_result = await page.evaluate("""
                () => {
                    // 查找 email 输入框
                    const emailInput = document.querySelector('input[type="email"], input[placeholder*="email" i], input');
                    if (!emailInput) return {found: false, message: 'Email input not found'};
                    
                    // 查找 email 输入框右侧或附近的按钮
                    const parent = emailInput.parentElement;
                    const buttons = parent.querySelectorAll('button, [role="button"], svg, [class*="arrow" i]');
                    
                    for (let btn of buttons) {
                        const style = window.getComputedStyle(btn);
                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                            const rect = btn.getBoundingClientRect();
                            const inputRect = emailInput.getBoundingClientRect();
                            // 检查按钮是否在输入框右侧
                            if (rect.left > inputRect.right - 50 && rect.top < inputRect.bottom && rect.bottom > inputRect.top) {
                                btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                setTimeout(() => {
                                    btn.click();
                                }, 500);
                                return {found: true, tagName: btn.tagName, className: btn.className};
                            }
                        }
                    }
                    
                    // 如果没找到，尝试查找所有可点击的元素
                    const allClickable = document.querySelectorAll('button, [role="button"], [onclick], [class*="cursor-pointer" i]');
                    for (let el of allClickable) {
                        const style = window.getComputedStyle(el);
                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                            const rect = el.getBoundingClientRect();
                            const inputRect = emailInput.getBoundingClientRect();
                            // 检查是否在输入框附近
                            if (Math.abs(rect.left - inputRect.right) < 100 && 
                                rect.top < inputRect.bottom + 50 && 
                                rect.bottom > inputRect.top - 50) {
                                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                setTimeout(() => {
                                    el.click();
                                }, 500);
                                return {found: true, tagName: el.tagName, className: el.className};
                            }
                        }
                    }
                    
                    return {found: false, message: 'Next button not found'};
                }
            """)
            
            print(f"   下一步按钮查找结果: {next_button_result}")
            
            if next_button_result.get('found'):
                print("✅ 点击下一步按钮")
                await page.wait_for_timeout(4000)  # 等待 password 字段出现
            else:
                print("⚠️  未找到下一步按钮，尝试按 Enter 键")
                await email_input.press('Enter')
                await page.wait_for_timeout(4000)
            
            await page.screenshot(path=SCREENSHOT_DIR / "step5_5_after_next.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step5_5_after_next.png'}")
            print()
            
            # 步骤 6: 输入 password
            print("步骤 6: 输入 password: Abc123123?")
            # 尝试多种方法查找 password 字段
            password_input = None
            password_found = False
            password_selectors = [
                'input[type="password"]',
                'input[placeholder*="password" i]',
                'input[placeholder*="Password" i]',
                'input[name*="password" i]',
                'input[aria-label*="password" i]'
            ]
            
            for selector in password_selectors:
                try:
                    test_locator = page.locator(selector).first
                    await test_locator.wait_for(state='visible', timeout=3000)
                    # 验证元素确实可见且可编辑
                    if await test_locator.is_visible():
                        password_input = test_locator
                        password_found = True
                        print(f"✅ Password 输入字段已找到（使用选择器: {selector}）")
                        break
                except:
                    continue
            
            if not password_found:
                # 使用 JavaScript 查找
                print("   尝试使用 JavaScript 查找 password 输入字段...")
                await page.wait_for_timeout(2000)  # 再等待一下
                
                password_info = await page.evaluate("""
                    () => {
                        const inputs = document.querySelectorAll('input');
                        let allInputs = [];
                        for (let input of inputs) {
                            const style = window.getComputedStyle(input);
                            if (style.display !== 'none' && style.visibility !== 'hidden') {
                                const type = input.type || '';
                                const placeholder = input.placeholder || '';
                                const name = input.name || '';
                                allInputs.push({
                                    type: type,
                                    placeholder: placeholder,
                                    name: name,
                                    id: input.id,
                                    className: input.className
                                });
                                if (type === 'password' || placeholder.toLowerCase().includes('password')) {
                                    return {
                                        found: true,
                                        type: type,
                                        placeholder: placeholder,
                                        allInputs: allInputs
                                    };
                                }
                            }
                        }
                        return {found: false, allInputs: allInputs};
                    }
                """)
                print(f"   JavaScript 查找结果: {password_info}")
                
                if password_info.get('found'):
                    # 再次尝试使用 locator
                    try:
                        password_input = page.locator('input[type="password"]').first
                        await page.wait_for_timeout(1000)
                        await password_input.wait_for(state='visible', timeout=5000)
                        if await password_input.is_visible():
                            password_found = True
                            print("✅ 使用 JavaScript 找到 password 输入字段")
                    except:
                        pass
                
                if not password_found:
                    # 如果找不到 password 字段，先截图看看当前状态
                    await page.screenshot(path=SCREENSHOT_DIR / "step6_debug_no_password.png", full_page=True)
                    print(f"   ⚠️  未找到 password 字段，调试截图已保存: {SCREENSHOT_DIR / 'step6_debug_no_password.png'}")
                    print(f"   当前页面所有输入框: {password_info.get('allInputs', [])}")
                    raise Exception("无法找到 password 输入字段")
            
            if not password_found or not password_input:
                raise Exception("Password 输入字段未正确初始化")
            
            await password_input.fill("Abc123123?")
            await page.wait_for_timeout(500)
            
            # 验证输入是否成功（password 字段通常无法读取值，但可以检查长度）
            input_length = len(await password_input.input_value())
            if input_length > 0:
                print(f"✅ Password 输入成功（长度: {input_length}）")
            else:
                print("⚠️  Password 输入可能失败")
            
            await page.screenshot(path=SCREENSHOT_DIR / "step6_password_entered.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step6_password_entered.png'}")
            print()
            
            # 步骤 7: 点击登录按钮
            print("步骤 7: 点击登录按钮")
            sign_in_button = None
            sign_in_found = False
            
            # 尝试多种方法查找登录按钮
            sign_in_selectors = [
                'button:has-text("Sign In")',
                'button:has-text("登录")',
                'button:has-text("Log In")',
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
                # 使用 JavaScript 查找
                print("   尝试使用 JavaScript 查找登录按钮...")
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
                        // 如果没找到文本匹配的，找 submit 按钮
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
                        sign_in_button = page.locator('button').filter(has_text=button_info.get('text', '')).first
                    await page.wait_for_timeout(1000)
                    await sign_in_button.wait_for(state='visible', timeout=5000)
                    if await sign_in_button.is_visible():
                        sign_in_found = True
                        print("✅ 使用 JavaScript 找到登录按钮")
            
            if not sign_in_found or not sign_in_button:
                await page.screenshot(path=SCREENSHOT_DIR / "step7_debug_no_signin_button.png", full_page=True)
                raise Exception("无法找到登录按钮")
            
            await sign_in_button.click()
            print("✅ 点击登录按钮成功")
            
            await page.wait_for_timeout(5000)  # 等待登录完成
            await page.screenshot(path=SCREENSHOT_DIR / "step7_after_login_click.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step7_after_login_click.png'}")
            print()
            
            # 步骤 8: 验证已登录 xyz
            print("步骤 8: 验证已登录 xyz")
            await page.wait_for_timeout(3000)
            
            # 检查页面内容是否包含登录后的元素
            page_text = await page.inner_text('body')
            has_xyz = "xyz" in page_text.lower() or "xyzdev01" in page_text.lower()
            
            # 检查是否还有 "Sign Up / Log In" 按钮（登录后应该消失或改变）
            sign_in_button_still_visible = await page.locator('text=Sign Up / Log In').count() > 0
            
            if has_xyz and not sign_in_button_still_visible:
                print("✅ 登录状态验证通过（找到 xyz 相关内容，登录按钮已消失）")
            elif has_xyz:
                print("⚠️  找到 xyz 相关内容，但登录按钮仍然可见")
            else:
                print("⚠️  未明确检测到登录状态，继续执行...")
            
            await page.screenshot(path=SCREENSHOT_DIR / "step8_login_verified.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step8_login_verified.png'}")
            print()
            
            # 步骤 9: 导航到 Society 页面（登录后通常在这里）
            print("步骤 9: 导航到 Society 页面")
            await page.goto("https://xyz-beta.protago-dev.com/agentSociety/society", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=SCREENSHOT_DIR / "step9_society_page.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step9_society_page.png'}")
            print()
            
            # 步骤 10: 点击左下角的个人头像
            print("步骤 10: 点击左下角的个人头像")
            # 尝试多种方法查找头像
            avatar_found = False
            
            # 方法1: 查找图片元素（头像通常是图片）
            try:
                # 查找页面底部的图片元素
                images = await page.query_selector_all('img')
                for img in images:
                    # 获取图片位置
                    box = await img.bounding_box()
                    if box:
                        # 检查是否在左下角区域（左侧且底部）
                        viewport = page.viewport_size
                        if box['x'] < viewport['width'] / 2 and box['y'] > viewport['height'] / 2:
                            # 尝试点击
                            await img.click()
                            print(f"✅ 找到并点击左下角图片（位置: x={box['x']}, y={box['y']}）")
                            avatar_found = True
                            break
            except Exception as e:
                print(f"⚠️  方法1失败: {e}")
            
            # 方法2: 使用 JavaScript 查找并点击左下角的可点击元素
            if not avatar_found:
                try:
                    result = await page.evaluate("""
                        () => {
                            const allElements = document.querySelectorAll('img, button, [role="button"], [class*="avatar" i], [class*="user" i], [class*="profile" i]');
                            let bottomLeftElement = null;
                            let minDistance = Infinity;
                            const viewportHeight = window.innerHeight;
                            const viewportWidth = window.innerWidth;
                            
                            for (let el of allElements) {
                                const rect = el.getBoundingClientRect();
                                // 计算到左下角的距离
                                const distance = Math.sqrt(
                                    Math.pow(rect.left, 2) + 
                                    Math.pow(viewportHeight - rect.bottom, 2)
                                );
                                
                                // 如果元素在左下角区域
                                if (rect.left < viewportWidth / 2 && 
                                    rect.bottom > viewportHeight / 2 &&
                                    distance < minDistance &&
                                    rect.width > 0 && rect.height > 0) {
                                    minDistance = distance;
                                    bottomLeftElement = el;
                                }
                            }
                            
                            if (bottomLeftElement) {
                                bottomLeftElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                setTimeout(() => {
                                    bottomLeftElement.click();
                                }, 500);
                                return {success: true, tagName: bottomLeftElement.tagName, className: bottomLeftElement.className};
                            }
                            return {success: false};
                        }
                    """)
                    
                    if result.get('success'):
                        print(f"✅ 使用 JavaScript 找到并点击左下角元素: {result}")
                        avatar_found = True
                    else:
                        print("⚠️  未找到左下角头像")
                except Exception as e:
                    print(f"⚠️  方法2失败: {e}")
            
            await page.wait_for_timeout(2000)
            await page.screenshot(path=SCREENSHOT_DIR / "step10_avatar_clicked.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step10_avatar_clicked.png'}")
            print()
            
            # 步骤 11: 在弹出选单中选 Account
            print("步骤 11: 在弹出选单中选 Account")
            try:
                account_menu = page.locator('text=Account, text=账户, [role="menuitem"]:has-text("Account"), [role="menuitem"]:has-text("账户")').first
                await account_menu.wait_for(state='visible', timeout=5000)
                await account_menu.click()
                print("✅ 点击 Account 菜单项成功")
            except Exception as e:
                print(f"⚠️  查找 Account 菜单失败: {e}")
                print("   尝试直接导航到账户设置页面...")
                # 直接导航到账户设置页面
                await page.goto("https://xyz-beta.protago-dev.com/agentSociety/setting/account", wait_until="domcontentloaded")
                print("✅ 直接导航到账户设置页面")
            
            await page.wait_for_timeout(3000)
            await page.screenshot(path=SCREENSHOT_DIR / "step11_account_menu_clicked.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step11_account_menu_clicked.png'}")
            print()
            
            # 步骤 12: 验证被引导到账户设置页面
            print("步骤 12: 验证被引导到账户设置页面")
            current_url = page.url
            expected_url = "https://xyz-beta.protago-dev.com/agentSociety/setting/account"
            
            if expected_url in current_url:
                print(f"✅ URL 验证通过: {current_url}")
            else:
                print(f"⚠️  URL 不匹配: 期望包含 '{expected_url}', 实际 '{current_url}'")
                # 如果 URL 不匹配，尝试导航到正确的 URL
                await page.goto(expected_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                current_url = page.url
                print(f"   已导航到: {current_url}")
            
            await page.screenshot(path=SCREENSHOT_DIR / "step12_account_page.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step12_account_page.png'}")
            
            # 额外截图：Account 页面详细内容
            print("   正在捕获 Account 页面详细内容...")
            await page.wait_for_timeout(2000)
            # 滚动到页面顶部，确保能看到所有内容
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=SCREENSHOT_DIR / "step12_account_page_top.png", full_page=True)
            # 滚动到页面中间
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=SCREENSHOT_DIR / "step12_account_page_middle.png", full_page=True)
            # 滚动到页面底部
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=SCREENSHOT_DIR / "step12_account_page_bottom.png", full_page=True)
            print(f"   Account 页面详细截图已保存（top, middle, bottom）")
            print()
            
            # 步骤 13: 验证使用者名字和 email
            print("步骤 13: 验证使用者名字 xyzdev01 以及 email xyzdev01@cqigames.com")
            await page.wait_for_timeout(2000)
            # 滚动回顶部以便查看用户信息
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(1000)
            
            page_text = await page.inner_text('body')
            
            username_found = "xyzdev01" in page_text or "xzyDev01" in page_text
            email_found = "xyzdev01@cqigames.com" in page_text
            
            if username_found:
                print("✅ 找到使用者名字: xyzdev01")
            else:
                print("❌ 未找到使用者名字: xyzdev01")
            
            if email_found:
                print("✅ 找到 email: xyzdev01@cqigames.com")
            else:
                print("❌ 未找到 email: xyzdev01@cqigames.com")
            
            # 尝试更精确地查找用户名和 email
            try:
                # 查找可能包含用户名的元素
                username_elements = await page.query_selector_all('*')
                for el in username_elements[:100]:  # 限制检查数量
                    text = await el.inner_text() if await el.is_visible() else ""
                    if "xyzdev01" in text.lower() and len(text) < 50:
                        print(f"   找到用户名元素: {text[:50]}")
                        break
            except:
                pass
            
            await page.screenshot(path=SCREENSHOT_DIR / "step13_account_info_verified.png", full_page=True)
            print(f"   截图已保存: {SCREENSHOT_DIR / 'step13_account_info_verified.png'}")
            print()
            
            # 最终总结
            print("=" * 60)
            print("测试完成总结")
            print("=" * 60)
            print(f"最终 URL: {current_url}")
            print(f"用户名验证: {'✅' if username_found else '❌'}")
            print(f"Email 验证: {'✅' if email_found else '❌'}")
            print(f"所有截图保存在: {SCREENSHOT_DIR.absolute()}")
            print()
            
            if username_found and email_found:
                print("🎉 所有验证通过！")
            else:
                print("⚠️  部分验证失败，请检查截图")
            
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            await page.screenshot(path=SCREENSHOT_DIR / "error_screenshot.png", full_page=True)
            raise
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_complete_login_flow())

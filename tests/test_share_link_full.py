"""完整的 Share Link 对话测试

测试步骤：
1. 连接到 share link
2. 在对话框中输入完整问题
3. 提交问题
4. 等待回应
5. 记录回应时间和内容
"""
import asyncio
from playwright.async_api import async_playwright
import time

SHARE_LINK = "https://xyz-beta.protago-dev.com/share/ac292053cc66421ea437e7c9c9a59050"
QUESTION = "列出knowledge-base目錄下的檔案"

# 验证规则：验证关键信息而不是完全匹配
VERIFICATION_RULES = {
    "列出knowledge-base目錄下的檔案": {
        "required_keywords": ["knowledge-base", "檔案", "hello.md"],  # 必须包含的关键词
        "expected_file": "hello.md",  # 预期的文件名
        "min_length": 50,  # 响应最小长度
        "exclude_keywords": ["错误", "error", "无法", "失败"]  # 不应包含的错误关键词
    }
}


async def test_share_link_full():
    """完整的 share link 对话测试"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 有头模式以便观察
        page = await browser.new_page()
        
        print("=" * 60)
        print("Share Link 完整对话测试")
        print("=" * 60)
        
        try:
            # 步骤 1: 导航到 share link
            print(f"\n步骤 1: 导航到 share link")
            print(f"URL: {SHARE_LINK}")
            await page.goto(SHARE_LINK, wait_until="networkidle")
            await page.wait_for_timeout(3000)
            print("✅ 页面加载完成")
            await page.screenshot(path="screenshots/share_full_step1_loaded.png", full_page=True)
            
            # 步骤 2: 定位并输入问题
            print(f"\n步骤 2: 在对话框中输入问题")
            print(f"问题: {QUESTION}")
            
            # 使用 Playwright 的 fill 方法（已验证可用）
            input_locator = page.locator('[role="textbox"]').first
            await input_locator.wait_for(state='visible', timeout=10000)
            
            # 记录开始时间
            start_time = time.time()
            print(f"开始时间: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
            
            # 输入问题
            await input_locator.fill(QUESTION)
            await page.wait_for_timeout(1000)
            
            # 验证输入
            input_value = await input_locator.inner_text()
            if QUESTION in input_value or input_value.strip() == QUESTION:
                print(f"✅ 问题已输入: '{input_value}'")
            else:
                print(f"⚠️  输入值可能不完整: '{input_value}'")
            
            await page.screenshot(path="screenshots/share_full_step2_input_done.png", full_page=True)
            
            # 步骤 3: 提交问题
            print(f"\n步骤 3: 提交问题")
            submit_time = time.time()
            print(f"提交时间: {time.strftime('%H:%M:%S', time.localtime(submit_time))}")
            
            # 按 Enter 键提交
            await input_locator.press('Enter')
            await page.wait_for_timeout(2000)
            
            print("✅ 已按 Enter 键提交")
            await page.screenshot(path="screenshots/share_full_step3_submitted.png", full_page=True)
            
            # 步骤 4: 等待回应
            print(f"\n步骤 4: 等待回应...")
            
            max_wait = 120  # 最多等待 120 秒
            check_interval = 2  # 每 2 秒检查一次
            elapsed = 0
            response_found = False
            working_on_it_seen = False
            working_on_it_disappeared = False
            
            initial_text = await page.inner_text('body')
            initial_message_count = len(await page.query_selector_all('[class*="message"], [class*="chat"], [role="article"]'))
            
            print(f"初始状态: 消息数={initial_message_count}, 文本长度={len(initial_text)}")
            
            while elapsed < max_wait:
                await page.wait_for_timeout(check_interval * 1000)
                elapsed += check_interval
                
                current_text = await page.inner_text('body')
                current_message_count = len(await page.query_selector_all('[class*="message"], [class*="chat"], [role="article"]'))
                
                # 检查是否看到 "Working on it"
                if "Working on it" in current_text and not working_on_it_seen:
                    working_on_it_seen = True
                    print(f"  ✅ 检测到 'Working on it...' (第 {elapsed} 秒)")
                
                # 检查 "Working on it" 是否消失
                if working_on_it_seen and "Working on it" not in current_text and not working_on_it_disappeared:
                    working_on_it_disappeared = True
                    print(f"  ✅ 'Working on it' 已消失！等待响应完全加载... (第 {elapsed} 秒)")
                    # 等待响应完全加载
                    for wait_attempt in range(15):  # 最多等待30秒
                        await page.wait_for_timeout(2000)
                        current_check = await page.inner_text('body')
                        text_length = len(current_check)
                        print(f"    等待响应加载... ({wait_attempt + 1}/15, 文本长度: {text_length})")
                        
                        # 检查文本是否稳定（连续两次检查长度相同）
                        if wait_attempt > 3:
                            # 检查是否有明显的新内容（不是 "Working on it"）
                            if text_length > len(initial_text) + 300:
                                # 检查是否包含可能的响应内容
                                if (QUESTION in current_check and 
                                    'Working on it' not in current_check):
                                    print(f"    ✅ 响应内容已加载 (文本长度: {text_length})")
                                    await page.wait_for_timeout(3000)  # 再等待3秒确保完全渲染
                                    response_found = True
                                    break
                    if response_found:
                        break
                
                # 检查消息数量是否增加
                if current_message_count > initial_message_count:
                    print(f"  ✅ 检测到新消息 (消息数: {initial_message_count} -> {current_message_count})")
                    await page.wait_for_timeout(3000)
                    response_found = True
                    break
                
                # 检查文本内容是否明显变化
                if current_text != initial_text:
                    text_increase = len(current_text) - len(initial_text)
                    if text_increase > 300 and "Working on it" not in current_text:
                        print(f"  ✅ 检测到内容明显变化 (文本增加: {text_increase} 字符)")
                        await page.wait_for_timeout(3000)
                        response_found = True
                        break
                
                status = f"等待中... ({elapsed} 秒, 消息数: {current_message_count}, 文本长度: {len(current_text)}"
                if working_on_it_seen:
                    if working_on_it_disappeared:
                        status += ", Working on it 已消失"
                    else:
                        status += ", 已看到 Working on it"
                status += ")"
                print(f"  {status}")
            
            end_time = time.time()
            response_time = end_time - submit_time
            
            print(f"\n检查完成时间: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
            print(f"响应时间: {response_time:.2f} 秒")
            
            # 步骤 5: 获取并记录回应内容
            print(f"\n步骤 5: 获取回应内容")
            await page.screenshot(path="screenshots/share_full_step5_final.png", full_page=True)
            
            # 使用 JavaScript 获取对话内容（改进版）
            conversation_data = await page.evaluate(f"""
                () => {{
                    const question = '{QUESTION}';
                    const result = {{
                        userQuestion: null,
                        agentResponse: null,
                        allMessages: [],
                        pageText: document.body.innerText || document.body.textContent || ''
                    }};
                    
                    // 方法1: 查找所有包含文本的元素，按位置排序
                    const allElements = Array.from(document.querySelectorAll('*'));
                    const textElements = [];
                    
                    for (let el of allElements) {{
                        const text = (el.textContent || el.innerText || '').trim();
                        if (text.length > 20) {{
                            const rect = el.getBoundingClientRect();
                            const style = window.getComputedStyle(el);
                            if (style.display !== 'none' && style.visibility !== 'hidden' &&
                                rect.width > 0 && rect.height > 0) {{
                                textElements.push({{
                                    text: text,
                                    tagName: el.tagName,
                                    top: rect.top,
                                    left: rect.left
                                }});
                            }}
                        }}
                    }}
                    
                    // 按位置排序（从上到下，从左到右）
                    textElements.sort((a, b) => {{
                        if (Math.abs(a.top - b.top) < 10) {{
                            return a.left - b.left;
                        }}
                        return a.top - b.top;
                    }});
                    
                    // 找到问题位置
                    let questionIndex = -1;
                    for (let i = 0; i < textElements.length; i++) {{
                        if (textElements[i].text.includes(question)) {{
                            questionIndex = i;
                            result.userQuestion = {{
                                text: textElements[i].text.substring(0, 200),
                                index: i
                            }};
                            break;
                        }}
                    }}
                    
                    // 获取问题之后的内容（可能是响应）
                    if (questionIndex >= 0) {{
                        const afterQuestion = textElements.slice(questionIndex + 1);
                        const responseCandidates = [];
                        
                        for (let elem of afterQuestion) {{
                            const text = elem.text;
                            // 过滤掉明显的UI元素和重复内容
                            if (!text.includes('I am Claudia') &&
                                !text.includes('Working on it') &&
                                !text.includes('Ask me anything') &&
                                !text.includes('Clear history') &&
                                !text.includes('DEBUG') &&
                                !text.includes('Copy') &&
                                text.length > 30 &&
                                !text.match(/^NetMind XYZ$/)) {{
                                
                                // 检查是否是响应（包含时间戳或 Claudia 但不是自我介绍）
                                if ((text.includes('Claudia') && text.match(/\\d{1,2}:\\d{2}\\s*(AM|PM)/)) ||
                                    text.includes('knowledge') ||
                                    text.includes('檔案') ||
                                    text.includes('file') ||
                                    text.length > 100) {{
                                    responseCandidates.push(text);
                                }}
                            }}
                        }}
                        
                        if (responseCandidates.length > 0) {{
                            // 合并响应，去除重复
                            const uniqueResponses = [];
                            for (let resp of responseCandidates) {{
                                if (!uniqueResponses.some(r => r.includes(resp.substring(0, 50)) || resp.includes(r.substring(0, 50)))) {{
                                    uniqueResponses.push(resp);
                                }}
                            }}
                            result.agentResponse = uniqueResponses.join('\\n\\n---\\n\\n');
                        }}
                    }}
                    
                    result.allMessages = textElements.map(e => e.text.substring(0, 150));
                    
                    return result;
                }}
            """)
            
            # 获取页面完整文本
            final_text = await page.inner_text('body')
            lines = final_text.split('\n')
            
            # 也尝试直接查找包含文件列表的内容
            print(f"\n>>> 直接搜索响应内容:")
            print("-" * 60)
            
            # 查找问题之后的所有内容
            question_found = False
            response_lines = []
            for i, line in enumerate(lines):
                if QUESTION in line:
                    question_found = True
                    print(f"找到问题在第 {i+1} 行")
                    # 继续查找问题之后的内容
                    continue
                
                if question_found:
                    line_clean = line.strip()
                    # 跳过明显的UI元素
                    if (line_clean and 
                        len(line_clean) > 10 and
                        'Working on it' not in line_clean and
                        'Ask me anything' not in line_clean and
                        'DEBUG' not in line_clean and
                        'Clear history' not in line_clean and
                        'Copy' not in line_clean and
                        'NetMind XYZ' not in line_clean and
                        not line_clean.startswith('I am Claudia')):
                        response_lines.append(line)
                        if len(response_lines) >= 30:  # 收集30行
                            break
            
            print("\\n" + "=" * 60)
            print("对话内容")
            print("=" * 60)
            
            # 显示用户问题
            if conversation_data.get('userQuestion'):
                q = conversation_data['userQuestion']
                print(f"\\n>>> 用户问题:")
                print(f"    {q['text'][:200]}...")
            else:
                print(f"\\n⚠️  未找到用户问题")
            
            # 显示 Agent 响应
            if conversation_data.get('agentResponse'):
                print(f"\n>>> Agent 响应:")
                print("-" * 60)
                response_text = conversation_data['agentResponse']
                print(response_text)
                print("-" * 60)
            else:
                print(f"\n⚠️  未找到 Agent 响应（通过 JavaScript）")
                print(f"    找到 {len(conversation_data.get('allMessages', []))} 条消息")
                
                # 显示所有消息（用于调试）
                if conversation_data.get('allMessages'):
                    print(f"\\n所有消息列表:")
                    print("-" * 60)
                    for i, msg in enumerate(conversation_data['allMessages']):
                        msg_text = msg['text'][:150]
                        if len(msg['text']) > 150:
                            msg_text += "..."
                        print(f"  {i+1}. [{msg['tagName']}] {msg_text}")
            
            # 也在页面文本中查找
            question_index = -1
            for i, line in enumerate(lines):
                if QUESTION in line:
                    question_index = i
                    print(f"\\n>>> 在页面文本中找到问题 (第 {i+1} 行):")
                    print(f"    {line}")
                    # 显示问题后的内容
                    if i + 1 < len(lines):
                        print(f"\\n>>> 问题后的内容（可能是响应）:")
                        print("-" * 60)
                        response_lines = []
                        for j in range(i + 1, min(len(lines), i + 100)):  # 增加行数
                            line_text = lines[j].strip()
                            # 跳过空行和太短的行，但保留可能有用的内容
                            if line_text and len(line_text) > 5:
                                # 跳过一些明显的UI元素
                                if not any(skip in line_text for skip in ['Ask me anything', 'DEBUG', 'Clear history', 'Copy']):
                                    response_lines.append(lines[j])
                                    if len(response_lines) >= 50:  # 显示更多行
                                        break
                        for line in response_lines:
                            print(f"    {line}")
                    break
            
            # 额外检查：查找可能包含文件列表的内容
            print(f"\\n>>> 查找可能包含文件列表的内容:")
            print("-" * 60)
            file_list_keywords = ['knowledge', 'base', '檔案', 'file', 'directory', '目錄', '.txt', '.md', '.pdf', '.doc']
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in file_list_keywords):
                    if QUESTION not in line:  # 排除问题本身
                        print(f"  第 {i+1} 行: {line[:200]}")
            
            # 步骤 6: 验证响应内容（灵活验证，不要求完全匹配）
            print("\n" + "=" * 60)
            print("步骤 6: 验证响应内容")
            print("=" * 60)
            
            # 获取响应内容
            response_content = conversation_data.get('agentResponse', '')
            if not response_content and response_lines:
                response_content = '\n'.join(response_lines)
            
            verification_result = {
                "passed": False,
                "checks": [],
                "errors": []
            }
            
            if response_content:
                # 获取验证规则
                rules = VERIFICATION_RULES.get(QUESTION, {})
                
                if rules:
                    print(f"\n验证规则: {QUESTION}")
                    print("-" * 60)
                    
                    # 检查1: 响应长度
                    if len(response_content) >= rules.get('min_length', 0):
                        verification_result["checks"].append("✅ 响应长度符合要求")
                        print(f"✅ 响应长度: {len(response_content)} 字符 (要求: >= {rules.get('min_length', 0)})")
                    else:
                        verification_result["errors"].append(f"响应长度不足: {len(response_content)} < {rules.get('min_length', 0)}")
                        print(f"❌ 响应长度不足: {len(response_content)} < {rules.get('min_length', 0)}")
                    
                    # 检查2: 必须包含的关键词
                    required_keywords = rules.get('required_keywords', [])
                    missing_keywords = []
                    for keyword in required_keywords:
                        if keyword.lower() in response_content.lower():
                            verification_result["checks"].append(f"✅ 包含关键词: {keyword}")
                            print(f"✅ 包含关键词: '{keyword}'")
                        else:
                            missing_keywords.append(keyword)
                            verification_result["errors"].append(f"缺少关键词: {keyword}")
                            print(f"❌ 缺少关键词: '{keyword}'")
                    
                    # 检查3: 不应包含的错误关键词
                    exclude_keywords = rules.get('exclude_keywords', [])
                    found_error_keywords = []
                    for keyword in exclude_keywords:
                        if keyword.lower() in response_content.lower():
                            found_error_keywords.append(keyword)
                            verification_result["errors"].append(f"包含错误关键词: {keyword}")
                            print(f"⚠️  包含错误关键词: '{keyword}'")
                    
                    if not found_error_keywords:
                        verification_result["checks"].append("✅ 未包含错误关键词")
                        print("✅ 未包含错误关键词")
                    
                    # 检查4: 预期的文件名
                    expected_file = rules.get('expected_file')
                    if expected_file:
                        if expected_file.lower() in response_content.lower():
                            verification_result["checks"].append(f"✅ 包含预期文件: {expected_file}")
                            print(f"✅ 包含预期文件: '{expected_file}'")
                        else:
                            verification_result["errors"].append(f"未找到预期文件: {expected_file}")
                            print(f"⚠️  未找到预期文件: '{expected_file}' (可能文件列表已变化)")
                    
                    # 综合判断
                    if len(verification_result["errors"]) == 0:
                        verification_result["passed"] = True
                        print("\n" + "=" * 60)
                        print("✅ 验证通过：响应包含所有关键信息")
                        print("=" * 60)
                    else:
                        print("\n" + "=" * 60)
                        print(f"⚠️  验证部分通过：{len(verification_result['checks'])} 项通过, {len(verification_result['errors'])} 项失败")
                        print("=" * 60)
                else:
                    print(f"⚠️  未找到验证规则，跳过验证")
                    verification_result["passed"] = True  # 没有规则时默认通过
            else:
                verification_result["errors"].append("未找到响应内容")
                print("❌ 未找到响应内容，无法验证")
            
            # 输出总结
            print("\n" + "=" * 60)
            print("测试总结")
            print("=" * 60)
            print(f"问题: {QUESTION}")
            print(f"响应时间: {response_time:.2f} 秒 ({response_time/60:.1f} 分钟)")
            print(f"响应状态: {'✅ 已收到' if response_found else '⚠️  可能未完全加载'}")
            print(f"验证结果: {'✅ 通过' if verification_result['passed'] else '⚠️  部分通过'}")
            if verification_result["checks"]:
                print(f"通过项: {len(verification_result['checks'])}")
            if verification_result["errors"]:
                print(f"失败项: {len(verification_result['errors'])}")
            
            # 保存响应内容到文件
            if response_content:
                import json
                result_data = {
                    "question": QUESTION,
                    "response_time_seconds": round(response_time, 2),
                    "response_time_minutes": round(response_time / 60, 2),
                    "response_content": response_content,
                    "verification": verification_result,
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
                }
                result_file = "screenshots/share_link_response.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(result_data, f, ensure_ascii=False, indent=2)
                print(f"响应内容已保存: {result_file}")
            
            print(f"截图已保存: screenshots/share_full_step*.png")
            print("=" * 60)
            
        except Exception as e:
            print(f"\\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            await page.screenshot(path="screenshots/share_full_error.png", full_page=True)
        finally:
            # 保持浏览器打开以便观察
            print("\\n💡 浏览器将保持打开 30 秒以便观察")
            await asyncio.sleep(30)
            print("\\n关闭浏览器...")
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_share_link_full())

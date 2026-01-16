# 如何运行 Login and check Account page 测试

## 方法 1: 使用提供的脚本（推荐）

```bash
# 在项目根目录执行
./run_login_test.sh
```

## 方法 2: 手动执行

### 步骤 1: 进入项目目录
```bash
cd /home/mark/dev/browsermcp-automation
```

### 步骤 2: 激活虚拟环境
```bash
source venv/bin/activate
```

### 步骤 3: 设置环境变量（可选）
如果使用默认测试账号，可以跳过此步骤。如果需要使用其他账号：

```bash
export PROTAGO_TEST_EMAIL="your_email@example.com"
export PROTAGO_TEST_PASSWORD="your_password"
```

### 步骤 4: 运行测试
```bash
# 使用默认测试账号
PROTAGO_TEST_EMAIL=xyzdev01@cqigames.com PROTAGO_TEST_PASSWORD="Abc123123?" pytest tests/test_login_and_check_account_page.py -v -s

# 或者如果已经设置了环境变量
pytest tests/test_login_and_check_account_page.py -v -s
```

### 步骤 5: 退出虚拟环境（可选）
```bash
deactivate
```

## 方法 3: 使用 pytest 标记运行

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行所有 e2e 测试
pytest -m e2e -v

# 运行特定测试类
pytest tests/test_login_and_check_account_page.py::TestLoginAndCheckAccountPage -v

# 运行特定测试方法
pytest tests/test_login_and_check_account_page.py::TestLoginAndCheckAccountPage::test_login_and_verify_account_page -v
```

## 测试输出说明

- `-v`: 详细输出模式
- `-s`: 显示 print 输出（不捕获标准输出）

## 测试账号配置

默认测试账号：
- Email: `xyzdev01@cqigames.com`
- Password: `Abc123123?`

可以通过环境变量覆盖：
```bash
export PROTAGO_TEST_EMAIL="your_email@example.com"
export PROTAGO_TEST_PASSWORD="your_password"
```

## 截图位置

测试过程中生成的截图保存在：
```
screenshots/test_login_step*.png
```

## 常见问题

### 1. 虚拟环境不存在
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Playwright 浏览器未安装
```bash
playwright install chromium
```

### 3. 测试超时
测试默认超时时间较长（约 30-60 秒），如果网络较慢可能需要等待。

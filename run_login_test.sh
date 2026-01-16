#!/bin/bash
# 运行 Login and check Account page 测试脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "错误: 虚拟环境不存在，请先运行: python3 -m venv venv"
    exit 1
fi

# 设置测试账号环境变量（如果未设置）
if [ -z "$PROTAGO_TEST_EMAIL" ]; then
    export PROTAGO_TEST_EMAIL="xyzdev01@cqigames.com"
fi

if [ -z "$PROTAGO_TEST_PASSWORD" ]; then
    export PROTAGO_TEST_PASSWORD="Abc123123?"
fi

# 运行测试
echo "=========================================="
echo "运行 Login and check Account page 测试"
echo "=========================================="
echo "测试账号: $PROTAGO_TEST_EMAIL"
echo "=========================================="
echo ""

pytest tests/test_login_and_check_account_page.py -v -s

# 退出虚拟环境
deactivate

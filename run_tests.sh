#!/bin/bash
# 运行测试的便捷脚本

# 激活虚拟环境
source venv/bin/activate

# 运行测试
if [ -z "$1" ]; then
    # 如果没有参数，运行所有测试
    pytest tests/ -v
else
    # 运行指定的测试
    pytest "$@" -v
fi

#!/bin/bash

# Skill Creator Pro 测试脚本

echo "🧪 Skill Creator Pro 测试"
echo "=========================="
echo ""

# 1. 检查安装
echo "1. 检查安装状态..."
if [ -L ~/.openclaw/skills/skill-creator-pro ]; then
    echo "   ✅ 已安装（符号链接）"
    ls -la ~/.openclaw/skills/skill-creator-pro
else
    echo "   ❌ 未安装"
    exit 1
fi

echo ""
echo "2. 检查文件结构..."
FILES=(
    "SKILL.md"
    "skill.json"
    "main.py"
    "src/orchestrator.py"
    "README.md"
)

for file in "${FILES[@]}"; do
    if [ -f "/Users/pxb/.openclaw/workspace/skills/skill-creator-pro/$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (缺失)"
    fi
done

echo ""
echo "3. 检查目录结构..."
DIRS=("src" "scripts" "references" "tests" "output")
for dir in "${DIRS[@]}"; do
    if [ -d "/Users/pxb/.openclaw/workspace/skills/skill-creator-pro/$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❌ $dir/ (缺失)"
    fi
done

echo ""
echo "4. 测试运行（模拟模式）..."
cd /Users/pxb/.openclaw/workspace/skills/skill-creator-pro
python3 main.py "帮我创建一个测试 skill" test-skill P1 2>&1 | head -30

echo ""
echo "=========================="
echo "✅ 测试完成！"
echo ""
echo "📁 Skill 位置：/Users/pxb/.openclaw/workspace/skills/skill-creator-pro/"
echo "🔗 安装位置：~/.openclaw/skills/skill-creator-pro"
echo ""
echo "🚀 使用方法："
echo "   python3 main.py \"帮我创建一个 xxx skill\""
echo ""

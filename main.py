#!/usr/bin/env python3
"""
Skill Creator Pro - 多 Agent 协作的 Skill 创建框架

从用户粗想法到高质量 Skill 的全流程实现
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('skill-creator-pro')

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from orchestrator import SkillCreatorOrchestrator


def run(idea: str, skill_name: str = None, priority: str = "P1", iteration_mode: bool = True):
    """
    Skill Creator Pro 主入口
    
    Args:
        idea: 用户粗想法描述
        skill_name: Skill 名称（可选）
        priority: 优先级 P0/P1/P2
        iteration_mode: 是否启用多轮迭代
    
    Returns:
        dict: 创建结果
    """
    logger.info(f"🚀 Skill Creator Pro 启动")
    logger.info(f"📝 想法：{idea}")
    logger.info(f"🎯 优先级：{priority}")
    logger.info(f"🔄 迭代模式：{iteration_mode}")
    
    # 初始化编排器
    orchestrator = SkillCreatorOrchestrator(
        workspace=os.getenv('OPENCLAW_WORKSPACE', '/Users/pxb/.openclaw/workspace'),
        iteration_mode=iteration_mode
    )
    
    # 执行 8 阶段工作流
    result = orchestrator.create_skill(
        idea=idea,
        skill_name=skill_name,
        priority=priority
    )
    
    # 输出结果
    print_result(result)
    
    return result


def print_result(result: dict):
    """打印结果"""
    print("\n" + "="*60)
    
    if result.get('success'):
        print("✅ **Skill 创建成功！**\n")
        
        skill = result.get('skill', {})
        print(f"📁 **名称**: {skill.get('name')}")
        print(f"🏷️ **版本**: {skill.get('version')}")
        print(f"📂 **目录**: {skill.get('directory')}")
        
        print(f"\n📄 **生成文件**:")
        for file in skill.get('files', []):
            print(f"   - {file}")
        
        quality = result.get('quality', {})
        print(f"\n📊 **质量评分**:")
        print(f"   完整性：{quality.get('completeness_score', 0)}/100")
        print(f"   架构分：{quality.get('architecture_score', 0)}/100")
        print(f"   测试覆盖：{quality.get('test_coverage', 0)}/100")
        print(f"   综合评分：{quality.get('overall_score', 0)}/100")
        
        process = result.get('process', {})
        print(f"\n🔄 **流程信息**:")
        print(f"   迭代轮次：{process.get('iterations', 0)}")
        print(f"   参与 Agent: {', '.join(process.get('agents_involved', []))}")
        print(f"   追问次数：{process.get('clarifications_count', 0)}")
        
        execution = result.get('execution', {})
        print(f"\n⏱️  **执行信息**:")
        print(f"   耗时：{execution.get('duration_ms', 0)/1000:.1f}秒")
        print(f"   成本：¥{execution.get('cost', 0):.2f}")
        
        if result.get('installed'):
            print(f"\n✅ **已安装到 OpenClaw**")
        
    else:
        print("❌ **Skill 创建失败**\n")
        print(f"错误：{result.get('error', '未知错误')}")
        
        if result.get('suggestions'):
            print(f"\n💡 **建议**:")
            for suggestion in result.get('suggestions', []):
                print(f"   - {suggestion}")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    # 命令行调用示例
    if len(sys.argv) < 2:
        print("用法：python main.py <粗想法描述> [skill 名称] [优先级]")
        print("\n示例:")
        print("  python main.py '帮我创建一个需求文档管理的 skill'")
        print("  python main.py '记忆宫殿训练' memory-palace P1")
        sys.exit(1)
    
    idea = sys.argv[1]
    skill_name = sys.argv[2] if len(sys.argv) > 2 else None
    priority = sys.argv[3] if len(sys.argv) > 3 else "P1"
    
    result = run(idea, skill_name, priority)
    
    sys.exit(0 if result.get('success') else 1)

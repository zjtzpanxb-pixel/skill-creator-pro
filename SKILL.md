# Skill Creator Pro - 多 Agent 协作的 Skill 创建框架

> 从粗想法到高质量 Skill 的全流程方法论

## 触发条件

**飞书消息/对话**：
- "帮我创建一个 skill"
- "把这个想法落地成 skill"
- "设计一个 xxx skill"
- "优化现有的 skill"
- "创建 skill"

**命令行**：
```bash
openclaw skill-pro create <skill-name> --idea "<粗想法描述>"
openclaw skill-pro optimize <skill-name>
```

## 功能描述

基于多 Agent 协作和 8 阶段方法论，从用户的粗想法自动生成完整的 Skill 包：

### 核心能力
1. **需求澄清** - 5W1H 追问 + SMART 校验 + 反向追问
2. **架构设计** - 4 层架构 + 状态机 + 数据流
3. **多 Agent 协作** - 需求分析师/架构师/工程师/验证师
4. **迭代优化** - 多轮评审改进
5. **完整交付** - SKILL.md + scripts/ + references/ + assets/

### 8 阶段工作流
```
1. 需求澄清 → 2. 架构设计 → 3. 接口定义 → 4. 实现规划
     ↓                                              ↓
8. 部署准备 ← 7. 测试验证 ← 6. 代码生成 ← 5. 多 Agent 协作
```

## 输入

```json
{
  "idea": "string (用户粗想法，10-500 字)",
  "context": {
    "skill_name": "string (可选，skill 名称)",
    "priority": "P0|P1|P2 (可选，默认 P1)",
    "iteration_mode": true|false (可选，默认 true，是否多轮迭代)
  },
  "clarifications": [
    {
      "question": "string (5W1H 追问)",
      "answer": "string (用户回答)"
    }
  ]
}
```

## 输出

```json
{
  "skill": {
    "name": "string",
    "version": "v1.0",
    "directory": "string (skill 目录路径)",
    "files": ["SKILL.md", "src/main.py", "scripts/", "references/"],
    "triggers": ["string"],
    "parameters": {}
  },
  "process": {
    "stage": "string (当前阶段)",
    "iterations": number (迭代轮次),
    "agents_involved": ["Analyst", "Architect", "Engineer", "Validator"],
    "clarifications_count": number (追问次数)
  },
  "quality": {
    "completeness_score": 0-100,
    "architecture_score": 0-100,
    "test_coverage": 0-100,
    "overall_score": 0-100
  },
  "execution": {
    "duration_ms": number,
    "model_used": "string",
    "token_used": number,
    "cost": number
  }
}
```

## 配置

```yaml
# LLM 配置
llm:
  primary: qwen3.5-plus
  fallback: qwen2
  timeout: 120
  max_retries: 3

# Agent 配置
agents:
  analyst:
    model: qwen3.5-plus
    temperature: 0.7
  architect:
    model: qwen3.5-plus
    temperature: 0.5
  engineer:
    model: qwen3.5-plus
    temperature: 0.3
  validator:
    model: qwen3.5-plus
    temperature: 0.4

# 迭代配置
iteration:
  max_rounds: 3
  min_score: 80
  auto_approve_threshold: 95

# 成本配置
cost:
  daily_limit: 50
  monthly_limit: 200
  estimate_per_skill: 5.0

# 输出配置
output:
  workspace: /Users/pxb/.openclaw/workspace/skills/
  auto_install: true
  backup: true
```

## 多 Agent 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator (主 Agent)                       │
│  职责：流程编排 · 任务分派 · 质量把关 · 多轮协调                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
    ┌───────────────┬───────┼───────┬───────────────┐
    ▼               ▼       ▼       ▼               ▼
┌─────────┐   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Analyst  │   │Architect│ │Engineer │ │Validator│ │Reporter │
│需求分析  │   │架构设计  │ │代码实现  │ │质量验证  │ │文档生成  │
└─────────┘   └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### Agent 职责

| Agent | 职责 | 输出 |
|-------|------|------|
| **Analyst** | 5W1H 追问、SMART 校验、需求抽取 | 需求文档、用户故事 |
| **Architect** | 4 层架构、状态机、数据流设计 | 架构文档、接口定义 |
| **Engineer** | SKILL.md 编写、脚本实现 | 完整 Skill 代码 |
| **Validator** | 测试用例、验收标准、鲁棒性审查 | 测试报告、质量评分 |
| **Reporter** | 文档生成、进度汇报 | 进度报告、最终交付物 |

## 工作流程

```
1. 接收请求 → 解析用户粗想法
         ↓
2. 需求澄清 → Analyst 发起 5W1H 追问（最多 3 轮）
         ↓
3. 架构设计 → Architect 设计 4 层架构 + 状态机
         ↓
4. 接口定义 → 定义触发条件、参数、输出格式
         ↓
5. 多 Agent 协作 → Engineer 编写代码，Validator 审查
         ↓
6. 代码生成 → 生成 SKILL.md + scripts/ + references/
         ↓
7. 测试验证 → 生成测试用例 + 执行验收
         ↓
8. 部署准备 → 安装到 OpenClaw + 备份
```

## 降级策略

| 故障 | 应对 |
|------|------|
| LLM 超时 | 重试 3 次（指数退避）→ 降级 qwen2 |
| 用户不回答追问 | 静默降级（基于假设继续，标记待确认） |
| 架构设计冲突 | 启动冲突调解 → 简化架构 |
| 测试失败 | 自动修复 → 标记问题 → 人工介入 |
| 成本超支 | 建议精简版 → 用户拒绝则中止 |
| 连续失败 | >3 次触发告警 → 建议人工处理 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| SCP-101 | 输入格式错误 |
| SCP-102 | 需求过于模糊 |
| SCP-201 | 需求澄清超时 |
| SCP-202 | 用户未回答追问 |
| SCP-301 | 架构设计冲突 |
| SCP-401 | 代码生成失败 |
| SCP-501 | 测试验证失败 |
| SCP-502 | 安装失败 |
| SCP-601 | 成本超支 |

## 监控指标

- **成功率**：>90%
- **P95 延迟**：<10 分钟
- **单次成本**：<¥5
- **需求完整率**：>85%
- **测试覆盖率**：>80%
- **用户满意度**：>4.5/5

## 示例

### 示例 1：创建需求文档管理 skill

```
用户：帮我创建一个需求文档管理的 skill

Agent 追问：
1. 谁用这个 skill？（产品经理/需求分析师）
2. 输入是什么？（需求描述/会议记录/飞书消息）
3. 输出是什么？（PRD 文档/需求列表）
4. 在哪使用？（飞书/命令行）
5. 成功标准？（需求完整率>90%）

输出：
✅ Skill 创建成功
📁 目录：/Users/pxb/.openclaw/workspace/skills/requirement-doc-manager/
📄 文件：SKILL.md, main.py, scripts/, references/
📊 质量评分：97/100
🧪 测试覆盖：63 个用例
✅ 已安装到 OpenClaw
```

### 示例 2：命令行创建

```bash
openclaw skill-pro create memory-palace \
  --idea "创建记忆思维宫殿训练的网站" \
  --priority P1
```

### 示例 3：优化现有 skill

```bash
openclaw skill-pro optimize weather-skill
```

## 相关文件

- `SKILL.md` - Skill 定义文件
- `src/orchestrator.py` - 主编排器
- `src/agents/` - 多 Agent 实现
- `templates/` - Skill 模板
- `references/` - 参考资料库
- `tests/` - 测试用例

## 版本

- 当前版本：v1.0
- 创建日期：2026-03-15
- 最后更新：2026-03-15
- 基于框架：skill-creator-pro-framework v1.0

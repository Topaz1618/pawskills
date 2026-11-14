# AI Agent 工程规范集

面向 AI 编码 Agent 的 **17 条工程规范**，以可移植的 Markdown Skill 形式分发。

每一条规范都是一份自包含的指令文档。Agent 读完之后，会确切知道对自己的要求：任务范围如何界定、已有代码何时必须复用、日志该记录什么、如何验证、以及如何如实汇报结果。

[English](README.md)

---

## 这套规范解决什么问题

AI 编码 Agent 的失败方式是有规律可循的。这些规范来自真实软件开发中反复出现的失败，而不是理论推演：

- 重跑已经完成的工作。
- 重复实现已经存在的函数。
- 交付没有明确定义接口契约的模块。
- 用加工过的摘要替代原始执行日志。
- 在没有实际验证的情况下宣称任务完成。
- 用户问的是问题，Agent 却去做用户没要求的操作。
- 把明确的指令改写成 Agent 自己偏好的做法。
- 用类型声明代替真实数据来描述数据结构。
- 把计划描述成已完成的工作。

这里每一条规范都针对其中一种失败模式。合在一起，它们定义了 Agent 眼中"完成"的含义。

---

## 17 条规范

| 序号 | Skill | 核心职责 |
|---|---|---|
| 01 | `task-execution-governance` | 任务识别、执行范围、规范协调 |
| 02 | `user-intent-priority` | 用户意图识别、响应优先级、工具调用闸门 |
| 03 | `engineering-context-completeness` | 问题上下文、逻辑链、改动前实施方案 |
| 04 | `data-first-execution` | 已有数据优先，禁止无依据重跑 |
| 05 | `code-asset-inventory` | 代码资产盘点、函数复用 |
| 06 | `interface-contract` | 接口契约、数据结构统一 |
| 07 | `data-audit-reproducibility` | 原始数据、数据审计、复现 |
| 08 | `production-logging` | 原始日志、执行路径、异常记录 |
| 09 | `testing-verification` | 测试、验证、独立审查 |
| 10 | `engineering-transparency` | 工程透明度、文件与函数说明 |
| 11 | `technical-documentation` | 技术文档真实性与完整性 |
| 12 | `documentation-structure` | 文档组织和阅读顺序 |
| 13 | `language-expression` | 语言表达和术语规范 |
| 14 | `change-report-delivery` | 变更报告与交付 |
| 15 | `unfinished-work-tracking` | 未完成事项追踪 |
| 16 | `explicit-instruction-fidelity` | 忠实执行明确指令，禁止擅自改写 |
| 17 | `repository-publication-hygiene` | 仓库发布卫生；私有引用与工具署名不得进入公开内容 |

---

## 仓库结构

```
agent-engineering-standards/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── SECURITY.md
│
├── skills/
│   ├── task-execution-governance/SKILL.md
│   ├── user-intent-priority/SKILL.md
│   ├── engineering-context-completeness/SKILL.md
│   ├── data-first-execution/SKILL.md
│   ├── code-asset-inventory/SKILL.md
│   ├── interface-contract/SKILL.md
│   ├── data-audit-reproducibility/SKILL.md
│   ├── production-logging/SKILL.md
│   ├── testing-verification/SKILL.md
│   ├── engineering-transparency/SKILL.md
│   ├── technical-documentation/SKILL.md
│   ├── documentation-structure/SKILL.md
│   ├── language-expression/SKILL.md
│   ├── change-report-delivery/SKILL.md
│   ├── unfinished-work-tracking/SKILL.md
│   ├── explicit-instruction-fidelity/SKILL.md
│   └── repository-publication-hygiene/SKILL.md
│
├── profiles/
│   ├── full.yaml
│   ├── data.yaml
│   ├── development.yaml
│   ├── lightweight.yaml
│   ├── full-engineering/README.md
│   ├── data-engineering/README.md
│   ├── development/README.md
│   └── lightweight/README.md
│
├── adapters/
│   ├── claude-code/README.md
│   ├── codex/README.md
│   ├── cursor/README.md
│   └── generic-agent/README.md
│
├── references/
│   ├── engineering-principles.md
│   ├── terminology.md
│   └── audit-data-model.md
│
├── scripts/
│   ├── install.py
│   ├── validate.py
│   └── check-links.py
│
└── tests/
    ├── test_install.py
    ├── test_skill_structure.py
    ├── test_frontmatter.py
    └── fixtures/
```

---

## Profiles

不是所有团队都需要全部 17 条规范。数据团队可能只需要 4 条，独立开发者可能只需要 2 条。Profile 是机器可读的 YAML 文件，声明某种工作方式需要哪些 Skill。

| Profile | 包含规范 | 适用场景 |
|---|---|---|
| [`full.yaml`](profiles/full.yaml) | 全部 17 条 | 需要完整工程基线的团队 |
| [`data.yaml`](profiles/data.yaml) | 11 条 | 数据工程、分析与研究类工作 |
| [`development.yaml`](profiles/development.yaml) | 12 条 | 日常功能开发 |
| [`lightweight.yaml`](profiles/lightweight.yaml) | 7 条 | 小型或探索性工作的最低护栏 |

每个 profile 目录下都有一个 README，说明何时选择它以及它具体约束了什么。

---

## 安装

```bash
git clone <repository-url>
cd pawskills
python3 scripts/install.py --agent codex --profile full
```

到此为止。安装脚本会把 Skill 目录复制到目标 Agent 的 skills 目录，并记录安装清单，以便后续卸载。

### 支持的 Agent

| Agent | 项目级 | 用户级 |
|---|---|---|
| `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| `codex` | `.agents/skills/` | `~/.agents/skills/` |
| `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |

### 安装范围

| 范围 | 参数 | 目标目录 |
|---|---|---|
| 当前项目 | `--scope project`（默认） | `<project-dir>/.agents/skills/` 或 `<project-dir>/.claude/skills/` |
| 当前用户 | `--scope user` | `~/.agents/skills/` 或 `~/.claude/skills/` |

用 `--project-dir /path/to/project` 可以安装到当前目录之外的其他项目。

### 按 Profile 安装

Profile 是 `profiles/*.yaml` 中声明的一组具名 Skill。

```bash
python3 scripts/install.py --agent codex --profile full
python3 scripts/install.py --agent claude-code --profile data
python3 scripts/install.py --agent codex --profile development
python3 scripts/install.py --agent codex --profile lightweight
```

### 单独安装 Skill

```bash
python3 scripts/install.py --agent codex --skill production-logging
python3 scripts/install.py --agent codex --skill production-logging --skill testing-verification
```

`--skill` 可重复使用，也可以与 `--profile` 组合。

### 查看可用内容

```bash
python3 scripts/install.py --list
```

输出全部 Skill 及其说明，以及全部 Profile 及其包含的 Skill。

### 覆盖保护

默认不覆盖已有 Skill。冲突的 Skill 会标记为 `SKIPPED`，其余 Skill 继续安装。

```bash
python3 scripts/install.py --agent codex --profile full --force
```

使用 `--force` 时，旧版本会先备份到 `.pawskills-backups/` 再被替换。

### 预览

```bash
python3 scripts/install.py --agent codex --profile full --dry-run
```

输出每个 Skill 的来源路径、目标路径、冲突状态，以及将被覆盖的文件。整个过程不创建、不修改、不删除任何文件。

### 卸载

```bash
python3 scripts/install.py --agent codex --profile full --uninstall
python3 scripts/install.py --agent codex --skill production-logging --uninstall
```

只卸载记录在 Pawskills 清单中的 Skill。用户自己创建的 Skill 保持不动；安装后被用户修改过的文件会被提示并跳过，除非加上 `--force`。

### 常见错误

| 提示 | 原因 | 处理方式 |
|---|---|---|
| `--agent is required` | 未指定 Agent | 加上 `--agent claude-code` 或 `--agent codex` |
| `Unknown profile '...'` | Profile 名称不存在 | 用 `--list` 查看可用 Profile |
| `Skill '...' does not exist` | Skill 名称不在 `skills/` 下 | 用 `--list` 查看可用 Skill |
| `skipped, target already exists` | 目标已存在 | 用 `--force` 覆盖 |
| `modified after installation` | 安装后文件被修改 | 用 `--force` 一并删除 |

---

## Skill 格式

每个 Skill 是一个带 YAML frontmatter 的 Markdown 文件：

```yaml
---
name: production-logging
description: Production logging standard. Requires recording real execution facts...
trigger: log, logging, logger, 日志, 排错, trace, audit
---
```

- `name` — 唯一标识，必须与 Skill 目录名完全一致。
- `description` — 这条规范要求什么，以及在什么情况下适用。
- `trigger` — 应当让 Agent 加载该 Skill 的关键词。

正文是写给 Agent 的直接指令，而不是关于这条规范的论述。

---

## 校验

```bash
python3 scripts/validate.py          # 校验 Skill 结构、frontmatter 与 Profile
python3 scripts/check-links.py        # 检查内部链接
python3 -m pytest tests/ -v           # 运行测试
```

测试全部在临时目录中执行，不会修改真实项目。

---

## Cursor 规则

本仓库提供两份 Cursor 规则文件。它们不是 Skill：规则由 Cursor 自己在每次提问时注入，而 Skill 由 Agent 在任务需要时才加载。

| 文件 | 生效范围 | 内容 |
|---|---|---|
| `.cursor/rules/engineering-context.mdc` | 本仓库 | 上下文、逻辑完整性与实施权限约束，`alwaysApply: true` |
| `~/.cursor/rules/global-engineering-behavior.mdc` | 所有项目 | 全局工程行为约束，`alwaysApply: true` |

项目规则与 `engineering-context-completeness` Skill 的义务一致，因此在 Cursor 中无论该 Skill 是否被触发，约束都生效。

若需要在所有项目中生效，而不限于当前处理的工作内容，请同时添加全局规则：`Cursor Settings` → `Rules` → `User Rules`。填在这里的规则保存在 Cursor 账号中，并注入每一次 Agent 对话；它们不保存在本仓库。

---

## 参考文档

这些不是规范——Agent 不需要加载它们。它们解释规范背后的逻辑和用词。

| 文档 | 内容 |
|---|---|
| [工程原则](references/engineering-principles.md) | 所有规范共同遵守的十一条原则，以及它们与各条 Skill 的对应关系 |
| [术语表](references/terminology.md) | 受控词汇，以及本仓库刻意不使用的表达 |
| [审计数据模型](references/audit-data-model.md) | `data-audit-reproducibility` 背后的具体记录结构 |

## Agent 适配器

| 适配器 | 适用对象 |
|---|---|
| [Claude Code](adapters/claude-code/README.md) | `.claude/skills/` 目录结构的安装与校验 |
| [Codex](adapters/codex/README.md) | `.agents/skills/` 目录结构的安装与校验 |
| [通用 Agent](adapters/generic-agent/README.md) | 没有 skills 目录的 Agent 如何使用这些规范 |

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增规范必须遵循相同结构，保持自包含，并且针对具体失败模式，而不是重复已有内容。

---

## 许可证

基于 MIT 许可证发布，详见 [LICENSE](LICENSE)。

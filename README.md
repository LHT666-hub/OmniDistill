# 蒸馏大满贯 OmniDistill

OmniDistill 是一个“蒸馏元 Skill”：把人物、学者、论文语料、知识库、成功与失败案例、岗位经验、项目记录和长期交互，转化为**证据可追踪、规则可执行、能力可测试、后续可更新**的 Skill 包。

它不训练模型权重。它把隐性知识工程化为：

- Knowledge：知道什么
- Taste：什么值得做、什么算强证据
- Heuristics：信息不完整时如何判断
- Workflows：具体任务如何执行
- Anti-patterns：哪些做法容易失败
- Boundaries：何时不应推断、执行或冒充

## 为什么需要它

现有蒸馏项目往往只覆盖一个方向：人物思维、学术导师、知识库、成功案例、科研工作流或持续学习。OmniDistill 将这些路线统一为一套协议，并补上四个常被忽略的环节：

1. Claim–Evidence 证据账本
2. 个人、团队、论文与项目的归因边界
3. 已知任务、前向任务、对照任务和边界任务验证
4. 新材料和反馈的增量更新，而不是一次性生成

## 支持的模式

- 人物思维 `person-thinking`
- 工作专家 `work-expert`
- 学术导师 `research-mentor`
- 知识库 `corpus`
- 案例模式 `case-pattern`
- 项目复盘 `project-retro`
- 自我成长 `self-evolution`
- 多模式组合 `hybrid`

## 快速开始

向支持 Skill 的 Agent 提出：

> 把这些材料蒸馏成一个可执行 Skill。先判断蒸馏模式，建立证据账本，然后生成工作流、启发式、反模式、限制和前向测试。不要把总结冒充能力，也不要模仿真实人物身份。

或使用脚本初始化一个标准工作区：

```bash
python scripts/init_distillation_workspace.py \
  --target "目标名称" \
  --mode research-mentor \
  --tier standard \
  --output-root ./workspaces
```

完成目标 Skill 后执行：

```bash
python scripts/validate_distillation_package.py ./workspaces/<slug>/output/<slug>
```

## 版本

- v0：资料与结构脚手架
- v1：可追溯的证据地图
- v2：可执行的操作型 Skill
- v3：通过前向、对照和边界测试的验证型 Skill

版本代表证据和测试强度，不代表文案长度。

## 项目结构

```text
omni-distill/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
│   ├── init_distillation_workspace.py
│   └── validate_distillation_package.py
└── references/
    ├── mode-router.md
    ├── evidence-protocol.md
    ├── synthesis-protocol.md
    ├── package-spec.md
    ├── validation-protocol.md
    ├── update-protocol.md
    ├── source-and-ethics.md
    └── sample-prompts.md
```

## 设计原则

- 默认提炼能力，不默认模拟身份。
- 强结论必须绑定证据和反证。
- 知识、品味、启发式和工作流分层保存。
- 成功案例必须尽量配合失败案例和情境条件。
- 合著成果与团队流程不得无条件归因给个人。
- 搜索摘要用于发现线索，不用于支撑强规则。
- 达不到版本门槛时诚实降级。

## 致谢

本项目在设计层面参考了人物思维蒸馏、学术导师蒸馏、基金写作经验蒸馏、科研工作流和引用核验等开源实践，包括 Nuwa Skill、MentorForge、Chinese Grant Writer Skills、Supervisor-Skills 和 Academic Reference Matcher。OmniDistill 的协议、文件结构与脚本为独立实现。

## License

MIT

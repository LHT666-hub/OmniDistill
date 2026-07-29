# OmniDistill · 蒸馏大满贯

OmniDistill 是一个证据驱动的元 Skill：把人物、专家、学者、文档语料、案例、项目历史和长期反馈，转化为**可追踪、可执行、可验证、可更新**的 Agent Skill。

它不训练模型权重，也不把摘要包装成专家。完整输出必须包含：

```text
Knowledge + Taste + Heuristics + Workflows
+ Anti-patterns + Boundaries + Evidence + Tests
```

## 与第一版的区别

第一版只有概念说明。当前版本增加了可运行的生产线：

- 七种可组合蒸馏模式和可审查路由器；
- 带哈希、权利、同意和独立来源分组的来源登记；
- Claim–Evidence 账本及强制晋升门槛；
- 个人、团队、合作者、机构和未知归因；
- 知识、品味、启发式、工作流、反模式和边界的独立合成；
- known、forward、contrast、boundary、adversarial 五类测试；
- v0–v3 自动核验，拒绝虚报等级；
- 观察、候选、测试、接受、修订和废止的规则生命周期；
- 生成包快照、回滚基础和 ZIP 打包。

## 快速开始

```bash
python scripts/init_distillation_workspace.py \
  --target "某位学者" \
  --purpose "评估选题并批评论文设计" \
  --tier v2 \
  --output-root ./workspaces
```

将授权材料放入 `workspaces/<slug>/sources/raw/`，然后：

```bash
python scripts/route_modes.py \
  --brief "把论文、访谈、课程和课题组项目蒸馏成科研导师" \
  --output workspaces/<slug>/route.json

python scripts/register_sources.py workspaces/<slug>
python scripts/validate_evidence_ledger.py workspaces/<slug>
python scripts/assemble_skill.py workspaces/<slug>
python scripts/validate_distillation_package.py \
  workspaces/<slug>/output/<skill-name>
```

通过验证后打包：

```bash
python scripts/package_skill.py \
  workspaces/<slug>/output/<skill-name> \
  --output ./dist
```

`assemble_skill.py` 不会替模型凭空提炼能力。Agent 或研究者需要先审阅证据账本并填写 `extraction/capability.json`；脚本负责保证结构、链接、门槛和包的一致性。

## 支持模式

| 模式 | 蒸馏目标 |
|---|---|
| `person-thinking` | 心智模型、决策启发式、内在张力 |
| `work-expert` | SOP、检查点、异常处理、升级规则 |
| `research-mentor` | 选题品味、方法选择、证据标准 |
| `corpus` | 知识地图、层级导航、概念关系 |
| `case-pattern` | 成功/失败案例中的条件性模式 |
| `project-retro` | 架构决策、复现路径、踩坑规则 |
| `self-evolution` | 反馈、错误和偏好的规则生命周期 |

模式不是互斥标签。蒸馏一位教授时，常见组合是：

```text
research-mentor + person-thinking + corpus + work-expert
```

## 质量等级

- `v0`：脚手架、用途、权限、模式和来源清单；
- `v1`：通过验证的来源—主张证据链；
- `v2`：可执行启发式、工作流、反模式和边界；
- `v3`：五类行为测试经过独立或人工复核，并具备版本构建链与回滚能力。

等级代表证据和验证强度，不代表文案长度。

## 参考项目

OmniDistill 在方法论层面参考了：

- [colleague-skill / dot-skill](https://github.com/titanwings/colleague-skill)
- [Nuwa Skill](https://github.com/alchaincyf/nuwa-skill)
- [MentorForge](https://github.com/qwqalice/MentorForge)
- [Chinese Grant Writer Skills](https://github.com/HuiyuLi-2000/Chinese-Grant-Writer-Skills)
- [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)
- [Corpus2Skill](https://github.com/dukesun99/Corpus2Skill)
- [OpenKB](https://github.com/VectifyAI/OpenKB)
- [self-improving-agent](https://github.com/peterskoett/self-improving-agent)
- [Academic Reference Matcher](https://github.com/keros68/academic-reference-matcher-skill)

具体借鉴点、局限和 OmniDistill 的回应见 [`references/reference-projects.md`](references/reference-projects.md) 与 [`docs/DESIGN_RATIONALE.md`](docs/DESIGN_RATIONALE.md)。

本项目为独立实现，不复制第三方项目的具体 Skill 文本。引用项目许可证各不相同；尤其不能把 CC BY-NC-SA 内容直接重新发布为 MIT。

## 测试

```bash
python scripts/doctor.py
python -m unittest discover -s tests -v
```

测试覆盖模式路由、重复初始化保护、来源登记、弱证据拒绝、v2 端到端生成与打包、v3 门槛及规则冲突阻断。

## License

MIT

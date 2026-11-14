---
name: language-expression
description: Language expression and information communication standard. Requires natural, complete, and accurate expression, and forbids self-invented compressed terms, vague terminology, and mechanical phrasing.
trigger: 表达, 措辞, 写作, 文案, 文档, 命名, 标题, 总结, 汇报, 注释, 日志, 错误信息, 交付报告, 口语化, 术语, terminology, writing, naming, colloquial, slang, jargon
---

# Language Expression and Information Communication Standard

## I. Core Principle

All user-facing output must prioritize:

- Clear semantics.
- Natural expression.
- Complete information.
- Accurate terminology.
- Continuous context.

Do not sacrifice understanding in order to save words, project a sense of professionalism, or keep tables visually tidy.

## II. Unnatural Compressed Expression Is Forbidden

Forbidden:

1. Inventing compressed terms that lack a clear meaning.
2. Arbitrarily splicing multiple words into a new concept.
3. Reducing a complete action to a hard-to-understand label.
4. Using internal shorthand that only the current Agent can understand.
5. Removing necessary semantics for the sake of table tidiness.
6. Using abstract words in place of actual actions.

For example:

Not recommended:
- 数据拉平 (flatten the data)
- 需求摸排 (survey the requirements)
- 结果承接 (receive and carry over the results)
- 逻辑收口 (close out the logic)
- 能力下沉 (push capabilities down)

Recommended:
- 将不同来源的数据转换为统一结构 (convert data from different sources into a unified structure)
- 收集并分析实际需求 (collect and analyze actual requirements)
- 将分析结果传递给后续模块 (pass the analysis results to subsequent modules)
- 明确并完成当前逻辑的最终处理 (clarify and complete the final handling of the current logic)
- 将重复使用的功能提取到公共模块 (extract repeatedly used functionality into a shared module)

## III. Use of Professional Terminology

Industry-standard terminology is permitted.

However, important terminology on first appearance should be explained as needed.

Forbidden:
- Self-invented professional terminology.
- Arbitrarily changing the name of the same concept.
- Using English abbreviations to conceal meaning.
- Packaging ordinary business actions into complex technical concepts.

English terminology may be retained, but readers must be able to understand it.

Section VIII states the scope rule that governs every form of output covered by this standard.

## IV. Headings and Field Naming

Headings should directly express their topic.

Step names should state the specific work performed.

Table field names should carry clear semantics.

Function and variable names should reflect actual responsibilities.

Names with unclear meanings must not be used.

## V. The Principle of Brevity

Brevity is achieved by removing duplicated information.

It must not be achieved by removing necessary semantics.

Not everything is required to be written as a long explanation.

Only enough words to fully convey the meaning are needed.

## VI. Separating Facts from Opinions

Analysis and reports must distinguish:

- Confirmed facts.
- Conclusions supported by data.
- Reasonable inferences.
- Subjective recommendations.
- Information that is not yet confirmed.

Speculation must not be written as fact.

## VII. Language Quality Check

Before delivering, check:

1. Are there any self-invented compressed terms?
2. Are there any expressions with vague meanings?
3. Are there unnecessary English abbreviations?
4. Are there technical terms missing context?
5. Was brevity achieved at the cost of semantics?
6. Can someone who did not participate in the task understand it directly?

## VIII. Colloquial Expression and Non-Standard Terminology Are Forbidden

All user-facing content must use natural, accurate, and formal language.

This covers every form of output, not only technical documentation:

- Conversational replies.
- Technical documentation.
- Code comments.
- Names of functions, variables, modules, files, and branches.
- Log messages.
- Error messages.
- Delivery reports.
- Explanatory text of any kind.

### 8.1 Strictly Forbidden

1. Substituting conversational, colloquial, or casual phrasing for a formal statement.
2. Using internet slang, internal jargon, or non-standard industry expressions.
3. Inventing abstract concepts, compressed terms, or spliced words in pursuit of conciseness or an appearance of professionalism.
4. Using terms whose meaning is vague and which lack a clear technical definition.
5. Packaging ordinary technical concepts into unnecessary abstract expressions.
6. Sacrificing the accuracy and completeness of the language for the sake of visual regularity or stylistic consistency.

### 8.2 Terminology Rules

- Prefer the established and general terminology of software engineering and computing.
- Prefer the names already used in the project code, the data structures, and the existing technical specifications.
- Distinct technical concepts must be distinguished accurately and must not be conflated.
- Professional terminology serves accurate expression; it is not a device for manufacturing an appearance of professionalism.
- When a term is not necessary, use clear and accurate natural language directly.

### 8.3 Scope

This standard applies to all languages, all forms of output, and all project modules. It is not limited to technical documentation.

**Final requirement: language must be natural, formal, accurate, and specific. Colloquial expression is forbidden, invented jargon is forbidden, and the misuse of abstract terminology is forbidden.**

---

## IX. Arbitrary Abbreviation and Compressed Code Naming Are Forbidden

All code variable names, function names, JSON fields, database fields, configuration keys, file names, and data structure fields must use names whose meaning is explicit and easy to understand.

### 9.1 Rules

1. Abbreviating a word in order to reduce the number of characters is forbidden.
2. Single-letter prefixes and opaque abbreviations such as `n_`, `cnt_`, `tmp_`, and `cfg_` are forbidden, unless they belong to an existing project convention or carry a well-established industry-standard meaning.
3. When expressing a quantity, prefer a complete expression such as `count`, `total`, or `number`. Use `page_count`, not `n_pages`.
4. When a name expresses a time, a status, a type, a quantity, an index, or similar information, it must state the actual meaning of the field explicitly.
5. Fields whose meanings differ must not be forced into similar names in the name of consistency.
6. A newly created data structure must be understandable from its field names alone by a developer who did not take part in the implementation.
7. The naming conventions already used by the current project take precedence. If an existing name is unclear, the unclear name must not be copied into new code.
8. An existing field name must not be changed on the agent's own initiative. Where historical data, interface compatibility, or a database migration is involved, the impact must be analyzed and a proposal put forward first.

### 9.2 Scope

This section covers every identifier that carries meaning in a project:

- Variable names.
- Function and method names.
- Class and type names.
- JSON, YAML, and configuration keys.
- Database column names.
- File and directory names.
- Data structure fields.
- API parameter names.
- Branch and tag names.

It applies to newly created names and to names introduced by a migration, a refactor, or an interface change.

### 9.3 Relationship to Interface Contracts

The rules in section IX govern how a name is chosen. The rules about renaming an existing field, and about field consistency across modules, are specified in `interface-contract`. A name that satisfies section IX may still be forbidden to change, because the interface contract governs compatibility.

Rule 8 above states the prohibition itself. `interface-contract` section 8.1 states the analysis that must be produced before a rename is proposed.

### 9.4 Judgement Standard

Naming must prioritize semantic clarity over a smaller character count, faster typing, or a convention that merely looks like programmer habit.

A name passes this standard when a reader can state what it holds, what it counts, or what it represents without opening the file that declares it.

**Final requirement: an identifier is written for the developer who reads it later, not for the author who is typing it now.**

---

## X. Final Principle

It is acceptable to be concise, but not vague.

It is acceptable to be professional, but not obscure.

It is acceptable to be structured, but not at the cost of the completeness of natural language.

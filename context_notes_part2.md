# Context Notes (Part 2)

Read: Context Security, Context Isolation, Context Failure Modes.

## 3 ways context goes wrong

### 1. Poisoned
Wrong information gets into the context and the model treats it as true.
- **Defense:** verify the data before it goes into the context or memory. Use trusted sources only.

### 2. Distracted
There is too much unrelated content. It pulls the model's attention away from what matters.
- **Defense:** trim the context so only the relevant parts stay. In RAG, take only the top-k results.

### 3. Conflicting
Two or more sources say different things, and the model cannot decide which is right.
- **Defense:** choose which source to trust (the official or newest one) and tell the model which one wins.

## Other failure modes
- **Context rot:** accuracy drops as the context gets longer, even inside the model's limit.
- **Stale data:** information that was true before but is not true now.

## Context isolation
Each task gets its own separate context. Use several small agents, each with its own job and its own data. Unrelated information cannot interfere.

## Context security
- **Prompt injection:** hidden instructions inside text the model reads. The model may follow them.
- **Indirect prompt injection:** the hidden instructions come from outside data (websites, documents, emails).
- **Defenses:** least privilege (only the tools the agent needs), delimiters between instructions and data, validate data before saving to memory, separate memory per user and session.
- No single defense is perfect. Use several together.

Source: [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

# Rememoir

> *Not every memory deserves to be kept. But those that do — deserve to be understood.*

**Rememoir** is a local-first, human-centered cognitive memory system for offline AI agents.  
It enables your agent to remember, learn from feedback, and collaborate with you — without sending your data to the cloud.

Built for [UAssistant](https://github.com/erabytse/uassistant) and any local LLM agent.

- ✅ 100% offline
- ✅ Semantic + contextual recall
- ✅ Feedback-aware learning
- ✅ Open source (MIT)
- ✅ Part of the [Erabytse](https://erabytse.github.io/) ecosystem

---

## Quick Start

```python
from erabytse_rememoir import RememoirDB

# Initialize for a user
memory = RememoirDB(user_id="alice")

# Add a memory
memory.add("I prefer short answers in the evening.")

# Recall contextually
results = memory.search("How should you answer me at night?")
print(results[0].content)
# → "I prefer short answers in the evening."


```bash
   pip install erabytse-rememoir


Philosophy
Rememoir is not a database. It’s a memory companion — designed to forget what’s noise, keep what matters, and always stay under your control.

Part of Erabytse’s quiet rebellion against digital waste.

---

## 📜 2. `LICENSE` (MIT)

```text
MIT License

Copyright (c) 2026 Erabytse

Permission is hereby granted [...] (standard MIT text)
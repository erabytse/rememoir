# Rememoir

> *Not every memory deserves to be kept. But those that do — deserve to be understood.*

**Rememoir** is a local-first, human-centered cognitive memory system for offline AI agents.  
It enables your agent to remember conversations, learn from feedback, and collaborate with you — **without ever sending your data to the cloud**.

Built for [UAssistant](https://github.com/erabytse/uassistant) and any local LLM agent.

- ✅ 100% offline — no internet required  
- ✅ Semantic + contextual recall  
- ✅ Feedback-aware learning  
- ✅ Lightweight (uses [LanceDB](https://lancedb.com))  
- ✅ Open source (MIT License)  
- ✅ Part of the [Erabytse](https://erabytse.github.io/) ecosystem  

---

## Quick Start

```python
from erabytse_rememoir import RememoirDB

# Initialize memory for a user
memory = RememoirDB(user_id="alice")

# Add a memory
memory.add("I prefer short answers in German.")

# Recall contextually
results = memory.search("How should you answer me?")
print(results[0].content)
# → "I prefer short answers in German."


```bash
    pip install erabytse-rememoir

Philosophy
Rememoir is not a database. It’s a memory companion — designed to forget what’s noise, keep what matters, and always stay under your control.

In a world of surveillance and data extraction, Rememoir is a quiet act of digital care.

Part of Erabytse’s rebellion against digital waste.

Integration
See examples/integrate_with_uassistant.py for a full walkthrough with UAssistant.

License
MIT © Erabytse
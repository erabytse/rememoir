# Rememoir

> *Not every memory deserves to be kept. But those that do — deserve to be understood.*

**Rememoir** is a local-first, human-centered cognitive memory system for offline AI agents.  
It enables your agent to remember conversations, learn from feedback, and collaborate with you — **without ever sending your data to the cloud**.

Built for [UAssistant](https://github.com/erabytse/uassistant) and any local LLM agent.

- ✅ **100% offline** — no internet required  
- ✅ **Semantic + contextual recall** — finds relevant memories by meaning, not just keywords  
- ✅ **Feedback-aware learning** — adapts based on your corrections and preferences  
- ✅ **Lightweight & embeddable** — powered by [LanceDB](https://lancedb.com), zero external dependencies  
- ✅ **Open source (MIT License)** — inspect, modify, redistribute freely  
- ✅ **Part of the [Erabytse](https://erabytse.github.io/) ecosystem** — tools for intentional digital care  

---

# Quick Start

## Install:

```bash
pip install erabytse-rememoir
```

## Use in your agent:

```python
from erabytse_rememoir import RememoirDB

# Initialize memory for a user (isolated by user_id)
memory = RememoirDB(user_id="alice")

# Add a memory episode
memory.add("I prefer short answers in German.")

# Recall contextually
results = memory.search("How should you answer me?")
print(results[0].content)
# → "I prefer short answers in German."
```


## Philosophy

Rememoir is not a database. It’s a memory companion — designed to forget what’s noise, keep what matters, and always stay under your control.

In a world of surveillance, data extraction, and opaque AI, Rememoir offers a quiet alternative:
an intelligent memory that belongs to you, learns from you, and never betrays you.

It embodies Erabytse’s core principle:

Technology should serve attention, not exploit it.



## Integration

See examples/integrate_with_uassistant.py for a full walkthrough with UAssistant.

Rememoir works seamlessly with:

- Local LLMs (Ollama, LM Studio, llama.cpp…)
- RAG systems
- Voice or text-based agents
- Personal productivity tools

## License

MIT © [Erabytse](https://erabytse.github.io/) 
Part of a quiet rebellion against digital waste.
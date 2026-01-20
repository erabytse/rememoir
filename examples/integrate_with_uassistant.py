"""
Exemple d'intégration de Rememoir dans UAssistant (ou tout agent IA local).

Ce script montre comment :
- Initialiser la mémoire cognitive
- Sauvegarder une interaction
- Récupérer du contexte personnel avant de répondre
###
Example of integrating Rememoir into UAssistant (or any local AI agent).

This script shows how to:
- Initialize cognitive memory
- Save an interaction
- Retrieve personal context before responding
###
Beispiel für die Integration von Rememoir in UAssistant (oder einen beliebigen lokalen KI-Agenten).

Dieses Skript zeigt, wie man:
- den kognitiven Speicher initialisiert
- eine Interaktion speichert
- vor der Antwort den persönlichen Kontext abruft
"""

from erabytse_rememoir import RememoirDB

def main():
    # 1. Initialisation (un utilisateur = une mémoire isolée)
    memory = RememoirDB(user_id="user_123")

    # 2. L'utilisateur parle
    user_input = "Merke dir: Ich bevorzuge Antworten auf Deutsch und kurz."

    # 3. Sauvegarde l'entrée utilisateur
    memory.add(
        content=user_input,
        content_type="conversation",
        source="user"
    )

    # 4. Plus tard : rappel contextuel
    query = "Wie solltest du antworten?"
    relevant_memories = memory.search(query, k=2)

    print("🔍 Contexte trouvé :")
    for mem in relevant_memories:
        print(f" - {mem.content}")

    # 5. Simule une réponse de l'agent
    agent_response = "Verstanden! Ich antworte ab jetzt kurz auf Deutsch."
    memory.add(
        content=agent_response,
        content_type="conversation",
        source="agent"
    )

    print("\n✅ Interaction sauvegardée. La prochaine fois, l'agent se souviendra.")

if __name__ == "__main__":
    main()
import uuid
from uuid_extensions import uuid7, uuid7str
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
import lancedb

# -------------------------------
# 1. Modèle de données
# -------------------------------

class MemoryEpisode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    agent_id: str = "default_agent"
    content: str
    content_type: str  # "conversation", "feedback", etc.
    embedding: List[float] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    source: str  # "user" or "agent"
    context_tags: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    version: int = 1
    parent_id: Optional[str] = None
    is_active: bool = True

# -------------------------------
# 2. Moteur d'embeddings
# -------------------------------

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> List[float]:
        return self.model.encode(text, convert_to_numpy=False).tolist()

# -------------------------------
# 3. Base de données Memora
# -------------------------------

class MemoraDB:
    def __init__(self, db_path="./memora_db"):
        self.db = lancedb.connect(db_path)
        self.embedder = Embedder()
        self.table_name = "episodes"
        # Crée ou récupère la table
        if self.table_name not in self.db.list_tables():
            # Schéma minimal pour LanceDB (embedding obligatoire)
            import pyarrow as pa
            schema = pa.schema([
                ("id", pa.string()),
                ("user_id", pa.string()),
                ("agent_id", pa.string()),
                ("content", pa.string()),
                ("content_type", pa.string()),
                ("embedding", pa.list_(pa.float32(), 384)),
                ("timestamp", pa.string()),
                ("source", pa.string()),
                ("context_tags", pa.list_(pa.string())),
                ("confidence", pa.float32()),
                ("version", pa.int32()),
                ("parent_id", pa.string()),
                ("is_active", pa.bool_()),
            ])
            self.table = self.db.create_table(self.table_name, schema=schema, mode="overwrite")
        else:
            self.table = self.db.open_table(self.table_name)

    def add_memory(self, episode: MemoryEpisode):
        # Génère l'embedding si absent
        if not episode.embedding:
            episode.embedding = self.embedder.encode(episode.content)
        # Ajoute à la base
        self.table.add([episode.model_dump()])

    def search(
        self,
        query: str,
        user_id: str,
        k: int = 5,
        content_types: Optional[List[str]] = None,
        context_tags: Optional[List[str]] = None,
    ):
        query_emb = self.embedder.encode(query)
        results = (
            self.table.search(query_emb, vector_column_name="embedding")
            .where(f"user_id = '{user_id}' AND is_active = true", prefilter=True)
            .limit(k * 3)  # On prend plus pour filtrer après
            .to_pydantic(MemoryEpisode)
        )

        # Filtres supplémentaires en mémoire (LanceDB ne gère pas encore bien les listes dans WHERE)
        filtered = []
        for r in results:
            if content_types and r.content_type not in content_types:
                continue
            if context_tags and not set(context_tags).issubset(set(r.context_tags)):
                continue
            filtered.append(r)
            if len(filtered) >= k:
                break
        return filtered[:k]

# -------------------------------
# 4. Exemple d'utilisation
# -------------------------------

if __name__ == "__main__":
    db = MemoraDB()

    user = "alice_42"

    # Étape 1 : L'agent répond à une question
    question = MemoryEpisode(
        user_id=user,
        content="Comment créer une base de données pour une IA ?",
        content_type="conversation",
        source="user",
        context_tags=["learning", "ai", "database"]
    )
    db.add_memory(question)

    reponse = MemoryEpisode(
        user_id=user,
        content="Utilise une base vectorielle comme LanceDB, avec embeddings et métadonnées.",
        content_type="conversation",
        source="agent",
        parent_id=question.id,
        context_tags=["ai", "database", "vector"]
    )
    db.add_memory(reponse)

    # Étape 2 : L'utilisateur donne un feedback
    feedback = MemoryEpisode(
        user_id=user,
        content="Trop technique, donne un exemple simple.",
        content_type="feedback",
        source="user",
        parent_id=reponse.id,
        confidence=0.6,
        context_tags=["learning", "confusion"]
    )
    db.add_memory(feedback)

    # Étape 3 : Recherche sémantique
    print("\n🔍 Recherche : 'base de données simple pour IA'")
    results = db.search(
        query="base de données simple pour IA",
        user_id=user,
        k=3,
        context_tags=["learning"]
    )
    for r in results:
        print(f"- [{r.source}] {r.content} (type: {r.content_type})")
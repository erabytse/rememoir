import lancedb
from .models import MemoryEpisode
from .embedder import Embedder
from typing import List, Optional

class RememoirDB:
    def __init__(self, user_id: str, db_path: str = "./rememoir_db"):
        self.user_id = user_id
        self.db = lancedb.connect(db_path)
        self.embedder = Embedder()
        self.table_name = "memories"
        if self.table_name not in self.db.table_names():
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
            self.table = self.db.create_table(self.table_name, schema=schema)
        else:
            self.table = self.db.open_table(self.table_name)

    def add(self, content: str, **kwargs):
        episode = MemoryEpisode(
            user_id=self.user_id,
            content=content,
            **kwargs
        )
        if not episode.embedding:
            episode.embedding = self.embedder.encode(episode.content)
        self.table.add([episode.model_dump()])

    def search(
        self,
        query: str,
        k: int = 3,
        content_types: Optional[List[str]] = None,
        context_tags: Optional[List[str]] = None,
    ) -> List[MemoryEpisode]:
        query_emb = self.embedder.encode(query)
        results = (
            self.table.search(query_emb, vector_column_name="embedding")
            .where(f"user_id = '{self.user_id}' AND is_active = true", prefilter=True)
            .limit(k * 3)
            .to_pydantic(MemoryEpisode)
        )
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
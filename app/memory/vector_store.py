import chromadb
from sentence_transformers import SentenceTransformer

# Embed Model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

#Persistent Chroma Client
client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(name="trip_memory")

class VectorStore:
    @staticmethod
    async def save_trip_context(user_id: str, context: str):
        embedding = embedding_model.encode(context).tolist()
        collection.add(
            documents=[context],
            embeddings=[embedding],
            ids=[f"{user_id}_{hash(context)}"],
            metadatas=[{"user_id": user_id}]
        )

    @staticmethod
    async def search_trip_context(user_id: str, query: str, limit: int = 5):
        query_embedding = embedding_model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={"user_id": user_id}
        )

        return results
    
    @staticmethod
    async def clear_user_context(user_id: str):
        results = collection.get(
            where={"user_id": user_id}
        )
        if results["ids"]:
            collection.delete(ids=results["ids"])

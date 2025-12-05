from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.case import Case


embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def generate_embedding(text: str) -> list:
    """Converts text into a list of floats (vector)."""
    return embed_model.embed_query(text)

def search_similar_cases(db: Session, query_text: str, limit: int = 3):
    """Finds the top 3 most relevant past cases."""
    try:
        query_vector = generate_embedding(query_text)
        stmt = select(Case).filter(
            Case.status == "closed",
            Case.embedding.is_not(None)
        ).order_by(
            Case.embedding.l2_distance(query_vector)
        ).limit(limit)
        
        results = db.execute(stmt).scalars().all()
        return results
    except Exception as e:
        print(f"Memory Search Failed: {e}")
        return []

def store_case_memory(db: Session, case_id: int, text_to_embed: str):
    """Updates a case with its vector embedding for future recall."""
    try:
        vector = generate_embedding(text_to_embed)
        case = db.get(Case, case_id)
        if case:
            case.embedding = vector
            db.commit()
            print(f"Memory stored for Case #{case_id}")
    except Exception as e:
        print(f"Failed to store memory: {e}")
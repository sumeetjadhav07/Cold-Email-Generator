import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path=r"C:\Users\jadha\OneDrive\Desktop\Cold Email Generator\project-genai-cold-email-generator\app\resource\my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # persistent vector DB
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:   # only load if empty
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        result = self.collection.query(query_texts=skills, n_results=2)
        return result["metadatas"]

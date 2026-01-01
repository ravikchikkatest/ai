import os
import pandas as pd
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbeddings


load_dotenv('C:/Agentic/codellm/.env')
GOOGLE_API_KEY = os.getenv("GOOGLEAI_API_KEY")


Settings.llm = Gemini(model_name="models/gemini-2.5-flash", api_key=GOOGLE_API_KEY)
Settings.embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")


csv_path = 'sample_data.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"The file {csv_path} does not exist.")


print("Loading documents...")

df = pd.read_csv(csv_path)
documents = []

for _, row in df.iterrows():
    # Convert each row into a readable text block for the LLM
    # This dynamic method works for ANY csv columns
    text_content = ", ".join([f"{col}: {val}" for col, val in row.items()])  #[orderid:3245, date:2023-01-01,...]
    documents.append(Document(text=text_content))

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=5)


# --- 5. Simple Query Loop ---
print("\n--- Sales Data RAG Ready ---")
print("Ask questions like 'What was the total sales for Laptops?' or 'exit' to quit.\n")

while True:
    user_input = input("Query: ").strip()
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    if not user_input:
        continue

    try:
        # The query engine retrieves context and generates an answer
        response = query_engine.query(user_input)
        print(f"\nAnswer: {response}\n")
    except Exception as e:
        print(f"Error: {e}")
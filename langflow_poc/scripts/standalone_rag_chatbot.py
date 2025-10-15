"""
Standalone Customer Support RAG Chatbot
This version doesn't require LangFlow to be running - it implements RAG directly using LangChain
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader

load_dotenv()


class CustomerSupportChatbot:
    """Standalone RAG chatbot for customer support"""
    
    def __init__(self, knowledge_base_path: str):
        """
        Initialize the chatbot
        
        Args:
            knowledge_base_path: Path to the knowledge base text file
        """
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.knowledge_base_path = knowledge_base_path
        self.vectorstore = None
        self.qa_chain = None
        self._setup_rag()
    
    def _setup_rag(self):
        """Set up the RAG pipeline"""
        print("Setting up RAG pipeline...")
        
        # Load documents
        print("Loading knowledge base...")
        loader = TextLoader(self.knowledge_base_path)
        documents = loader.load()
        
        # Split documents into chunks
        print("Splitting documents...")
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        print(f"Created {len(texts)} text chunks")
        
        # Create embeddings
        print("Creating embeddings...")
        embeddings = OpenAIEmbeddings()
        
        # Create vector store
        print("Building vector store...")
        self.vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            collection_name="customer_support",
            persist_directory="./chroma_db"
        )
        
        # Create LLM
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Create prompt template
        template = """You are a helpful customer support assistant for ACME Corp. 
Use the following context from our knowledge base to answer the customer's question. 
If you don't know the answer based on the context, politely say so and suggest contacting support.

Context:
{context}

Customer Question: {question}

Helpful Answer:"""
        
        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        print("RAG pipeline ready!\n")
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the chatbot
        
        Args:
            question: User question
            
        Returns:
            Answer from the chatbot
        """
        result = self.qa_chain.invoke({"query": question})
        return result["result"]
    
    def run_interactive(self):
        """Run the chatbot in interactive mode"""
        print("=" * 60)
        print("ACME Corp Customer Support Chatbot (Standalone Mode)")
        print("=" * 60)
        print("Ask me anything about our products and services!")
        print("Type 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\nThank you for contacting ACME Corp! Have a great day!")
                    break
                
                print("Bot: ", end="", flush=True)
                answer = self.ask(user_input)
                print(answer)
                print()
                
            except KeyboardInterrupt:
                print("\n\nThank you for contacting ACME Corp! Have a great day!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type 'quit' to exit.\n")
    
    def test(self):
        """Test the chatbot with predefined questions"""
        test_questions = [
            "What is the price of SmartWidget Pro?",
            "How do I reset my device?",
            "What is your return policy?",
            "How long does shipping take?",
            "My device won't connect to WiFi, what should I do?",
        ]
        
        print("=" * 60)
        print("Testing Customer Support Chatbot")
        print("=" * 60 + "\n")
        
        for i, question in enumerate(test_questions, 1):
            print(f"Test {i}/{len(test_questions)}")
            print(f"Question: {question}")
            
            try:
                answer = self.ask(question)
                print(f"Answer: {answer}")
            except Exception as e:
                print(f"Error: {e}")
            
            print("-" * 60 + "\n")


def main():
    """Main function"""
    import sys
    
    knowledge_base_path = "../data/knowledge_base.txt"
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if not os.path.exists(knowledge_base_path):
        print(f"Error: Knowledge base not found at {knowledge_base_path}")
        sys.exit(1)
    
    # Initialize chatbot
    try:
        chatbot = CustomerSupportChatbot(knowledge_base_path)
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)
    
    # Run in test mode or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        chatbot.test()
    else:
        chatbot.run_interactive()


if __name__ == "__main__":
    main()

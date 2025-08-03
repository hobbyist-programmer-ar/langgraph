# search_processor.py

import argparse
import json
from typing import Dict, List, Set, Tuple

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS

from rag.data_embedding.document_persistance import VectorStoreManager


class SearchProcessor:
    """
    Handles searching and retrieving information from a pre-built FAISS vector store.
    This class is responsible for the 'retrieval' part of the pipeline.
    """

    def __init__(self, vector_store: FAISS):
        """
        Initializes the SearchProcessor with a loaded vector store.

        Args:
            vector_store (FAISS): An initialized FAISS vector store instance.
        """
        if not isinstance(vector_store, FAISS):
            raise TypeError("vector_store must be an instance of langchain_community.vectorstores.FAISS")
        self.vector_store = vector_store

    def query_vector_store(self, query: str, k: int = 4) -> List[Document]:
        """
        Performs a similarity search on the vector store to find relevant chunks.
        """
        return self.vector_store.similarity_search(query, k=k)

    def retrieve_and_reconstruct_sections(self, query: str, k: int = 4) -> Dict[str, Dict]:
        """
        Retrieves relevant documents and reconstructs their full sections.

        Args:
            query (str): The question or text to search for.
            k (int): The number of top initial chunks to retrieve.

        Returns:
            A dictionary where each key is a unique section identifier and the value
            is a dictionary containing the reconstructed content and metadata.
        """
        relevant_chunks = self.query_vector_store(query, k=k)
        if not relevant_chunks:
            return {}

        unique_section_keys: Set[Tuple[str, str]] = set()
        for chunk in relevant_chunks:
            key = (chunk.metadata['file_name'], chunk.metadata['section_name'])
            unique_section_keys.add(key)

        reconstructed_sections = {}
        all_docs = self.vector_store.docstore._dict.values()

        for file_name, section_name in unique_section_keys:
            section_chunks = [
                doc for doc in all_docs
                if doc.metadata['file_name'] == file_name and doc.metadata['section_name'] == section_name
            ]
            section_chunks.sort(key=lambda x: x.metadata.get('chunk_index', 0))

            full_content = " ".join([doc.page_content for doc in section_chunks])
            representative_metadata = section_chunks[0].metadata

            section_id = f"{file_name} - {section_name}"
            reconstructed_sections[section_id] = {
                "content": full_content,
                "metadata": representative_metadata
            }

        return reconstructed_sections

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Query a pre-built FAISS vector store.")
    parser.add_argument('--index_path', type=str, required=True, help="Path to the saved FAISS index folder.")
    parser.add_argument('--k', type=int, help="Number of top results to retrieve.", default=8)
    args = parser.parse_args()

    try:
        # 1. Load the pre-built vector store
        print(f"Loading vector store from: {args.index_path}")
        vector_store = VectorStoreManager.load_local(args.index_path)

        # 2. Instantiate the search processor
        searcher = SearchProcessor(vector_store)
        print("--- Search Processor Ready ---")

        # 3. Start interactive query loop
        print("You can now ask questions about the documents. Type 'exit' to quit.")
        while True:
            try:
                user_query = input("Query> ")
                if user_query.lower() == 'exit':
                    break
                if not user_query:
                    continue

                results = searcher.retrieve_and_reconstruct_sections(user_query, k=args.k)

                print("\n--- Reconstructed Sections ---")
                if not results:
                    print("No relevant sections found.")
                else:
                    print(json.dumps(results, indent=2))
                print("\n" + "-" * 20)

            except KeyboardInterrupt:
                print("\nExiting query loop.")
                break

    except (FileNotFoundError, TypeError) as e:
        print(f"\nAn error occurred: {e}")
        print(f"Please ensure '{args.index_path}' is a valid FAISS index folder created by document_persistance.py.")

# Created by Satish Bomma Nov23 24 qdrant_app/search_ui.py
import streamlit as st
from qdrant_client import QdrantClient
import yaml

class CloroxHybridSearch:
    DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    SPARSE_MODEL = "prithivida/Splade_PP_en_v1"

    def __init__(self, collection_name, config_path):
        self.collection_name = collection_name

        # Load configuration from file
        config = self.read_from_file(config_path)
        print("Configuration loaded:", config)

        # Retrieve Qdrant endpoint and API key from configuration
        qdrant_url = config.get('qdrant_endpoint')
        qdrant_api = config.get('api_key')

        if not qdrant_url or not qdrant_api:
            raise ValueError("Qdrant endpoint or API key is missing in the configuration.")

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api)

        # Set dense and sparse models
        self.qdrant_client.set_model(self.DENSE_MODEL)
        self.qdrant_client.set_sparse_model(self.SPARSE_MODEL)
        print(f"Initialized Qdrant client with models: Dense={self.DENSE_MODEL}, Sparse={self.SPARSE_MODEL}")

    @staticmethod
    def read_from_file(config_path):
        """Reads configuration from a YAML file."""
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Error loading configuration file: {e}")

   #use documentation to drive: this.
    def search(self, text: str):

        try:
            # Perform the search query
            search_result = self.qdrant_client.query(
                collection_name=self.collection_name,
                query_text=text,
                query_filter=None,  # If no filters are applied
                limit=5,  # Limit to the top 5 closest results
            )
            print(f"Search results for '{text}':", search_result)

            # Extract and return metadata from search results
            metadata = [hit.metadata for hit in search_result]
            return metadata

        except Exception as e:
            print(f"Error during search: {e}")
            raise


# Streamlit UI
def start_ui():
    st.title("Clorox Qdrant Search UI")
    st.write("Search the Clorox knowledge base using natural language queries.")

    # Path to the configuration file
    config_file = "//config.yml"

    # Initialize the CloroxHybridSearch instance
    collection_name = "clorox_version2"
    search_instance = CloroxHybridSearch(collection_name=collection_name, config_path=config_file)

    # Search bar
    query_text = st.text_input("Enter your search query:", "")

    if st.button("Search"):
        if query_text.strip():
            st.write(f"Searching for: **{query_text}**")
            try:
                # Perform the search
                results = search_instance.search(query_text)

                # Display results
                if results:
                    st.success(f"Found {len(results)} results.")
                    for i, result in enumerate(results):
                        st.subheader(f"Result {i + 1}")
                        for key, value in result.items():
                            st.write(f"**{key.capitalize()}**: {value}")
                else:
                    st.warning("No results found.")
            except Exception as e:
                st.error(f"An error occurred while searching: {e}")
        else:
            st.warning("Please enter a valid search query.")

if __name__ == "__main__":
    start_ui()

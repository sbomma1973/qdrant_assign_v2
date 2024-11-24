#created by Satish Bomma Nov23 24

import yaml
from qdrant_client import QdrantClient
#from qdrant_client.models import VectorParams, Distance

# Read `config.yml` file for all the config data
def read_from_file(config_path='config.yml'):
    try:
        with open(config_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        raise


# Test connection to Qdrant
def test_connect(qc):
    try:
        collections = qc.get_collections()
        print("Connected to Qdrant cloud successfully!")
        print("Available collections:", collections)
    except Exception as e:
        print(f"Failed to connect: {e}")
        raise


# Create a new collection in Qdrant - With Sparse (Splade) as well as Dense vectors
def create_collection(qc, colname): # dims, dist):
    try:
        qc.create_collection(
            collection_name=colname,
            vectors_config=qc.get_fastembed_vector_params(),
            sparse_vectors_config=qc.get_fastembed_sparse_vector_params(),
        )
        print(f"Collection '{colname}' created successfully!")
    except Exception as e:
        print(f"Failed to create collection '{colname}': {e}")
        raise


# Delete a collection in Qdrant
def delete_collection(client, colname):
    try:
        client.delete_collection(
            collection_name=colname
        )
        print(f"Collection '{colname}' deleted successfully!")
    except Exception as e:
        print(f"Failed to delete collection '{colname}': {e}")
        raise


def main():
    # Load configuration

    config = read_from_file()
    print("Configuration loaded:", config)

    # Retrieve Qdrant endpoint and API key
    qdrant_url = config.get('qdrant_endpoint')
    qdrant_api = config.get('api_key')

    if not qdrant_url or not qdrant_api:
        print("Qdrant endpoint or API key is missing in the configuration.")
        return

    # Initialize Qdrant client
    qc = QdrantClient(url=qdrant_url, api_key=qdrant_api)

    # Test connection
    test_connect(qc)

    # Example: Create a collection
    qc.set_model("sentence-transformers/all-MiniLM-L6-v2")
    qc.set_sparse_model("prithivida/Splade_PP_en_v1")

    collection_name = "colroxv4"

    # Delete the collection if it already exists, then create a new one
    #delete_collection(qc, collection_name)
    create_collection(qc, collection_name)# vector_dimensions, distance_metric)



if __name__ == '__main__':
    main()

This `README.md` provides an overview of the script, instructions for installation, and descriptions of each function and its purpose.

# Number 1: Hybrid Data Ingestion (with splade and dense model(cosine distance)) for Clorox Learn Articles

## Overview

This script is designed to crawl and ingest data from the "Learn" section of the Clorox website (`https://www.clorox.com/learn/`). It extracts articles, saves them in JSON format, and then ingests them into a Qdrant vector database. The main purpose of this script is to collect article data (title, body text, and URL) and add the content to Qdrant for further processing, such as search or analysis.

## Features

- Crawls the Clorox Learn website to collect articles.
- Extracts the title, body, and URL from each article.
- Saves each article in a structured JSON file.
- Ingests the extracted data into a Qdrant collection for storage and later use.
- This uses a hybrid approach described in qdrant's documenation (https://qdrant.tech/documentation/beginner-tutorials/hybrid-search-fastembed/)
- Supports dynamic URL handling and relative path resolution.
- Handles connection to the Qdrant cloud and integrates with the Qdrant client to store documents.

## Requirements

Before running the script, ensure that the following libraries are installed:

- `requests`: For sending HTTP requests to fetch the article pages.
- `beautifulsoup4`: For parsing HTML content and extracting data.
- `qdrant-client`: For interacting with the Qdrant vector database.
- `tqdm`: For displaying progress bars during the crawling and ingestion processes.
- `pyyaml`: For reading configuration files.

You can install the required packages via pip:

```bash
pip install requests beautifulsoup4 qdrant-client tqdm pyyaml
```
Configuration
This script uses a configuration file (assumed to be read via the read_from_file() function in the createCollection.py module). The configuration should contain the following details:

qdrant_endpoint: The URL of the Qdrant instance.
api_key: The API key for authenticating with the Qdrant instance.
Example configuration (config.yaml):

qdrant_endpoint: "https://your-qdrant-endpoint"
api_key: "your-api-key"
How It Works
1. Crawling and Saving Articles
The script starts by crawling the Clorox Learn website from the URL https://www.clorox.com/learn/. It visits a specified number of pages (default: 200) and extracts the following data from each article page:

Title: The title of the article.
Body: The main content (body) of the article.
URL: The URL of the article.
Each article is saved as a JSON file in the clorox_learn_articles directory. If a page has links to other articles within the "Learn" section, those are added to the crawl queue.

2. Data Ingestion into Qdrant
After the articles are saved, the script reads the saved JSON files, extracts the title and body from each article, and combines them into a single string. This combined text is then ingested into a Qdrant collection for indexing.

3. Connection to Qdrant
The script connects to the Qdrant instance using the provided API endpoint and key. It tests the connection and then proceeds with ingesting the data into a collection named clorox_version5.

Functions
extract_title_and_body(url)
This function takes a URL, fetches the page content, and extracts the title and body text.

Arguments:

url (str): The URL of the article.
Returns:

A dictionary containing the url, title, and body of the article.
crawl_and_save_learn_pages(start_url, num_pages)
This function starts crawling from the given start_url and extracts articles from the Clorox Learn section. It saves the data into JSON files in the clorox_learn_articles directory.

Arguments:

start_url (str): The starting URL for crawling.
num_pages (int): The number of pages to crawl.
ingest_data(output_dir)
This function loads the saved JSON files from the output_dir, extracts the title and body, and prepares the data for ingestion into Qdrant.

Arguments:

output_dir (str): The directory where the JSON files are saved.
Returns:

metadata (list): A list of dictionaries containing metadata for each article.
documents (list): A list of combined text (title + body) for each article.
add_to_collection(client, metadata, documents)
This function adds the extracted data (documents and metadata) to the specified Qdrant collection.

Arguments:

client (QdrantClient): The Qdrant client instance.
metadata (list): The list of metadata dictionaries.
documents (list): The list of document texts.
test_connect(client)
This function tests the connection to the Qdrant instance by attempting to fetch available collections.

Arguments:

client (QdrantClient): The Qdrant client instance.
main()
The main function that coordinates the execution of the entire process:

Loads the configuration.
Initializes the Qdrant client.
Tests the connection to Qdrant.
Crawls the Clorox Learn pages.
Ingests the extracted data into Qdrant.
How to Run
Configure the Qdrant endpoint and API key in a config.yaml file.
Run the script with the following command:

python dataingstion.py

# Number 2Clorox Qdrant Search UI

## Overview

This script provides a Streamlit-based user interface to interact with a Qdrant-based search system for the Clorox knowledge base. It allows users to perform natural language searches and retrieve relevant documents stored in the Qdrant vector database.

The search is powered by hybrid models: a dense model (`sentence-transformers/all-MiniLM-L6-v2`) and a sparse model (`prithivida/Splade_PP_en_v1`), which are used to compute and rank the relevance of documents based on the search query.

## Features

- Simple Streamlit-based user interface for search.
- Allows natural language text-based queries.
- Queries the Qdrant vector database using a hybrid search approach (dense and sparse models).
- Displays the metadata of the top search results.
- Configurable Qdrant connection using a YAML configuration file.

## Requirements

Before running the script, ensure that the following libraries are installed:

- `streamlit`: For building the web UI.
- `qdrant-client`: For interacting with the Qdrant vector database.
- `pyyaml`: For reading the configuration file.

You can install the required packages via pip:

```bash
pip install streamlit qdrant-client pyyaml
```

Configuration
The script requires a configuration file (config.yml) that contains the Qdrant endpoint URL and API key. This configuration is used to initialize the connection to the Qdrant database.

Example configuration (config.yml):

qdrant_endpoint: "https://your-qdrant-endpoint"
api_key: "your-api-key"
The configuration file should be located at the path specified in the config_file variable in the script.

How It Works
1. Initialization of Qdrant Client
The script loads the configuration from the YAML file and initializes the Qdrant client using the provided API key and endpoint. It also sets up two models for hybrid search: a dense model for embeddings-based search and a sparse model for token-based search.

2. Performing Search
The user enters a search query into a text input field.
Upon pressing the "Search" button, the entered query is sent to Qdrant for processing.
The results are fetched based on the query's relevance, considering both dense and sparse models.
The top 5 results are displayed, showing the metadata of each result (such as title, body, and URL).
3. Streamlit Interface
The user interface consists of a simple text input field for the search query and a button to initiate the search. The results are displayed with headers and details for each hit returned by the search.

Functions
CloroxHybridSearch.__init__(self, collection_name, config_path)
The constructor initializes the CloroxHybridSearch object by loading the configuration from a specified YAML file and setting up the Qdrant client with the provided endpoint and API key. It also sets the dense and sparse models for search.

Arguments:

collection_name (str): The name of the Qdrant collection to query.
config_path (str): The path to the YAML configuration file.
CloroxHybridSearch.read_from_file(config_path)
This static method reads the configuration from a YAML file.

Arguments:

config_path (str): The path to the configuration file.
Returns:

A dictionary containing the configuration values (endpoint URL and API key).
CloroxHybridSearch.search(self, text: str)
This method performs the actual search query using the Qdrant client. It returns the metadata of the most relevant documents based on the provided search text.

Arguments:

text (str): The query text to search for.
Returns:

A list of metadata for the top search results.
start_ui()
This function sets up the Streamlit user interface. It allows the user to enter a search query and displays the results based on the search response from Qdrant.

How to Run
Configure your Qdrant endpoint and API key in the config.yml file.
Make sure you have installed all the required dependencies (streamlit, qdrant-client, and pyyaml).
Run the Streamlit app with the following command:
bash

streamlit run qdrant_app/search_ui.py
Navigate to the local Streamlit UI, typically hosted at http://localhost:8501, where you can enter your search query and view the results.
License
This project is licensed under the MIT License - see the LICENSE file for details.

s




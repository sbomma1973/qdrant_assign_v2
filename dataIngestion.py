#created by Satish Bomma Nov23 24
import os
import json
from importlib.metadata import metadata

import requests
from bs4 import BeautifulSoup
import time
import yaml
from qdrant_client import QdrantClient

from createCollection import read_from_file
from tqdm import tqdm


# Directory to store JSON files
output_dir = "clorox_learn_articles"
os.makedirs(output_dir, exist_ok=True)

# Function to extract title and body
def extract_title_and_body(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the title
    title = soup.title.string.strip() if soup.title else "No Title Found"

    # Extract the body text
    body = soup.body.get_text(separator="\n", strip=True) if soup.body else "No Body Found"

    return {"url": url, "title": title, "body": body}

# Function to crawl and save pages under /learn/ sub-URL
def crawl_and_save_learn_pages(start_url, num_pages):
    visited_urls = set()
    to_crawl = [start_url]  # Queue of URLs to visit
    saved_count = 0

    while saved_count < num_pages and to_crawl:
        url = to_crawl.pop(0)
        if url in visited_urls or not url.startswith("https://www.clorox.com/learn/"):
            continue

        try:
            print(f"Processing: {url}")
            data = extract_title_and_body(url)
            visited_urls.add(url)

            # Save to file
            file_name = os.path.join(output_dir, f"article_{saved_count + 1}.json")
            with open(file_name, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Saved: {file_name}")
            saved_count += 1

            # Find links to add to the queue
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                full_url = a_tag["href"]
                if full_url.startswith("/"):  # Handle relative URLs
                    full_url = "https://www.clorox.com" + full_url
                if full_url.startswith("https://www.clorox.com/learn/"):
                    to_crawl.append(full_url)

        except Exception as e:
            print(f"Error processing {url}: {e}")
        time.sleep(1)  # Be polite and avoid overwhelming the server


def ingest_data(output_dir):
    metadata = []
    documents = []

    # Iterate over files in the output directory
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)

        # Process only JSON files
        if file_name.endswith(".json"):
            with open(file_path, "r") as f:
                try:
                    # Load the entire file content as a single JSON object
                    data = json.load(f)

                    # Extract relevant fields
                    url = data.get("url", "")
                    title = data.get("title", "")
                    body = data.get("body", "")

                    # Combine title and body for embedding
                    combined_text = f"{title}\n{body}"

                    # Store metadata and combined text
                    metadata.append(data)
                    documents.append(combined_text)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_path}: {e}")

    return metadata, documents

def add_to_collection(client, metadata, documents):
        try:
            client.add(
                collection_name="clorox_version2",
                documents=documents,
                metadata=metadata,
                ids=tqdm(range(len(documents))),
            )
            print("Data successfully added to the collection 'test'.")
        except Exception as e:
            print(f"Failed to add data to the collection: {e}")
            raise

def test_connect(client):
    try:
        collections = client.get_collections()
        print("Connected to Qdrant cloud successfully!")
        print("Available collections:", collections)
    except Exception as e:
        print(f"Failed to connect: {e}")
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
        qc.set_model("sentence-transformers/all-MiniLM-L6-v2")
        qc.set_sparse_model("prithivida/Splade_PP_en_v1")

        #Start crawling and save the pages

        start_url = "https://www.clorox.com/learn/"
        num_pages = 200
        #crawl_and_save_learn_pages(start_url, num_pages)

        # Ingest data
        metadata, documents = ingest_data(output_dir)

        # Add data to the collection
        add_to_collection(qc, metadata, documents)

if __name__ == '__main__':
    main()

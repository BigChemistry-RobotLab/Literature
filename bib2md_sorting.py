import bibtexparser
import os
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

month = 'OCT'
year = '2024'

# Define the base directory where folders are stored
base_dir = r'C:\Users\Jhoux\OneDrive - Radboud Universiteit\Documenten\PhD\Coding\Literature'
data_dir = r'C:\Users\Jhoux\OneDrive - Radboud Universiteit\Documenten\PhD\Coding\Literature\Bibtex_files'

# Construct the folder name based on month and year
folder_name = f'{month}{year}'

# Construct the full path to the folder
folder_path = os.path.join(data_dir, folder_name)

# Check if the folder exists
if not os.path.exists(folder_path):
    raise FileNotFoundError(f"The folder for {month}{year} does not exist at {folder_path}")

print(f"Folder found: {folder_path}")

# Load the BibTeX file from the constructed folder path
bibtex_file_path = os.path.join(folder_path, 'Exported Items.bib')
with open(bibtex_file_path, encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# Print the number of entries in the BibTeX file
print(f"Number of entries in the BibTeX file: {len(bib_database.entries)}")

topics = {
    'Self-assembly': ['self-assembly', 'aggregation', 'micelles'],
    'Peptides': ['peptides', 'peptide design', 'amino acids', 'peptide synthesis', 'peptide'],
    'Peptide Amphiphiles': ['peptide amphiphiles', 'PA', 'amphiphile'],
    'Surfactants': ['surfactants', 'detergents', 'soaps'],
    'Biomaterials': ['biomaterials', 'materials', 'biodegradable'],
    'Polymers': ['polymers', 'polymerization', 'polymer'],
    'Lab automation': ['lab automation', 'robotics', 'high-throughput'],
    'Machine Learning': ['machine learning', 'deep learning', 'AI'],
    'Graph neural networks': ['graph neural networks', 'GNN', 'graph'],
    'Vapor pressure': ['vapor pressure', 'pressure', 'vapor'],
    # Add more topics and keywords as needed
}

# Initialize a dictionary to store sorted entries by topic
sorted_entries = defaultdict(list)

for entry in bib_database.entries:
    entry_text = entry.get('title', '') + " " + entry.get('abstract', '') + " " + entry.get('keywords', '')
    entry_text = entry_text.lower()
    
    # Check for keywords in each topic
    for topic, keywords in topics.items():
        if any(keyword in entry_text for keyword in keywords):
            sorted_entries[topic].append(entry)
            break  # Add only to the first matching topic (optional)

# Print or save sorted entries for review
for topic, entries in sorted_entries.items():
    print(f"\nTopic: {topic}")
    for entry in entries:
        print(f"Title: {entry.get('title')}")

# Function to create markdown content for each topic
def create_markdown_content(topic, entries):
    content = f"# Literature on {topic}\n\n"
    for entry in entries:
        # Extract relevant fields
        authors = entry["author"].replace(" and ", "; ")
        title = entry["title"]
        journal = entry["journal"]
        volume = entry.get("volume", "")
        number = entry.get("number", "")
        pages = entry.get("pages", "")
        year = entry["year"]
        publisher = entry.get("publisher", "")
        url = entry["url"]
        abstract = entry.get("abstract", "")

        # Extract the two most important keywords from the abstract
        abstract_keywords = extract_keywords(abstract, keywords, num_keywords=2)

        # Format the volume and number
        volume_number = f"**{volume}**" + (f"({number})" if number else "")

        # Construct the Markdown citation
        citation = f"[{title}]({url}). {authors}. *{journal}* {volume_number}, {pages}. {publisher}, {year}.\n*notes*\n  - Keywords: {', '.join(abstract_keywords)}\n* * * * * * * * * * *"
        content += citation + "\n\n"
    return content

def extract_keywords(text, topic_keywords, num_keywords=2):
    # Combine the topic keywords and the text
    combined_text = ' '.join(topic_keywords) + ' ' + text
    
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Fit and transform the combined text
    tfidf_matrix = vectorizer.fit_transform([combined_text, text])
    
    # Calculate cosine similarity between the topic keywords and the text
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Get the feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get the top N keywords based on TF-IDF scores
    sorted_indices = np.argsort(tfidf_matrix[1].toarray()[0])[::-1]
    top_keywords = [feature_names[i] for i in sorted_indices if feature_names[i] not in topic_keywords][:num_keywords]
    
    return top_keywords

# Create markdown files for each topic
for topic, entries in sorted_entries.items():
    markdown_content = create_markdown_content(topic, entries)
    markdown_file_path = os.path.join(base_dir, f"{topic.replace(' ', '_')}.md")
    with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_content)

print(f"Markdown files created in {base_dir}")

# Path for the table of contents markdown file
toc_file_path = os.path.join(base_dir, 'Table_of_Contents.md')

# Create the table of contents content
toc_content = "# Table of Contents\n\n"
for topic in sorted_entries.keys():
    topic_file_name = f"{topic.replace(' ', '_')}.md"
    toc_content += f"- [{topic}](./{topic_file_name})\n"

# Write the table of contents to the markdown file
with open(toc_file_path, 'w', encoding='utf-8') as toc_file:
    toc_file.write(toc_content)

print(f"Table of Contents created at {toc_file_path}")
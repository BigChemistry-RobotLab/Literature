import bibtexparser
import os
from collections import defaultdict

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
        title = entry.get('title', 'No title')
        author = entry.get('author', 'No author')
        journal = entry.get('journal', 'No journal')
        year = entry.get('year', 'No year')
        abstract = entry.get('abstract', 'No abstract')
        doi = entry.get('doi', 'No DOI')
        url = entry.get('url', 'No URL')
        keywords = entry.get('keywords', 'No keywords')
        
        content += f"## {title}\n"
        content += f"**Authors:** {author}\n\n"
        content += f"**Journal:** {journal} ({year})\n\n"
        #content += f"**Abstract:** {abstract}\n\n"
        #content += f"**Keywords:** {keywords}\n\n"
        content += f"**DOI:** [{doi}]({url})\n\n"
        content += "---\n\n"
    return content

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
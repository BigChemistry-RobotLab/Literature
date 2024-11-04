import bibtexparser
import pyperclip


def bibtex_to_markdown(bibtex_entry):
    # Parse the BibTeX entry
    bib_database = bibtexparser.loads(bibtex_entry)
    entry = bib_database.entries[0]

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

    # Format the volume and number
    volume_number = f"**{volume}**" + (f"({number})" if number else "")

    # Construct the Markdown citation
    citation = f"[{title}]({url}). {authors}. *{journal}* {volume_number}, {pages}. {publisher}, {year}.\n*notes*\n  -\n* * * * * * * * * * *"
    pyperclip.copy(citation)


# Example usage
bibtex_entry = """


@article{berry_measurement_2015,
	title = {Measurement of surface and interfacial tension using pendant drop tensiometry},
	volume = {454},
	issn = {0021-9797},
	url = {https://www.sciencedirect.com/science/article/pii/S002197971500466X},
	doi = {10.1016/j.jcis.2015.05.012},
	abstract = {Pendant drop tensiometry offers a simple and elegant solution to determining surface and interfacial tension – a central parameter in many colloidal systems including emulsions, foams and wetting phenomena. The technique involves the acquisition of a silhouette of an axisymmetric fluid droplet, and iterative fitting of the Young–Laplace equation that balances gravitational deformation of the drop with the restorative interfacial tension. Since the advent of high-quality digital cameras and desktop computers, this process has been automated with high speed and precision. However, despite its beguiling simplicity, there are complications and limitations that accompany pendant drop tensiometry connected with both Bond number (the balance between interfacial tension and gravitational forces) and drop volume. Here, we discuss the process involved with going from a captured experimental image to a fitted interfacial tension value, highlighting pertinent features and limitations along the way. We introduce a new parameter, the Worthington number, Wo, to characterise the measurement precision. A fully functional, open-source acquisition and fitting software is provided to enable the reader to test and develop the technique further.},
	urldate = {2024-09-30},
	journal = {Journal of Colloid and Interface Science},
	author = {Berry, Joseph D. and Neeson, Michael J. and Dagastine, Raymond R. and Chan, Derek Y. C. and Tabor, Rico F.},
	month = sep,
	year = {2015},
	keywords = {Interfacial tension, Surface tension, Bond number, Drop shape analysis, Pendant drop, Tensiometry},
	pages = {226--237},
	file = {ScienceDirect Snapshot:C\:\\Users\\pimda\\Zotero\\storage\\S7PK5ZYH\\S002197971500466X.html:text/html},
}


"""

# Convert and copy the md citation to clipboard
bibtex_to_markdown(bibtex_entry)

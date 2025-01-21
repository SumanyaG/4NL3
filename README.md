<h1>4NL3 Winter 2025 - Natural Language Processing</h1>

The following files are included in this repository:
- **myfile.txt**: UTF-8 encoded input file
- **normalize_text.py**: a python script to tokenize, normalize and visualize the data
- **Makefile**: Makefile to convert LaTeX code to as a PDF
- **homework1_report**: folder containing report-related files including the LaTeX file and the rendered PDF

The python script can be executed using the command: `$ python normalize_text.py myfile.txt (<your-options>)`. (<your-options>) can be replaced using any combination of the following options:
1. lowercasing as `--lowercase`
2. stemming as `--stem`
3. lemmatization as `--lemmatization`
4. removal of stopwords as `--remove-stopwords`
5. removal of numbers as `--remove-numbers`
import nltk
import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display

def tokenize_text(text):
    text = text[1:] if text.startswith('\ufeff') else text #Remove BOM characters appearing in text
    pattern = r"[A-Za-z]+(?:[''][A-Za-z]+)*|\d+|[A-Za-z]+|[^\w\s]"
    tokens = re.findall(pattern, text)
    tokens = [token for token in tokens if any(c.isalnum() for c in token)]

    return tokens

def normalize_tokens(tokens, lowercase=False, stem=False, lemmatize=False, remove_stopwords=False, remove_numbers=False):
    processed_tokens = tokens[:]

    if lowercase:
        processed_tokens = [token.lower() for token in processed_tokens]
    
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        processed_tokens = [token for token in tokens if token.lower() not in stop_words]
    
    if stem:
        stemmer = PorterStemmer()
        processed_tokens = [stemmer.stem(token) for token in tokens]
    
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        processed_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    if remove_numbers:
        processed_tokens = [token for token in processed_tokens if not re.match(r'^\d+$', token)]
    
    return processed_tokens

def count_tokens(tokens):
    counts = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

def visualize(word_counts, output_file='token_distribution.png'):
    df = pd.DataFrame(list(word_counts.items()), columns=['Tokens', 'Count'])
    df['Rank'] = range(1, len(df) + 1)

    display(df)

    plt.figure(figsize=(12,6))
    ax = df.head(25).plot(kind='bar', x='Tokens', y='Count', legend=False, ax=plt.gca())
    #plt.loglog(df['Rank'], df['Count'])
    plt.title('Token Frequency Distribution')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)

    plt.tight_layout()

    ax.set_yscale('log')
    plt.grid(True)
    #plt.savefig(output_file)
    #plt.close()
    plt.show()

def parse_args():
    args = {
        'input_file': None,
        'lowercase': False,
        'stem': False,
        'lemmatize': False,
        'remove_stopwords': False,
        'remove_numbers': False
    }

    if len(sys.argv) < 2:
        print("To use, type: python normalization.py myfile.txt [--lowercase] [--stem] [--lemmatize] [--remove-stopwords] [--remove-numbers]")
        sys.exit(1)
    
    args['input_file'] = sys.argv[1]

    flags = sys.argv[2:] if len(sys.argv) > 2 else []
    args['lowercase'] = '--lowercase' in flags
    args['stem'] = '--stem' in flags
    args['lemmatize'] = '--lemmatize' in flags
    args['remove_stopwords'] = '--remove-stopwords' in flags
    args['remove_numbers'] = '--remove-numbers' in flags

    return args

def main():
    args = parse_args()

    try:
        with open(args['input_file'], 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file {args['input_file']}")
        sys.exit(1)
    
    tokens = tokenize_text(text)
    print(f"\nAfter tokenization: ")
    print(f"Total tokens: {len(tokens)}")

    normalized = normalize_tokens(
        tokens,
        lowercase=args['lowercase'],
        stem=args['stem'],
        lemmatize=args['lemmatize'],
        remove_stopwords=args['remove_stopwords'],
        remove_numbers=args['remove_numbers']
    )

    sorted_counts = count_tokens(normalized)

    print(f"\nAfter normalization: ")
    print(f"Total tokens: {len(normalized)}")
    print(f"Unique tokens: {len(sorted_counts)}")
    print("\nTokens:")
    for word, count in list(sorted_counts.items())[-150:-100]:
        print(f"{word}: {count}")

    visualize(sorted_counts)

if __name__ == "__main__":
    main()
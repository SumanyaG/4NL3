import argparse
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

def tokenize_text(text):
    text = text[1:] if text.startswith('\ufeff') else text #Remove BOM characters appearing in text
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if any(c.isalnum() for c in token)]

    return tokens

def normalize_tokens(tokens, lowercase=False, stem=False, lemmatize=False, remove_stopwords=False):
    processed_tokens = tokens

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
    
    return processed_tokens

def main():
    parser = argparse.ArgumentParser(description='Normalize text and count tokens')
    parser.add_argument('input_file', help='Input text file')
    parser.add_argument('--lowercase', action='store_true', help='Covert text to lowercase')
    parser.add_argument('--stem', action='store_true', help='Apply stemming')
    parser.add_argument('--lemmatize', action='store_true', help='Apply lemmatization')
    parser.add_argument('--remove-stopwords', action='store_true', help='Remove stopwords')

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    tokens = tokenize_text(text)
    normalized = normalize_tokens(tokens, lowercase=args.lowercase, stem=args.stem, lemmatize=args.lemmatize, remove_stopwords=args.remove_stopwords)

    word_counts = Counter(normalized)

    sorted_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))

    print(f"\nFinal Results: ")
    print(f"Total tokens: {len(normalized)}")
    print(f"Unique tokens: {len(sorted_counts)}")
    print("\nTop 50 tokens:")
    for word, count in list(sorted_counts.items())[:50]:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
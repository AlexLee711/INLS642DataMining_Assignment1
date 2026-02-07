import re
import math
from collections import Counter
import json

def calculate_chi_square(reviews, labels):
    # labels: list of 1 (positive) and 0 (negative)
    N = len(reviews)
    num_pos = sum(labels)
    num_neg = N - num_pos

    # 1. Count occurrences in positive and negative reviews
    word_pos_counts = Counter()
    word_neg_counts = Counter()
    all_vocab = set()

    for i in range(N):
        # Preprocessing: Remove punctuation and lowercase (Slide 4)
        words = set(re.sub(r'[^\w\s]', '', reviews[i].lower()).split())
        all_vocab.update(words)
        if labels[i] == 1:
            word_pos_counts.update(words)
        else:
            word_neg_counts.update(words)

    chi_results = []
    for word in all_vocab:
        # A: Word in Positive reviews
        A = word_pos_counts[word]
        # C: Word in Negative reviews
        C = word_neg_counts[word]
        # B: Word NOT in Positive reviews
        B = num_pos - A
        # D: Word NOT in Negative reviews
        D = num_neg - C

        # Calculate Chi-square score
        denominator = (A + B) * (C + D) * (A + C) * (B + D)
        if denominator == 0: continue
            
        chi_score = (N * (A * D - B * C)**2) / denominator
        
        # We also track A/C to determine sentiment direction later
        chi_results.append({
            'word': word,
            'score': chi_score,
            'pos_count': A,
            'neg_count': C
        })

    # Get Top 100 features
    return sorted(chi_results, key=lambda x: x['score'], reverse=True)[:100]


def auto_label_reviews(reviews):
    # Simple lexicon-based labelling: returns list of 1 (positive) or 0 (negative)
    pos_lex = {
        'love', 'great', 'amazing', 'wonderful', 'best', 'excellent', 'delight', 'luxurious', 'pleasant', 'liked', 'loveit', 'favorite'
    }
    neg_lex = {
        'bad', 'disappoint', 'disappointed', 'not', "don't", 'dont', 'return', 'worst', 'odd', 'oddest', 'expensive', 'pricey', 'overpowering'
    }

    labels = []
    for review in reviews:
        clean = re.sub(r'[^\w\s]', '', review.lower())
        words = clean.split()
        pos_count = sum(1 for w in words if w in pos_lex)
        neg_count = sum(1 for w in words if w in neg_lex)

        if pos_count > neg_count:
            labels.append(1)
        elif neg_count > pos_count:
            labels.append(0)
        else:
            # fallback: treat presence of common positive tokens as positive
            labels.append(1 if any(w in words for w in ('love', 'great', 'amazing', 'like')) else 0)

    return labels


if __name__ == "__main__":
    # Load sample reviews and auto-label
    with open('sample_reviews.json', 'r', encoding='utf-8') as f:
        reviews = json.load(f)

    labels = auto_label_reviews(reviews)

    results = calculate_chi_square(reviews, labels)

    # Print results: word, chi2 score, pos_count, neg_count, associated sentiment
    print(f"{'Word':<20} {'Chi2':>10} {'PosDocs':>8} {'NegDocs':>8} {'Assoc'}")
    print('-' * 60)
    for r in results:
        assoc = 'Ambiguous'
        if r['pos_count'] > r['neg_count']:
            assoc = 'Positive'
        elif r['neg_count'] > r['pos_count']:
            assoc = 'Negative'

        print(f"{r['word']:<20} {r['score']:10.4f} {r['pos_count']:8d} {r['neg_count']:8d} {assoc}")
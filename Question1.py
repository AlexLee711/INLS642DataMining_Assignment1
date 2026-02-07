import re
import math
import json
from collections import Counter

def get_top_word_associations(reviews, window_size=5, min_count=50):
    word_counts = Counter()
    pair_counts = Counter()
    total_tokens = 0

    for review in reviews:
        # 1. Preprocessing: Remove punctuation and lowercase (Slide 4)
        clean_text = re.sub(r'[^\w\s]', '', review.lower())
        words = clean_text.split()
        total_tokens += len(words)
        
        # 2. Update individual word counts
        word_counts.update(words)
        
        # 3. Sliding Window for pairs (Slide 3)
        for i in range(len(words)):
            # Look at the next 4 words (total window size 5)
            for j in range(i + 1, min(i + window_size, len(words))):
                pair = tuple(sorted((words[i], words[j]))) # Ordered pair
                pair_counts[pair] += 1

    # 4. Calculate PMI (Slide 3, p. 30)
    pmi_results = []
    for (w1, w2), count in pair_counts.items():
        if count >= min_count:
            # Probabilities
            p_w1_w2 = count / total_tokens
            p_w1 = word_counts[w1] / total_tokens
            p_w2 = word_counts[w2] / total_tokens
            
            pmi = math.log2(p_w1_w2 / (p_w1 * p_w2))
            pmi_results.append(((w1, w2), pmi))
            
    # Sort by PMI score
    return sorted(pmi_results, key=lambda x: x[1], reverse=True)[:100]


if __name__ == "__main__":
    # Load sample reviews from JSON file
    with open('sample_reviews.json', 'r', encoding='utf-8') as f:
        reviews = json.load(f)
    
    # Get top word associations with PMI score (increased min_count for better results)
    results = get_top_word_associations(reviews, window_size=5, min_count=2)
    
    # Display results
    print("Top Word Associations (PMI Scores)")
    print("=" * 70)
    print(f"{'Word 1':<15} {'Word 2':<15} {'PMI Score':<15} {'Co-occur Count'}")
    print("-" * 70)
    
    for (word1, word2), pmi_score in results[:30]:
        print(f"{word1:<15} {word2:<15} {pmi_score:>10.4f}")
    
    print("-" * 70)
    print(f"Total word associations found: {len(results)}")


def get_ngrams(word, n):
    """Break a word into overlapping n-grams."""
    return set(word[i:i+n] for i in range(len(word) - n + 1))
def get_ngrams(word, n):
    """Break a word into overlapping n-grams."""
    word = word.lower()
    if len(word) < n:
        return {word}
    return set(word[i:i+n] for i in range(len(word) - n + 1))


def jaccard_similarity(set1, set2):
    """Calculate Jaccard: Intersection / Union."""
    if not set1 or not set2:
        return 0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def find_top_matches(target, dictionary, n=3):
    """Find top 10 matches for a target word in a dictionary."""
    target_ngrams = get_ngrams(target, n)
    results = []

    for word in dictionary:
        word_ngrams = get_ngrams(word, n)
        score = jaccard_similarity(target_ngrams, word_ngrams)
        results.append((word, score))

    # Sort by score descending then by word
    return sorted(results, key=lambda x: (x[1], x[0]), reverse=True)[:10]


def levenshtein_distance(a, b):
    """Compute Levenshtein edit distance between two strings."""
    a = a.lower()
    b = b.lower()
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[n]


def find_top_matches_edit(target, dictionary):
    """Find top 10 matches by smallest edit distance."""
    results = []
    for word in dictionary:
        d = levenshtein_distance(target, word)
        results.append((word, d))
    return sorted(results, key=lambda x: (x[1], x[0]))[:10]


def load_dictionary(path=None):
    """Load dictionary words. Try provided path, then /usr/share/dict/words, else fallback small set."""
    import os

    candidates = []
    if path:
        candidates.append(path)
    candidates.append(os.path.join(os.getcwd(), 'a_words.txt'))
    candidates.append('/usr/share/dict/words')

    for p in candidates:
        try:
            with open(p, 'r', encoding='utf-8') as f:
                words = [w.strip() for w in f if w.strip()]
                # keep only words starting with 'a' or all if file is general
                a_words = [w for w in words if w[0].lower() == 'a'] if all(w[0].isalpha() for w in words[:10]) else words
                if a_words:
                    return list(dict.fromkeys(a_words))
        except Exception:
            continue

    # Fallback small sample
    return [
        'abandon', 'abbreviation', 'abbreviate', 'ability', 'abject', 'ablaze',
        'able', 'abnormal', 'abolish', 'aboriginal', 'abort', 'about', 'above',
        'abroad', 'abrupt', 'absence', 'absent', 'absolute', 'absolution', 'absorb',
        'abstract', 'abundance', 'abundant', 'abusive', 'abut', 'academic', 'academy',
        'accelerate', 'accent', 'accept', 'access', 'accident', 'acclaim', 'acclimate',
        'accolade', 'accommodate', 'accompany', 'accomplish', 'accord', 'account',
        'accuracy', 'accurate', 'accuse', 'ache', 'achieve', 'acid', 'acorn', 'acoustic'
    ]


def pretty_print_list(items, limit=10, show_score=True):
    out = []
    for i, item in enumerate(items[:limit], 1):
        if show_score:
            out.append(f"{i}. {item[0]}\t{item[1]:.4f}")
        else:
            out.append(f"{i}. {item[0]}\t{item[1]}")
    return "\n".join(out)


if __name__ == '__main__':
    # Test words requested in the assignment
    test_words = [
        'abreviation',
        'abstrictiveness',
        'accanthopterigenous',
        'artifitial inteligwnse',
        'agglumetation'
    ]

    dictionary = load_dictionary()
    print(f"Loaded dictionary with {len(dictionary)} words (sample: {dictionary[:5]})\n")

    for target in test_words:
        print('=' * 60)
        print(f"Target: {target}\n")
        for n in (2, 3, 4, 5):
            top = find_top_matches(target, dictionary, n=n)
            print(f"Top 10 by Jaccard with {n}-grams:")
            print(pretty_print_list(top, show_score=True))
            print()

        top_edit = find_top_matches_edit(target, dictionary)
        print("Top 10 by Levenshtein (distance):")
        print(pretty_print_list(top_edit, show_score=False))
        print('\n')
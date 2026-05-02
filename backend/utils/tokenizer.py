def tokenize(text):
    words = text.lower().split()
    return [abs(hash(w)) % 1000 for w in words]
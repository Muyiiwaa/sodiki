import re

def extract_words_after_prompt(text):
    pattern = r'(?<=prompt:)\s*\b(\w+)\b'
    matches = re.findall(pattern, text)
    words_str = ' '.join(matches)
    return words_str

# Example usage:
text = "This is a prompt: example sentence. Words after prompt: data science and analytics."
words_after_prompt = extract_words_after_prompt(text)
print(words_after_prompt)
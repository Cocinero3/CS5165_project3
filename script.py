import socket
import os
from collections import Counter
import re

def count_words(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        words = re.findall(r'\b\w+(?:\'[a-z]+)?\b', content.lower())
        return len(words), content

def get_words_with_contractions_handled(text):
    # split contradictions
    words = []
    for word in re.findall(r'\b[\w\']+\b', text.lower()):
        if "'" in word:
            parts = word.split("'")
            for part in parts:
                if part:  # only add non-empty parts
                    words.append(part)
        else:
            words.append(word)
    
    return words

def get_top_words(text, n=3, handle_contractions=False):
    # remove punctuation except apostrophes
    text = re.sub(r'[^\w\s\']', '', text.lower())
    
    if handle_contractions:
        words = get_words_with_contractions_handled(text)
    else:
        words = re.findall(r'\b\w+\b', text.lower())
    
    word_counts = Counter(words)
    # filter empty strings 
    if '' in word_counts:
        del word_counts['']
    
    return word_counts.most_common(n)

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except:
            try:
                return os.popen('hostname -I').read().strip().split()[0]
            except:
                return "Could not determine IP address"

def main():
    if_path = "/home/data/IF.txt"
    always_path = "/home/data/AlwaysRememberUsThisWay.txt"
    result_path = "/home/data/output/result.txt"
    
    if_word_count, if_content = count_words(if_path)
    
    always_word_count, always_content = count_words(always_path)
    
    total_words = if_word_count + always_word_count
    
    top_if_words = get_top_words(if_content)
    
    top_always_words = get_top_words(always_content, handle_contractions=True)
    
    ip_address = get_ip_address()
    
    with open(result_path, 'w') as result_file:
        result_file.write(f"Word count in {os.path.basename(if_path)}: {if_word_count}\n")
        result_file.write(f"Word count in AlwaysRememberUsThisWay.txt: {always_word_count}\n")
        result_file.write(f"Total word count: {total_words}\n\n")
        
        result_file.write(f"Top 3 words in {os.path.basename(if_path)}:\n")
        for word, count in top_if_words:
            result_file.write(f"{word}: {count}\n")
        
        result_file.write("\nTop 3 words in AlwaysRememberUsThisWay.txt (with contractions handled):\n")
        for word, count in top_always_words:
            result_file.write(f"{word}: {count}\n")
        
        result_file.write(f"\nIP Address: {ip_address}\n")
    
    # print results.txt
    with open(result_path, 'r') as result_file:
        print(result_file.read())

if __name__ == "__main__":
    main()

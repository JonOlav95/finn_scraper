import re

urls = [
    "https://www.example.com/job/fulltime/search.html?page=12&published=1",
    "https://www.example.com/realestate/parttime/search.html?page=15&published=1",
    "https://www.example.com/job/contract/search.html?page=10&published=1",
    # Add more URLs as needed
]

# Define the regular expression pattern
pattern = re.compile(r'example\.com/(\w+)/(\w+)')

# Extract the first two words after example.com in each URL
word_pairs = [(match.group(1), match.group(2)) for url in urls if (match := re.search(pattern, url))]

# Print the extracted word pairs
print("Extracted word pairs:", word_pairs)

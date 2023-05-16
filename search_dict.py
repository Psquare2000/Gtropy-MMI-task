class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Dictionary:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    # Time Complexity = word in dict? O(n):O(m*n*k) 
    # Space Complexity = word in dict ? O(1): O(k*avg_word_length*char_size) 
    # where k is number of words starting with first letter of search_word
    # m = length of longest word and n =  length of search word
    def search_word(self, word):
        node = self.root
        closest_word = ""
        for char in word:
            if char not in node.children:
                break
            node = node.children[char]
            closest_word += char
        else:
            if node.is_word:
                return True

        self.suggested_words.clear()
        self.find_closest_word(self.root.children[word[0]],word[0], word)
        return False
    
    suggested_words = set()

    # Time Complexity = O(m*n*k) 
    # Space Complexity = O(k*avg_word_length*char_size) 
    # where k is number of words starting with first letter of search_word
    # m = length of longest word and n =  length of search word
    def find_closest_word(self, node, prefix, target_word):
        closest_word = ""
        closest_distance = float('inf')

        if node.is_word:
            distance = self.calculate_distance(prefix, target_word)
            if distance <  closest_distance:
                closest_word = prefix
                closest_distance = distance
                if distance <= 2: 
                    self.suggested_words.add(closest_word)
                # threhold can be limited to one character difference for less suggestions

        for char, child_node in node.children.items():
            # print(prefix + char)
            word = self.find_closest_word(child_node, prefix + char, target_word)
            # word = prefix + char
            distance = self.calculate_distance(word, target_word)
            if distance <  closest_distance:
                closest_word = word
                closest_distance = distance
                if distance <= 2:
                    self.suggested_words.add(closest_word)

        return closest_word

    # Time Complexity = O(m*n) 
    # m = length of longest word and n =  length of search word
    # Space complexity = O(m+1*n+1)
    def calculate_distance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(
                        dp[i - 1][j] + 1,  # deletion
                        dp[i][j - 1] + 1,  # insertion
                        dp[i - 1][j - 1] + 1  # substitution
                    )

        return dp[m][n]

# Creating an instance of the dictionary
my_dictionary = Dictionary()

# text file path
file_path = "DICT.txt"

# Space complexity = O(N*average_word_length*char_size)
# Time complexity = O(N) 
# N = number of words in the dictionary
try:
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            my_dictionary.add_word(word)
    print("Dictionary created successfully!")

except FileNotFoundError:
    print("File not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Searching for a word in the dictionary
terminate = False
while(not terminate):
    search_word = input("Enter a word to search in the dictionary or press @ to escape: ")
    if search_word == "@":
        terminate = True
        continue
    elif search_word == "":
        print("Please enter a word")
        continue
    elif " " in search_word :
        print("Please enter only one word at a time")
        continue
    elif not search_word.isalpha():
        has_bad_char = False
        for alphabet in search_word:
            if not ((alphabet >= 'a' and alphabet <= 'z') or (alphabet >= 'A' and alphabet <= 'Z') or alphabet == "'"):
                has_bad_char= True
                print("The dictionary consists of words and shortened phrases only")
                break
        if has_bad_char :continue
    
    search_word = search_word.lower()
    found_word = my_dictionary.search_word(search_word)

    if found_word :
        print(f"Word found in the dictionary: {search_word}")
    else:
        print(f"No matching word found. Did you mean {my_dictionary.suggested_words} ?")
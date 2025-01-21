from difflib import SequenceMatcher
import Levenshtein


class NameChecker:
    def __init__(self, male_names_file, female_names_file):
            self.male_names = self.load_names(male_names_file)
            self.female_names = self.load_names(female_names_file)

    # Load datasets
    def load_names(file_path):
        with open(file_path, 'r') as file:
            return [line.strip().lower() for line in file.readlines()]

    # Match names using similarity threshold
    def find_matches(list1, list2, threshold=0.8):
        matches = []
        for name1 in list1:
            for name2 in list2:
                similarity = SequenceMatcher(None, name1, name2).ratio()
                # Or use Levenshtein ratio
                # similarity = Levenshtein.ratio(name1, name2)
                if similarity >= threshold:
                    matches.append((name1, name2, round(similarity, 2)))
        return matches

    # Main
    male_names = load_names('male.txt')
    female_names = load_names('female.txt')

    # Adjust threshold to control similarity (1.0 is exact match)
    similarity_threshold = 0.8
    matches = find_matches(male_names, female_names, threshold=similarity_threshold)

    # Output matches
    print(f"Found {len(matches)} matches:")
    for match in matches:
        print(f"{match[0]} - {match[1]} (Similarity: {match[2]})")

    # Save matches to a file
    with open('matches.txt', 'w') as file:
        for match in matches:
            file.write(f"{match[0]} - {match[1]} (Similarity: {match[2]})\n")

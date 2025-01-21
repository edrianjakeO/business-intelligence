class NameChecker:
    def __init__(self, male_names_file, female_names_file):
        self.male_names = self.load_names(male_names_file)
        self.female_names = self.load_names(female_names_file)

    def load_names(self, file_path):
        """Load names from a text file into a set for fast lookup."""
        with open(file_path, 'r') as file:
            return {name.strip().lower() for name in file.readlines()}

    def check_name(self, name):
        """Check if the name is in male or female names."""
        first_name = str(name).split()[0].lower()

        if first_name == "":
            return '0000'  # Empty
        elif first_name == 'nan':
            return '0002'  # Not a valid name
        elif first_name in self.male_names:
            return '0002'  # Male
        elif first_name in self.female_names:
            return '0001'  # Female
        else:
            return '0002'  # Not found
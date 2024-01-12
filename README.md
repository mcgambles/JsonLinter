# linter

Prerequisites:
Python 3+
pip install json
pip install jsonschema

Linter.py performs JSON validation for all App-Factory templates within AppTemplatesJson directory. Here how it works:

1. compile_category_pattern() and compile_name_pattern(): These functions compile regex patterns for validating the "Category" and "Name" fields in the JSON respectively. 
2. load_json_schema(): This function defines a JSON schema. It specifies the expected structure of the JSON files to be validated. 
        It expects a JSON object with "Name" as a required string, "Generic" as a boolean, and "Category" as a string. It uses the compiled regex patterns for validation.
3. search_and_validate_json(directory_path, ignore_file): This function performs the validation process.
	It constructs the directory path where JSON files are expected to be found.
	It gathers all JSON files within the specified directory and its subdirectories.
	It loads an ignore list from a file, if available.
	Then, it iterates through each JSON file found:
		Checks if the file is in the ignore list. If so, it skips validation for that file.
		Verifies if the file is empty. If so, it prints an error message and exits the validation.
		Reads and parses the JSON content from the file.
		Validates the parsed JSON against the defined schema:
			If validation fails, it prints the errors and exits the validation for that file.
			If validation passes, it increments the validated count.
 

The validation process checks for the presence of specific keys ("Name", "Generic", "Category") and their types in the JSON files. It also employs regex patterns to validate the format of the "Name" and "Category" fields. These patterns are set by developers. 

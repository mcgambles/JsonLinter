import os
import json
import jsonschema
import sys
import re


def compile_category_pattern():
    # Compiling the regex pattern for Category outside the loop
    # Pattern allowing uppercase words and excluding only "_and_" in lowercase
    pattern = re.compile(r'^_?[A-Z][a-zA-Z0-9]*(?:_(?:[A-Z][a-zA-Z0-9]*|and))*$')
    return pattern


def compile_name_pattern():
    # Compiling the regex pattern for Name outside the loop
    pattern = re.compile("^(?!\\s*$).+")
    return pattern


def load_json_schema():
    schema = {
        "type": "object",
        "properties": {
            "Name": {
                "type": "string",
                "minLength": 1,
                "pattern": compile_name_pattern()
            },
            "Generic": {
                "type": "boolean"
            },
            "Category": {
                "type": "string",
                "minLength": 1,
                "pattern": compile_category_pattern()
            }
            # Add other properties of your JSON schema
        },
        "required": ["Name"]
    }
    return schema


def search_and_validate_json(ignore_file):
    current_directory = os.getcwd()  # Get the current working directory
    app_templates_dir = os.path.join(current_directory, "AppTemplatesJson")

    if not os.path.exists(app_templates_dir) or not os.path.isdir(app_templates_dir):
        print("Error: AppTemplatesJson directory not found in the current working directory.")
        return

    json_files = []
    for root, _, files in os.walk(app_templates_dir):
        for filename in files:
            if filename.endswith(".json"):
                json_files.append(os.path.join(root, filename))

    if not json_files:
        print("Error: No JSON files found in the AppTemplatesJson directory")
        return

    # Read the ignore list file
    ignore_list = set()
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as ignore_file:
            ignore_list = {line.strip() for line in ignore_file}

    print("Validating JSON files in the AppTemplatesJson directory:")
    schema = load_json_schema()  # Load the schema outside the loop

    validated_count = 0
    for file_path in json_files:
        try:
            filename = os.path.basename(file_path)
            if filename in ignore_list:
                print(f"{filename} has been whitelisted")
                continue

            if os.path.getsize(file_path) == 0:
                print(f"Error: {file_path} is empty")
                sys.exit(1)

            with open(file_path, 'r') as file:
                parsed_json = json.load(file)

                if not parsed_json:
                    print(f"Error: {file_path} contains no data")
                    sys.exit(1)

                validator = jsonschema.Draft7Validator(schema)
                errors = list(validator.iter_errors(parsed_json))

                if errors:
                    print("Error: " + file_path + " does not conform to the schema")
                    for error in errors:
                        print(error.message)
                    sys.exit(1)
                else:
                    validated_count += 1

        except Exception as e:
            print("Error: An error occurred while processing " + file_path + ": " + str(e))
            sys.exit(1)

    print(
        f"============================ Validated {validated_count} AppTemplates successfully ============================")


def main():
    ignore_file_path = "ignore_list.txt"
    search_and_validate_json(ignore_file_path)


if __name__ == "__main__":
    main()

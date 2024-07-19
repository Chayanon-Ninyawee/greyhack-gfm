import re
import os

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def replace_import_code(content, base_path):
    pattern = r'import_code\("([^"]+)"\)'
    matches = re.finditer(pattern, content)

    for match in matches:
        import_path = os.path.join(base_path, match.group(1))
        if os.path.exists(import_path):
            imported_content = read_file(import_path)
            imported_content = replace_import_code(imported_content, base_path)
            content = content.replace(match.group(0), imported_content)
        else:
            print(f"Warning: {import_path} does not exist.")

    return content

def remove_comments_and_whitespace(content):
    # Remove comments
    content = re.sub(r'//.*', '', content)

    # Remove leading/trailing whitespace and lines with no content
    lines = content.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    return '\n'.join(lines)


main_filepath = 'main.src'
output_filepath = 'build/gfmauto.src'
shortened_output_filepath = 'build/gfmauto_shortened.src'

if os.path.exists(main_filepath):
    main_content = read_file(main_filepath)
    base_path = os.path.dirname(main_filepath)
    new_content = replace_import_code(main_content, base_path)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    # Write the full version of the file
    with open(output_filepath, 'w') as output_file:
        output_file.write(new_content)

    # Generate and write the shortened version of the file
    shortened_content = remove_comments_and_whitespace(new_content)
    with open(shortened_output_filepath, 'w') as shortened_output_file:
        shortened_output_file.write(shortened_content)

    print(f"Output written to {output_filepath}")
    print(f"Shortened output written to {shortened_output_filepath}")
else:
    print(f"Error: {main_filepath} does not exist.")
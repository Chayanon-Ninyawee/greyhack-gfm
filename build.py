import re
import os

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def replace_import_code(content, base_path, seen_imports=None):
    if seen_imports is None:
        seen_imports = set()

    pattern = r'import_code\("([^"]+)"\)'
    matches = re.finditer(pattern, content)

    for match in matches:
        import_path_raw = match.group(1)
        
        # Remove leading slash if present
        if import_path_raw.startswith('/'):
            import_path_raw = import_path_raw[1:]

        import_path = os.path.join(base_path, import_path_raw)
        normalized_path = os.path.normpath(import_path)

        if normalized_path in seen_imports:
            # Skip already imported files
            content = content.replace(match.group(0), "")
            # print(f'Info: Skipped "{normalized_path}" since it already imported.')
            continue

        if os.path.exists(import_path):
            seen_imports.add(normalized_path)
            imported_content = read_file(import_path)
            imported_content = replace_import_code(imported_content, base_path, seen_imports)
            imported_content = replace_import_script(imported_content, base_path)
            content = content.replace(match.group(0), imported_content)
        else:
            print(f'Warning: "{import_path}" does not exist.')

    return content

def replace_import_script(content, base_path):
    pattern = r'"@import_script\(([^"]+)\)"'
    matches = re.finditer(pattern, content)

    for match in matches:
        import_path = os.path.join(base_path, match.group(1))
        if os.path.exists(import_path):
            imported_content = read_file(import_path)
            imported_content = replace_import_code(imported_content, base_path)
            imported_content = replace_import_script(imported_content, base_path)
            imported_content = remove_comments_and_whitespace(imported_content)
            imported_content = imported_content.replace('"', '""')
            imported_content = imported_content.replace('\n', ';')
            imported_content = f'"{imported_content}"'
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


def process_file(main_filepath, output_filepath, shortened_output_filepath):
    if os.path.exists(main_filepath):
        main_content = read_file(main_filepath)
        new_content = replace_import_code(main_content, "")

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


process_file('src/main.src', 'build/gfmTools.src', 'build/gfmTools_shortened.src')
process_file('generateEncryptedString.src', 'build/generateEncryptedString.src', 'build/generateEncryptedString_shortened.src')

#!/usr/bin/env python3
import os
import sys

def process_directory(root_dir):
    """
    Process files in the root directory and its subdirectories.
    - Files in root go to main.py
    - Files in subdirs go to a file named after the first subdir
    """
    print(f"Processing directory: {os.path.abspath(root_dir)}")

    # Dictionary to store file contents
    output_files = {"main.py": []}

    # Counter for tracking processed files
    processed_files = 0

    # Walk through all directories and files
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories (those starting with .) and __pycache__ directories
        # But be careful not to skip directories that just contain a dot in their path
        rel_path = os.path.relpath(dirpath, root_dir)
        path_parts = rel_path.split(os.sep)

        # Skip only if a part starts with dot or is __pycache__
        # (but don't skip the root directory which is represented as '.')
        if (rel_path != '.' and 
            (any(part.startswith('.') and part != '.' for part in path_parts) or 
             '__pycache__' in path_parts)):
            print(f"Skipping directory: {dirpath}")
            continue

        print(f"Examining directory: {dirpath}")

        # Process each file in the current directory
        for filename in filenames:
            # Skip hidden files and non-python files
            if filename.startswith('.') or not filename.endswith('.py'):
                continue

            file_path = os.path.join(dirpath, filename)
            print(f"Processing file: {file_path}")

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Determine which output file to use
                if rel_path == '.':
                    # File is in the root directory, add to main.py
                    header = f"## {filename}"
                    output_files["main.py"].append(f"{header}\n{content}\n\n")
                    print(f"Added {filename} to main.py")
                else:
                    # Get the first subdirectory
                    parts = rel_path.split(os.sep)
                    first_subdir = parts[0]

                    # Create the output file name for this subdirectory if it doesn't exist
                    if first_subdir not in output_files:
                        output_files[first_subdir] = []
                        print(f"Created new output file for subdirectory: {first_subdir}")

                    # Create the header with the full relative path to the file
                    sub_path = os.path.join(rel_path, filename)
                    header = f"## {sub_path}"
                    output_files[first_subdir].append(f"{header}\n{content}\n\n")
                    print(f"Added {sub_path} to {first_subdir}")

                processed_files += 1

            except Exception as e:
                print(f"Error processing {file_path}: {e}", file=sys.stderr)

    print(f"Processed {processed_files} Python files.")
    print(f"Found {len(output_files)} output files to create.")

    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {os.path.abspath(output_dir)}")
    else:
        print(f"Using existing output directory: {os.path.abspath(output_dir)}")

    # Write all the accumulated content to their respective files in the output directory
    files_written = 0
    for output_file, contents in output_files.items():
        if contents:  # Only write files that have content
            output_path = os.path.join(output_dir, output_file)
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(''.join(contents))
                print(f"Created {output_path} with {len(contents)} sections")
                files_written += 1
            except Exception as e:
                print(f"Error writing to {output_path}: {e}", file=sys.stderr)
        else:
            print(f"Skipping {output_file} because it has no content")

    print(f"Successfully wrote {files_written} files to {os.path.abspath(output_dir)}")
    return files_written

if __name__ == "__main__":
    # Use current directory if no argument is provided
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    file_count = process_directory(directory)
    if file_count > 0:
        print(f"File concatenation complete! {file_count} files created in the output directory.")
    else:
        print("No files were created. Check if there are any Python files in the directory.")
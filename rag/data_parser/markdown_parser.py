import os
from typing import Dict


class MarkdownProcessor:
    """
    A class to process and read Markdown files from a directory.
    """

    def read_markdown_files_from_directory(self, directory_path: str) -> Dict[str, str]:
        """
        Reads all Markdown (.md) files from a given directory and returns their
        contents in a dictionary.

        The dictionary keys are the filenames (without the .md extension), and the
        values are the string contents of the files.

        Args:
            directory_path: The absolute or relative path to the directory
                            containing the markdown files.

        Returns:
            A dictionary where each key is a filename and each value is the
            content of that file.

        Raises:
            FileNotFoundError: If the specified directory_path does not exist.
            NotADirectoryError: If the specified path points to a file, not a directory.
        """
        # --- 1. Validate the input path ---
        # Check if the path exists. If not, raise an error.
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Error: The directory '{directory_path}' was not found.")

        # Check if the path is a directory. If it's a file, raise an error.
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Error: The path '{directory_path}' is a file, not a directory.")

        # --- 2. Read the files ---
        markdown_content: Dict[str, str] = {}

        # Iterate over all entries in the directory
        for filename in os.listdir(directory_path):
            # Construct the full path for the current file
            full_path = os.path.join(directory_path, filename)

            # Process only if it's a file and has a '.md' extension
            if os.path.isfile(full_path) and filename.lower().endswith('.md'):
                try:
                    # Open and read the file content
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Get the filename without the '.md' extension for the dictionary key
                    base_filename = os.path.splitext(filename)[0]

                    # Store the content in the dictionary
                    markdown_content[base_filename] = content
                except Exception as e:
                    print(f"Could not read file {filename} due to error: {e}")

        # --- 3. Return the result ---
        return markdown_content

# Example of how to use the class
if __name__ == '__main__':
    # Create a dummy directory and some files for demonstration
    if not os.path.exists('temp_md_files'):
        os.makedirs('temp_md_files')

    with open('temp_md_files/file1.md', 'w') as f:
        f.write('# This is file 1\n\nHello, World!')
    with open('temp_md_files/another_file.md', 'w') as f:
        f.write('## This is another file\n\n* Item 1\n* Item 2')
    with open('temp_md_files/should_be_ignored.txt', 'w') as f:
        f.write('This is a text file and should be ignored.')

    # Instantiate the processor and call the method
    processor = MarkdownProcessor()
    try:
        data = processor.read_markdown_files_from_directory('./rag/test-data')

        # Print the result in a readable format
        import json
        print("Successfully read markdown files. Contents:")
        print(json.dumps(data, indent=4))

    except (FileNotFoundError, NotADirectoryError) as e:
        print(e)

    # Clean up the dummy files and directory
    import shutil
    shutil.rmtree('temp_md_files')

import os

def is_image_file(file_name):
    """
    Check if the file has an image extension.
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    return os.path.splitext(file_name)[1].lower() in image_extensions

def process_folders(root_path, dry_run=False):
    """
    Traverse folders recursively and create .md files for folders
    containing only image files.
    """
    for folder_name, subfolders, files in os.walk(root_path, topdown=False):
        # Skip folders with subfolders
        if subfolders:
            continue
        
        # Filter out non-image files and hidden files
        image_files = [file for file in files if is_image_file(file)]
        visible_files = [file for file in files if not file.startswith('.')]

        # Check if the folder contains only images (and no hidden/non-image files)
        if visible_files and len(visible_files) == len(image_files):
            parent_directory = os.path.dirname(folder_name)
            md_file_name = f"{os.path.basename(folder_name)}.md"
            md_file_path = os.path.join(parent_directory, md_file_name)

            if dry_run:
                print(f"Dry Run: Would create {md_file_path} with references to {len(image_files)} images.")
            else:
                try:
                    # Create .md file in the parent directory
                    with open(md_file_path, 'w') as md_file:
                        for image_file in sorted(image_files):
                            md_file.write(f"![[{image_file}]]\n")
                    print(f"Created: {md_file_path}")
                except Exception as e:
                    print(f"Error creating {md_file_path}: {e}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    # Set dry_run=True for testing without making changes
    process_folders(current_directory, dry_run=False)

import os
import tarfile
import zipfile
import argparse

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def extract_tar_gz(tar_gz_file):
    """Extracts a .tar.gz file to a folder."""
    if not os.path.exists(tar_gz_file):
        print(f"{RED}Error: File '{tar_gz_file}' not found!{RESET}")
        return None

    extract_folder = os.path.splitext(tar_gz_file)[0]  # Remove .gz
    os.makedirs(extract_folder, exist_ok=True)

    print(f"Extracting {YELLOW}{tar_gz_file}{RESET} to {GREEN}{extract_folder}{RESET}...")
    try:
        with tarfile.open(tar_gz_file, "r:gz") as tar:
            tar.extractall(extract_folder)
        print(f"{GREEN}Extraction completed! Files are in: {extract_folder}{RESET}")
        return extract_folder
    except Exception as e:
        print(f"{RED}Extraction failed: {str(e)}{RESET}")
        return None

def convert_to_zip(folder):
    """Converts an extracted folder to a ZIP archive."""
    if not os.path.exists(folder):
        print(f"{RED}Error: Folder '{folder}' does not exist!{RESET}")
        return None

    zip_file = folder + ".zip"
    print(f"Converting {YELLOW}{folder}{RESET} to {GREEN}{zip_file}{RESET}...")

    try:
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder))

        print(f"{GREEN}Conversion completed! ZIP file saved as: {zip_file}{RESET}")
        return zip_file
    except Exception as e:
        print(f"{RED}ZIP conversion failed: {str(e)}{RESET}")
        return None

def main():
    parser = argparse.ArgumentParser(description="CLI TAR.GZ Unpacker & Converter")
    parser.add_argument("file", help="Path to the .tar.gz file")
    parser.add_argument("--convert", action="store_true", help="Convert extracted folder to .zip")

    args = parser.parse_args()

    extracted_folder = extract_tar_gz(args.file)
    
    if extracted_folder and args.convert:
        convert_to_zip(extracted_folder)

if __name__ == "__main__":
    main()

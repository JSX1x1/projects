import os
import sys
import zipfile
import datetime
import shutil
from pathlib import Path
import argparse

def get_folder_size(folder):
    """Calculate total size of a folder (in bytes)."""
    return sum(f.stat().st_size for f in Path(folder).rglob('*') if f.is_file())

def estimate_compressed_size(folder):
    """Estimate compressed size (roughly 50% of the original for testing)."""
    return get_folder_size(folder) * 0.5  # Approximation

def analyze_files(folder):
    """Detect risky and unnecessary files."""
    risky_files = []
    unnecessary_files = []

    for file in folder.rglob('*'):
        if file.is_file():
            # Check for unreadable files (simulated risk analysis)
            try:
                with open(file, 'rb'):
                    pass
            except:
                risky_files.append(file)

            # Identify unnecessary files (logs, cache, tmp)
            if file.suffix in ['.log', '.tmp', '.cache']:
                unnecessary_files.append(file)

    return risky_files, unnecessary_files

def create_snapshot(folder, exclude_risky, exclude_unnecessary):
    """Creates a ZIP snapshot of the given folder."""
    folder = Path(folder)
    now = datetime.datetime.now().strftime("%m-%d-%Y")
    zip_filename = f"{now}-snapshot.zip"
    zip_path = folder.parent / zip_filename

    risky_files, unnecessary_files = analyze_files(folder)

    files_to_include = list(folder.rglob("*"))
    if exclude_risky:
        files_to_include = [f for f in files_to_include if f not in risky_files]
    if exclude_unnecessary:
        files_to_include = [f for f in files_to_include if f not in unnecessary_files]

    total_files = len(files_to_include)
    if total_files == 0:
        print("No files to compress. Exiting.")
        return

    print(f"Creating snapshot: {zip_path}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i, file in enumerate(files_to_include):
            if file.is_file():
                arcname = file.relative_to(folder)
                zipf.write(file, arcname)
            progress = int((i + 1) / total_files * 100)
            print(f"Progress: {progress}%", end='\r')

    print("\nSnapshot creation complete.")
    print(f"Snapshot saved as: {zip_path}")

def main():
    parser = argparse.ArgumentParser(description="CLI Snapshot Creator")
    parser.add_argument("folder", nargs="?", help="Path to the folder for snapshot")
    parser.add_argument("--exclude-risky", action="store_true", help="Exclude risky files")
    parser.add_argument("--exclude-unnecessary", action="store_true", help="Exclude unnecessary files")
    args = parser.parse_args()

    if args.folder:
        folder = Path(args.folder)
    else:
        folder = Path(input("Enter folder path: ").strip())

    if not folder.exists() or not folder.is_dir():
        print("Invalid folder path. Please provide a valid directory.")
        sys.exit(1)

    print(f"Selected folder: {folder}")

    # Calculate and display details
    total_size = get_folder_size(folder)
    compressed_size = estimate_compressed_size(folder)
    risky_files, unnecessary_files = analyze_files(folder)

    print(f"Estimated Size: {total_size / (1024 ** 2):.2f} MB")
    print(f"Estimated Compressed Size: {compressed_size / (1024 ** 2):.2f} MB")
    print(f"Corruption Risk: {len(risky_files)} files")
    print(f"Unnecessary Files: {len(unnecessary_files)} files")

    # Ask user for confirmation
    if not args.exclude_risky and len(risky_files) > 0:
        exclude_risky = input("Exclude risky files? (y/n): ").strip().lower() == 'y'
    else:
        exclude_risky = args.exclude_risky

    if not args.exclude_unnecessary and len(unnecessary_files) > 0:
        exclude_unnecessary = input("Exclude unnecessary files? (y/n): ").strip().lower() == 'y'
    else:
        exclude_unnecessary = args.exclude_unnecessary

    # Create snapshot
    create_snapshot(folder, exclude_risky, exclude_unnecessary)

if __name__ == "__main__":
    main()

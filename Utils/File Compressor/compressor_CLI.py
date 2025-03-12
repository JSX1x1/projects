import os
import sys
import zlib
import argparse

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def format_size(size):
    """Convert bytes to a human-readable format (KB, MB, etc.)."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"

def compress_file(input_file, compression_level):
    """Compress a file using zlib with the specified level."""
    if not os.path.exists(input_file):
        print(f"{RED}❌ Error: File '{input_file}' not found!{RESET}")
        return

    if os.path.getsize(input_file) == 0:
        print(f"{YELLOW}⚠️ Cannot compress an empty file!{RESET}")
        return

    output_file = input_file + ".compressed"
    compression_level = min(9, max(1, compression_level // 2))  # Scale 1-20 to 1-9

    with open(input_file, "rb") as f:
        data = f.read()

    compressed_data = zlib.compress(data, compression_level)

    with open(output_file, "wb") as f:
        f.write(compressed_data)

    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    reduction = 100 - ((compressed_size / original_size) * 100)
    gain_loss_ratio = original_size / compressed_size if compressed_size > 0 else 0

    # Color output based on compression success
    color = GREEN if reduction > 0 else RED

    print(f"\n📊 {GREEN}Compression Details:{RESET}")
    print(f"📏 Original Size: {format_size(original_size)}")
    print(f"📦 Compressed Size: {format_size(compressed_size)}")
    print(f"🔽 {color}Reduction: {reduction:.2f}%{RESET}")
    print(f"📈 {color}Gain/Loss Ratio: {gain_loss_ratio:.2f}{RESET}")
    print(f"✅ {GREEN}File compressed successfully: {output_file}{RESET}")

def decompress_file(input_file):
    """Decompress a file using zlib."""
    if not os.path.exists(input_file):
        print(f"{RED}❌ Error: File '{input_file}' not found!{RESET}")
        return

    if not input_file.endswith(".compressed"):
        print(f"{RED}❌ Error: The selected file is not a compressed file!{RESET}")
        return

    output_file = input_file.replace(".compressed", ".decompressed")

    with open(input_file, "rb") as f:
        compressed_data = f.read()

    try:
        decompressed_data = zlib.decompress(compressed_data)
    except zlib.error:
        print(f"{RED}❌ Decompression failed! The file may be corrupted.{RESET}")
        return

    with open(output_file, "wb") as f:
        f.write(decompressed_data)

    compressed_size = os.path.getsize(input_file)
    decompressed_size = os.path.getsize(output_file)
    gain_loss_ratio = decompressed_size / compressed_size if compressed_size > 0 else 0

    # Color output based on efficiency
    color = GREEN if gain_loss_ratio < 1 else RED

    print(f"\n📊 {GREEN}Decompression Details:{RESET}")
    print(f"📦 Compressed Size: {format_size(compressed_size)}")
    print(f"📏 Decompressed Size: {format_size(decompressed_size)}")
    print(f"📈 {color}Gain/Loss Ratio: {gain_loss_ratio:.2f}{RESET}")
    print(f"✅ {GREEN}File decompressed successfully: {output_file}{RESET}")

def main():
    parser = argparse.ArgumentParser(description="CLI File Compression Tool")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Mode: compress or decompress")
    parser.add_argument("file", help="Path to the file to compress or decompress")
    parser.add_argument("-l", "--level", type=int, default=5, help="Compression level (1-20)")

    args = parser.parse_args()

    if args.mode == "compress":
        compress_file(args.file, args.level)
    elif args.mode == "decompress":
        decompress_file(args.file)

if __name__ == "__main__":
    main()

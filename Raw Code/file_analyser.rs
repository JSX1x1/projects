use std::fs::File;
use std::io::{Read, BufReader};
use std::path::Path;
use clap::Parser;
use walkdir::WalkDir;
use sha2::{Digest, Sha256};
use md5::{Md5};
use image::io::Reader as ImageReader;
use pdf::file::File as PdfFile;
use zip::read::ZipArchive;
use object::{Object, ObjectSection};
use pelite::pe64::PeFile;

///
/// This tool is for EDUCATIONAL and LEGAL USE ONLY.
/// Do NOT use this for unauthorized file analysis.
/// The creator is NOT responsible for misuse.
///

// INSTALL DEPENDENCIES: cargo add clap walkdir image pdf zip sha2 md-5 pelite object

/// Command-line arguments
#[derive(Parser)]
#[command(version = "1.0", about = "Advanced Metadata File Analyzer")]
struct Args {
    #[arg(short, long)]
    file: String, // Path to the file
}

fn main() {
    let args = Args::parse();
    let file_path = Path::new(&args.file);

    if !file_path.exists() {
        eprintln!("❌ Error: File does not exist!");
        return;
    }

    println!("📂 Analyzing file: {}\n", args.file);
    
    // Detect file type
    match detect_file_type(file_path) {
        Some(file_type) => println!("🔍 File Type Detected: {}", file_type),
        None => println!("🔍 File Type: Unknown"),
    }

    // Compute hashes
    if let Some(hash) = compute_hash::<Sha256>(file_path) {
        println!("🔑 SHA-256: {}", hash);
    }
    if let Some(hash) = compute_hash::<Md5>(file_path) {
        println!("🔑 MD5: {}", hash);
    }

    // Extract metadata based on file type
    if let Some(file_type) = detect_file_type(file_path) {
        match file_type.as_str() {
            "Image" => extract_image_metadata(file_path),
            "PDF" => extract_pdf_metadata(file_path),
            "ZIP Archive" => extract_zip_metadata(file_path),
            "PE Executable" => extract_pe_metadata(file_path),
            "ELF Binary" => extract_elf_metadata(file_path),
            _ => println!("ℹ️ No specialized metadata extraction available for this file type."),
        }
    }
}

/// Detects file type using magic bytes
fn detect_file_type(path: &Path) -> Option<String> {
    let mut file = File::open(path).ok()?;
    let mut buffer = [0; 8];
    file.read_exact(&mut buffer).ok()?;

    let file_type = match &buffer {
        b"%PDF-" => "PDF",
        b"\x89PNG" => "Image",
        b"GIF87a" | b"GIF89a" => "Image",
        b"PK\x03\x04" => "ZIP Archive",
        b"MZ" => "PE Executable", // Windows Executable
        b"\x7FELF" => "ELF Binary", // Linux Executable
        _ => return None,
    };

    Some(file_type.to_string())
}

/// Computes hash (SHA-256 or MD5) for integrity verification
fn compute_hash<T: Digest + Default>(path: &Path) -> Option<String> {
    let mut file = File::open(path).ok()?;
    let mut hasher = T::default();
    let mut buffer = [0; 4096];

    while let Ok(n) = file.read(&mut buffer) {
        if n == 0 { break; }
        hasher.update(&buffer[..n]);
    }

    Some(format!("{:x}", hasher.finalize()))
}

/// Extracts metadata from images (JPEG, PNG, etc.)
fn extract_image_metadata(path: &Path) {
    if let Ok(img) = ImageReader::open(path).and_then(|r| r.with_guessed_format()) {
        println!("🖼 Image Format: {:?}", img.format());
        if let Ok(dimensions) = img.into_dimensions() {
            println!("📏 Dimensions: {}x{}", dimensions.0, dimensions.1);
        }
    }
}

/// Extracts metadata from PDFs
fn extract_pdf_metadata(path: &Path) {
    if let Ok(pdf) = PdfFile::open(path) {
        println!("📚 PDF Version: {:?}", pdf.version);
        println!("📄 Pages: {}", pdf.num_pages());
    }
}

/// Extracts metadata from ZIP archives
fn extract_zip_metadata(path: &Path) {
    let file = File::open(path).ok()?;
    let mut archive = ZipArchive::new(BufReader::new(file)).ok()?;

    println!("📦 ZIP Archive contains:");
    for i in 0..archive.len() {
        if let Ok(file) = archive.by_index(i) {
            println!("📄 {} ({} bytes)", file.name(), file.size());
        }
    }
}

/// Extracts metadata from Windows PE executables
fn extract_pe_metadata(path: &Path) {
    if let Ok(data) = std::fs::read(path) {
        if let Ok(pe) = PeFile::from_bytes(&data) {
            println!("🖥 PE Executable");
            println!("🔹 Entry Point: 0x{:X}", pe.optional_header().AddressOfEntryPoint);
            println!("🔹 Number of Sections: {}", pe.num_sections());
        }
    }
}

/// Extracts metadata from Linux/macOS ELF binaries
fn extract_elf_metadata(path: &Path) {
    let file = File::open(path).ok()?;
    let buffer = BufReader::new(file);
    let object = object::File::parse(buffer).ok()?;

    println!("🐧 ELF Binary");
    println!("🔹 Sections:");
    for section in object.sections() {
        println!("📂 {} - {} bytes", section.name().unwrap_or("[Unknown]"), section.size());
    }
}

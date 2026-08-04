#!/usr/bin/env python3
"""
Compress executable for email transmission
Converts to Base64, then compresses with ZIP
"""

import base64
import zipfile
import os
import sys

def compress_exe(exe_path):
    """Compress exe to Base64 + ZIP for email"""
    
    # Check if file exists
    if not os.path.exists(exe_path):
        print(f"❌ Error: {exe_path} not found!")
        print(f"Current directory: {os.getcwd()}")
        print("\nFiles in directory:")
        for f in os.listdir('.'):
            if f.endswith('.exe'):
                size_mb = os.path.getsize(f) / 1024 / 1024
                print(f"   📦 {f} - {size_mb:.2f} MB")
        return False
    
    original_size = os.path.getsize(exe_path) / 1024 / 1024
    print(f"\n{'='*50}")
    print(f"  Base64 + ZIP Compression")
    print(f"{'='*50}\n")
    print(f"📦 Original file: {exe_path}")
    print(f"   Size: {original_size:.2f} MB\n")
    
    # Step 1: Read binary file
    print("⏳ Step 1/3: Reading binary file...")
    with open(exe_path, 'rb') as f:
        binary_data = f.read()
    print(f"   ✅ Read {len(binary_data):,} bytes")
    
    # Step 2: Convert to Base64
    print("\n⏳ Step 2/3: Converting to Base64...")
    base64_data = base64.b64encode(binary_data).decode('utf-8')
    text_size = len(base64_data) / 1024 / 1024
    print(f"   ✅ Base64 text: {text_size:.2f} MB")
    
    # Save to temporary text file
    temp_txt = "temp_base64.txt"
    with open(temp_txt, 'w') as f:
        f.write(base64_data)
    
    # Step 3: Compress with ZIP
    print("\n⏳ Step 3/3: Compressing with ZIP...")
    zip_name = os.path.splitext(exe_path)[0] + ".zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write(temp_txt, os.path.basename(temp_txt))
    
    # Remove temp file
    os.remove(temp_txt)
    
    zip_size = os.path.getsize(zip_name) / 1024 / 1024
    savings = original_size - zip_size
    percent = (savings / original_size) * 100
    
    print(f"   ✅ Created: {zip_name}")
    
    # Results
    print(f"\n{'='*50}")
    print(f"  RESULTS")
    print(f"{'='*50}")
    print(f"Original exe:     {original_size:.2f} MB")
    print(f"Compressed ZIP:   {zip_size:.2f} MB")
    print(f"Space saved:      {savings:.2f} MB ({percent:.1f}%)")
    
    if zip_size < 25:
        print(f"\n✅ SUCCESS: Under 25 MB - Ready to email!")
        print(f"\n📧 Email this file: {zip_name}")
    else:
        print(f"\n⚠️  WARNING: Still over 25 MB")
        print(f"   Consider using split method instead")
    
    print(f"{'='*50}\n")
    return True


def main():
    # Check for command line argument
    if len(sys.argv) > 1:
        exe_path = sys.argv[1]
    else:
        # Try to find exe in current directory
        exe_files = [f for f in os.listdir('.') if f.endswith('.exe')]
        
        if not exe_files:
            print("❌ No .exe files found in current directory!")
            print(f"Usage: python {sys.argv[0]} <exe_file>")
            return
        
        if len(exe_files) == 1:
            exe_path = exe_files[0]
        else:
            print("Multiple .exe files found:")
            for i, f in enumerate(exe_files, 1):
                size_mb = os.path.getsize(f) / 1024 / 1024
                print(f"  [{i}] {f} - {size_mb:.2f} MB")
            
            choice = input("\nSelect file number: ")
            exe_path = exe_files[int(choice) - 1]
    
    compress_exe(exe_path)


if __name__ == "__main__":
    main()
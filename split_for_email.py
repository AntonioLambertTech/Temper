#!/usr/bin/env python3
"""
Split exe into multiple parts for email
Each part will be under 20 MB
"""

import base64
import os
import sys
import math

def split_exe(exe_path, max_size_mb=20):
    """Split exe into Base64 text parts"""
    
    if not os.path.exists(exe_path):
        print(f"❌ Error: {exe_path} not found!")
        return False
    
    print(f"\n{'='*50}")
    print(f"  Base64 Split Tool")
    print(f"{'='*50}\n")
    
    # Read and encode
    print("⏳ Converting to Base64...")
    with open(exe_path, 'rb') as f:
        binary_data = f.read()
    
    base64_data = base64.b64encode(binary_data).decode('utf-8')
    total_size = len(base64_data)
    
    # Calculate parts
    max_chars = max_size_mb * 1024 * 1024
    num_parts = math.ceil(total_size / max_chars)
    
    print(f"   Original: {os.path.getsize(exe_path)/1024/1024:.2f} MB")
    print(f"   Base64: {total_size/1024/1024:.2f} MB")
    print(f"   Splitting into {num_parts} parts...\n")
    
    # Split into parts
    base_name = os.path.splitext(exe_path)[0]
    parts = []
    
    for i in range(num_parts):
        start = i * max_chars
        end = min((i + 1) * max_chars, total_size)
        part_data = base64_data[start:end]
        
        part_name = f"{base_name}_part{i+1}.txt"
        with open(part_name, 'w') as f:
            f.write(part_data)
        
        part_size = os.path.getsize(part_name) / 1024 / 1024
        print(f"   ✅ Created: {part_name} ({part_size:.2f} MB)")
        parts.append(part_name)
    
    print(f"\n{'='*50}")
    print(f"✅ Split complete! Email all {num_parts} files")
    print(f"{'='*50}\n")
    
    return True


def combine_parts(part_files):
    """Combine split parts back into exe"""
    
    print(f"\n{'='*50}")
    print(f"  Combining {len(part_files)} parts...")
    print(f"{'='*50}\n")
    
    # Read all parts in order
    base64_data = ""
    for part_file in sorted(part_files):
        print(f"⏳ Reading {part_file}...")
        with open(part_file, 'r') as f:
            base64_data += f.read()
    
    # Decode
    print("\n⏳ Decoding to binary...")
    binary_data = base64.b64decode(base64_data)
    
    # Determine output name
    exe_name = part_files[0].replace('_part1', '').replace('.txt', '.exe')
    
    with open(exe_name, 'wb') as f:
        f.write(binary_data)
    
    exe_size = os.path.getsize(exe_name) / 1024 / 1024
    print(f"✅ Created: {exe_name} ({exe_size:.2f} MB)\n")
    
    return True


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--combine':
        # Combine mode
        part_files = [f for f in os.listdir('.') if '_part' in f and f.endswith('.txt')]
        if not part_files:
            print("❌ No part files found!")
            return
        combine_parts(part_files)
    else:
        # Split mode
        if len(sys.argv) > 1:
            exe_path = sys.argv[1]
        else:
            exe_files = [f for f in os.listdir('.') if f.endswith('.exe')]
            if not exe_files:
                print("❌ No .exe files found!")
                print(f"Usage: python {sys.argv[0]} <exe_file>")
                return
            exe_path = exe_files[0]
        
        split_exe(exe_path)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
FIXED: Combine email-split parts into exe
Handles corrupt email attachments
"""

import base64
import os
import sys

def combine():
    """Combine split txt parts back into exe"""
    
    # Find all part files
    part_files = sorted([f for f in os.listdir('.') if '_part' in f and f.endswith('.txt')])
    
    if not part_files:
        print("❌ No part files found!")
        print("Looking for files like: *_part1.txt, *_part2.txt, etc.")
        return False
    
    print(f"\n{'='*60}")
    print(f"  Combining {len(part_files)} parts...")
    print(f"{'='*60}\n")
    
    # Read all parts
    all_data = ""
    for part_file in part_files:
        print(f"⏳ Reading {part_file}...")
        
        # Read as bytes first
        try:
            with open(part_file, 'rb') as f:
                raw_bytes = f.read()
        except Exception as e:
            print(f"❌ Can't read {part_file}: {e}")
            return False
        
        # Convert to string, removing non-ASCII
        clean_text = ""
        removed_count = 0
        
        for byte in raw_bytes:
            if byte < 128:  # ASCII only
                clean_text += chr(byte)
            else:
                removed_count += 1
        
        if removed_count > 0:
            print(f"   ⚠️  Removed {removed_count} non-ASCII bytes")
        
        all_data += clean_text
    
    # Remove whitespace
    print("\n⏳ Cleaning data...")
    all_data = all_data.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
    
    # Remove invalid Base64 characters (keep only A-Z, a-z, 0-9, +, /, =)
    print("⏳ Filtering Base64 characters...")
    valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
    before_len = len(all_data)
    all_data = ''.join(ch for ch in all_data if ch in valid_chars)
    removed = before_len - len(all_data)
    if removed > 0:
        print(f"   ⚠️  Removed {removed} invalid Base64 character(s)")
    
    # Fix Base64 padding (must be multiple of 4)
    print("⏳ Fixing Base64 padding...")
    padding_needed = len(all_data) % 4
    if padding_needed:
        all_data += '=' * (4 - padding_needed)
        print(f"   ⚠️  Added {4 - padding_needed} padding character(s)")
    
    print(f"   Final Base64 length: {len(all_data)} characters")
    
    # Decode Base64
    print("⏳ Decoding Base64...")
    try:
        binary_data = base64.b64decode(all_data)
    except Exception as e:
        print(f"\n❌ Failed to decode: {e}")
        print("\nThe files are too corrupted to recover.")
        print("You need to re-download the original attachments.\n")
        return False
    
    # Determine output filename
    exe_name = part_files[0].replace('_part1', '').replace('.txt', '.exe')
    
    # Write exe
    print(f"⏳ Writing {exe_name}...")
    try:
        with open(exe_name, 'wb') as f:
            f.write(binary_data)
    except Exception as e:
        print(f"❌ Can't write file: {e}")
        return False
    
    # Success
    size_mb = len(binary_data) / 1024 / 1024
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS!")
    print(f"   Created: {exe_name}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"{'='*60}\n")
    
    return True


if __name__ == "__main__":
    result = combine()
    if not result:
        sys.exit(1)

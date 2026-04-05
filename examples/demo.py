"""
Demo script for Cover Letter Generator
Shows how to use the core module programmatically.

Usage:
    python examples/demo.py
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.cover_letter_gen.core import load_config, get_tones, read_file, extract_skills, match_skills, build_prompt, generate_cover_letter, save_revision, list_revisions


def main():
    """Run a quick demo of Cover Letter Generator."""
    print("=" * 60)
    print("🚀 Cover Letter Generator - Demo")
    print("=" * 60)
    print()
    # Using load_config
    print("📝 Example: load_config()")
    result = load_config()
    print(f"   Result: {result}")
    print()
    # Using get_tones
    print("📝 Example: get_tones()")
    result = get_tones()
    print(f"   Result: {result}")
    print()
    # Read content from a text file.
    print("📝 Example: read_file()")
    result = read_file(
        filepath="sample.txt"
    )
    print(f"   Result: {result}")
    print()
    # Extract skills from text and categorize them.
    print("📝 Example: extract_skills()")
    result = extract_skills(
        text="The quick brown fox jumps over the lazy dog. This is a sample text for demonstration purposes."
    )
    print(f"   Result: {result}")
    print()
    print("✅ Demo complete! See README.md for more examples.")


if __name__ == "__main__":
    main()

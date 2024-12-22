#!/usr/bin/env python3

import json
import argparse

def load_source_type_dict(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_source_type_dict(file_path, source_type_dict):
    with open(file_path, 'w') as file:
        json.dump(source_type_dict, file, indent=4)

def add_source_type(file_path, key, value):
    source_type_dict = load_source_type_dict(file_path)
    source_type_dict[key] = value
    save_source_type_dict(file_path, source_type_dict)

def remove_source_type(file_path):
    source_type_dict = load_source_type_dict(file_path)
    if not source_type_dict:
        print("No source types to remove.")
        return

    print("Select a key value pair to remove:")
    for idx, (key, value) in enumerate(source_type_dict.items(), start=1):
        print(f"{idx}. {key}: {value}")

    selection = input("Enter the number of the key value pair to remove: ")
    try:
        idx = int(selection) - 1
        if idx < 0 or idx >= len(source_type_dict):
            raise ValueError
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    key_to_remove = list(source_type_dict.keys())[idx]
    del source_type_dict[key_to_remove]
    save_source_type_dict(file_path, source_type_dict)

def main():
    parser = argparse.ArgumentParser(description="Modify source type dictionary")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add-source-type", "-a", nargs=2, metavar=("key", "value"),
                       help="Add a new key value pair")
    group.add_argument("--remove-source-type", "-r", action="store_true",
                       help="Remove an existing key value pair")

    args = parser.parse_args()

    file_path = "/herringbone/receiver/source_type_dict.json"

    if args.add_source_type:
        key, value = args.add_source_type
        add_source_type(file_path, key, value)
        print(f"Added key value pair: {key}: {value}")
    elif args.remove_source_type:
        remove_source_type(file_path)
        print("Key value pair removed.")

if __name__ == "__main__":
    main()
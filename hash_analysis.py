#!/usr/bin/env python3

import sys
import argparse
from collections import defaultdict

def parse_hashcat_output(filename):
    length_counts = defaultdict(int)
    passwords = []
    empty_users = []
    total = 0
    skipped = 0
    empty_count = 0

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(':')

            if len(parts) == 3:
                username = parts[0]
                password = parts[2]
            elif len(parts) == 2:
                username = parts[0]
                password = parts[1]
            else:
                skipped += 1
                continue

            if not password:
                empty_count += 1
                empty_users.append(username)
                continue

            length_counts[len(password)] += 1
            passwords.append(password)
            total += 1

    return length_counts, passwords, total, skipped, empty_count, empty_users


def categorize_password(password):
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c in '0123456789' for c in password)
    has_special = any(not c.isalnum() for c in password)

    if has_special and has_upper and has_lower and has_digit:
        return "Mixed Case + Numbers + Special"
    elif has_special and has_lower and has_digit:
        return "Lower + Numbers + Special"
    elif has_special and has_upper and has_digit:
        return "Upper + Numbers + Special"
    elif has_special and has_upper and has_lower:
        return "Mixed Case + Special"
    elif has_special and has_digit:
        return "Numbers + Special"
    elif has_special and has_lower:
        return "Lower + Special"
    elif has_special and has_upper:
        return "Upper + Special"
    elif has_special:
        return "Special Only"
    elif has_upper and has_lower and has_digit:
        return "Mixed Case + Numbers"
    elif has_upper and has_lower:
        return "Mixed Case"
    elif has_upper and has_digit:
        return "Upper + Numbers"
    elif has_lower and has_digit:
        return "Lower + Numbers"
    elif has_upper:
        return "Uppercase Only"
    elif has_lower:
        return "Lowercase Only"
    elif has_digit:
        return "Numbers Only"
    else:
        return "Other"


def print_length_table(length_counts, total):
    col1 = 12
    col2 = 12
    col3 = 12
    table_width = col1 + col2 + col3 + 1

    print("\n" + "=" * table_width)
    print(f"{'Password Length Analysis':^{table_width}}")
    print("=" * table_width)
    print(f"{'Length':^{col1}}{'Count':^{col2}}{'% of Total':^{col3}}")
    print("-" * table_width)

    for length in sorted(length_counts.keys()):
        count = length_counts[length]
        pct = (count / total) * 100
        print(f"{str(length):^{col1}}{str(count):^{col2}}{f'{pct:.1f}%':^{col3}}")

    print("-" * table_width)
    print(f"{'Total':^{col1}}{str(total):^{col2}}")
    print("=" * table_width)


def print_charset_table(passwords, total):
    category_order = [
        "Lowercase Only",
        "Uppercase Only",
        "Numbers Only",
        "Lower + Numbers",
        "Upper + Numbers",
        "Mixed Case",
        "Mixed Case + Numbers",
        "Lower + Special",
        "Upper + Special",
        "Numbers + Special",
        "Mixed Case + Special",
        "Lower + Numbers + Special",
        "Upper + Numbers + Special",
        "Mixed Case + Numbers + Special",
        "Special Only",
        "Other"
    ]

    counts = defaultdict(int)
    for p in passwords:
        counts[categorize_password(p)] += 1

    col1 = 32
    col2 = 10
    col3 = 12
    table_width = col1 + col2 + col3

    print("\n" + "=" * table_width)
    print(f"{'Character Set Analysis':^{table_width}}")
    print("=" * table_width)
    print(f"{'  Category':<{col1}}{'Count':^{col2}}{'% of Total':^{col3}}")
    print("-" * table_width)

    for category in category_order:
        count = counts.get(category, 0)
        if count == 0:
            continue
        pct = (count / total) * 100
        print(f"{'  ' + category:<{col1}}{str(count):^{col2}}{f'{pct:.1f}%':^{col3}}")

    print("-" * table_width)
    print(f"{'  Total':<{col1}}{str(total):^{col2}}")
    print("=" * table_width)


def print_weak_accounts(weak_accounts, threshold):
    print(f"\n*** WARNING: {len(weak_accounts)} account(s) with passwords <= {threshold} characters ***")
    print(f"  {'Username':<20} {'Password Length'}")
    print(f"  {'-'*18} {'-'*15}")
    for username, password in sorted(weak_accounts, key=lambda x: len(x[1])):
        print(f"  {username:<20} {len(password):^15}")


def print_empty_warning(empty_users, empty_count):
    print(f"\n*** WARNING: {empty_count} account(s) found with no password set! ***")
    print("  Accounts with blank passwords:")
    for user in empty_users:
        print(f"    - {user}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Hashcat cracked password output.")
    parser.add_argument("filename", help="Path to Hashcat output file")
    parser.add_argument("--weak", type=int, default=None, metavar="N",
                        help="Flag accounts with passwords <= N characters")
    args = parser.parse_args()

    try:
        length_counts, passwords, total, skipped, empty_count, empty_users = parse_hashcat_output(args.filename)
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        sys.exit(1)

    if total == 0:
        print("No cracked passwords found in the file.")
        sys.exit(1)

    if skipped > 0:
        print(f"Note: Skipped {skipped} unrecognized line(s).")

    print_length_table(length_counts, total)
    print_charset_table(passwords, total)

    if empty_count > 0:
        print_empty_warning(empty_users, empty_count)

    if args.weak:
        weak_accounts = []
        with open(args.filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                if len(parts) == 3:
                    username, password = parts[0], parts[2]
                elif len(parts) == 2:
                    username, password = parts[0], parts[1]
                else:
                    continue
                if password and len(password) <= args.weak:
                    weak_accounts.append((username, password))
        if weak_accounts:
            print_weak_accounts(weak_accounts, args.weak)
        else:
            print(f"\nNo accounts found with passwords <= {args.weak} characters.")

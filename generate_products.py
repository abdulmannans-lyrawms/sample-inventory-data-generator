#!/usr/bin/env python3
"""
Generate sample inventory data CSV file.

Requires Python 3.6+ (uses f-strings and pathlib).
"""

import csv
import argparse
import sys
import random
from pathlib import Path
from datetime import datetime

# Check Python version
if sys.version_info < (3, 6):
    print("Error: This script requires Python 3.6 or higher.")
    print(f"Current version: {sys.version}")
    sys.exit(1)


def generate_sku(sku_type: int, index: int, global_seed: int = None) -> str:
    """
    Generate unique SKU based on type and index.
    
    Args:
        sku_type: 0 for numeric, 1 for alphanumeric, 2 for alphanumeric with special chars
        index: Sequential index for the SKU (1-based)
        global_seed: Optional seed for random generation (for variety between runs)
    
    Returns:
        Generated unique SKU string
    """
    # Calculate which occurrence of this SKU type (1-based)
    # Row 1: type 0, occurrence 1; Row 2: type 1, occurrence 1; Row 3: type 2, occurrence 1
    occurrence = ((index - 1) // 3) + 1
    
    if sku_type == 0:
        # Type 1: Numerical SKU
        # Random number between 6 and 10 digits
        # Use occurrence + global_seed for variety between runs
        seed = (occurrence * 1000) + (global_seed or 0)
        rng = random.Random(seed)
        num_digits = rng.randint(6, 10)
        min_value = 10 ** (num_digits - 1)  # e.g., 100000 for 6 digits
        max_value = (10 ** num_digits) - 1   # e.g., 999999 for 6 digits
        return str(rng.randint(min_value, max_value))
    elif sku_type == 1:
        # Type 2: Alphanumeric SKU
        # Auto-generated 3-letter prefix + 5-digit number
        # Use occurrence + global_seed for variety between runs
        seed = (occurrence * 1000) + (global_seed or 0)
        rng = random.Random(seed)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Generate random 3-letter prefix
        prefix = ''.join(rng.choice(letters) for _ in range(3))
        
        # Generate random 5-digit number
        num_part = rng.randint(10000, 99999)
        return f"{prefix}-{num_part:05d}"
    else:
        # Type 3: Alphanumeric with special characters
        # Varied patterns with different special characters and formats
        # Use occurrence + global_seed for variety between runs
        seed = (occurrence * 1000) + (global_seed or 0)
        rng = random.Random(seed)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Generate random components with more variety
        prefix_len = rng.randint(1, 4)
        prefix = ''.join(rng.choice(letters) for _ in range(prefix_len))
        
        num1 = rng.randint(100, 9999)
        num2 = rng.randint(100, 9999)
        num3 = rng.randint(10, 999)
        num4 = rng.randint(10, 99)
        
        # Choose different pattern formats with more randomness
        pattern_type = rng.randint(0, 9)
        if pattern_type == 0:
            return f"{prefix}-{num1}-{num2}  #{rng.choice(letters)}{rng.choice(letters)}s{num3}"
        elif pattern_type == 1:
            return f"{prefix}#{num1}-{num2}-{num3}"
        elif pattern_type == 2:
            return f"{prefix}_{num1}-{num2}@{num3}"
        elif pattern_type == 3:
            return f"{prefix} - {num1} - {num2}  #{rng.choice(letters)}{rng.choice(letters)}s{num3}L{rng.randint(1,9)}"
        elif pattern_type == 4:
            return f"{prefix}-{num1}#{num2}-{num3}"
        elif pattern_type == 5:
            return f"{prefix}_{num1}_{num2}-{num3}"
        elif pattern_type == 6:
            return f"{prefix}@{num1}_{num2}#{num3}"
        elif pattern_type == 7:
            return f"{prefix}-{num1} - {num2}  #{rng.choice(letters)}{rng.choice(letters)}s{num3}"
        elif pattern_type == 8:
            return f"{prefix}#{num1}_{num2}-{num3}@{num4}"
        else:
            return f"{prefix}-{num1}_{num2}  #{rng.choice(letters)}s{num3}L{rng.randint(1,9)}"


def main() -> None:
    """
    Generate a CSV file with a customizable number of product rows.

    The file will be created as `products_generated.csv`
    in the project root directory.
    """
    parser = argparse.ArgumentParser(
        description="Generate sample inventory data file (CSV)"
    )
    parser.add_argument(
        "-n",
        "--num-entries",
        type=int,
        default=3000,
        help="Number of product entries to generate (default: 3000)",
    )
    parser.add_argument(
        "-f",
        "--fulfilmentclient",
        type=str,
        default="Stock Prop Test",
        help="Fulfilment client name (default: 'Stock Prop Test')",
    )
    parser.add_argument(
        "-s",
        "--total-stock",
        type=str,
        default="5500",
        help="Total stock value (default: '5500')",
    )
    args = parser.parse_args()

    num_rows = args.num_entries
    fulfilmentclient = args.fulfilmentclient
    total_stock = args.total_stock

    # Project root is the directory containing this script
    project_root = Path(__file__).resolve().parent
    # Generate filename with timestamp to make each run unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_output_path = project_root / f"products_generated_{timestamp}.csv"

    header = [
        "fulfilmentclient",
        "sku",
        "barcode",
        "product_name",
        "product_type",
        "product_price",
        "product_width",
        "product_height",
        "product_length",
        "product_weight",
        "product_volume",
        "product_size",
        "total_stock",
        "free_stock",
        "cycling_stock",
        "anticipation_stock",
        "backordered_stock",
        "total_inventory_value",
        "next_expiration_date",
        "stock_expiring_in_30_days",
        "expired_stock",
    ]

    base_row = [
        fulfilmentclient,  # fulfilmentclient
        "",  # sku (placeholder, will be filled)
        "",  # barcode
        "",  # product_name (placeholder, will be filled)
        "product",  # product_type
        "100",  # product_price
        "",  # product_width
        "",  # product_height
        "",  # product_length
        "0",  # product_weight
        "0",  # product_volume
        "",  # product_size
        total_stock,  # total_stock
        "1886",  # free_stock
        "2088",  # cycling_stock
        "1",  # anticipation_stock
        "202",  # backordered_stock
        "0",  # total_inventory_value
        "",  # next_expiration_date
        "0",  # stock_expiring_in_30_days
        "0",  # expired_stock
    ]

    # Generate a global seed based on timestamp for variety between runs
    global_seed = int(datetime.now().timestamp() * 1000) % 1000000
    
    # Generate all rows first
    rows = []
    seen_skus = set()  # Track SKUs to ensure uniqueness
    
    for i in range(1, num_rows + 1):
        # Cycle through the three SKU types (0, 1, 2)
        sku_type = (i - 1) % 3
        sku = generate_sku(sku_type, i, global_seed)
        
        # Ensure uniqueness - if duplicate found, append index to make it unique
        original_sku = sku
        counter = 0
        while sku in seen_skus:
            counter += 1
            if sku_type == 0:
                # For numeric, add a suffix
                sku = f"{original_sku}-{counter}"
            elif sku_type == 1:
                # For alphanumeric, modify the number
                base_sku = original_sku.split('-')[0]
                num_part = int(original_sku.split('-')[1]) + counter
                sku = f"{base_sku}-{num_part:05d}"
            else:
                # For special chars, modify the last number
                parts = original_sku.split('L')
                sku = f"{parts[0]}L{int(parts[1]) + counter}"
        
        seen_skus.add(sku)
        product_name = f"Generated Product {i:04d}"

        row = base_row.copy()
        row[1] = sku
        row[3] = product_name
        rows.append(row)

    # Create output directory if needed
    csv_output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write CSV file
    with csv_output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Generated CSV file with {num_rows} rows at: {csv_output_path}")


if __name__ == "__main__":
    main()



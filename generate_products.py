#!/usr/bin/env python3
"""
Generate sample inventory data CSV file.

Requires Python 3.6+ (uses f-strings and pathlib).
"""

import csv
import argparse
import sys
from pathlib import Path

# Check Python version
if sys.version_info < (3, 6):
    print("Error: This script requires Python 3.6 or higher.")
    print(f"Current version: {sys.version}")
    sys.exit(1)


def generate_sku(sku_type: int, index: int) -> str:
    """
    Generate unique SKU based on type and index.
    
    Args:
        sku_type: 0 for numeric, 1 for alphanumeric, 2 for alphanumeric with special chars
        index: Sequential index for the SKU (1-based)
    
    Returns:
        Generated unique SKU string
    """
    # Calculate which occurrence of this SKU type (1-based)
    # Row 1: type 0, occurrence 1; Row 2: type 1, occurrence 1; Row 3: type 2, occurrence 1
    occurrence = ((index - 1) // 3) + 1
    
    if sku_type == 0:
        # Numeric SKU: similar to 874837204
        # Start from a base number and increment uniquely for each occurrence
        base_num = 874837200
        return str(base_num + occurrence)
    elif sku_type == 1:
        # Alphanumeric SKU: similar to PHO-13081
        # Use different prefixes to ensure uniqueness
        prefixes = ["PHO", "ABC", "XYZ", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VWX"]
        prefix = prefixes[(occurrence - 1) % len(prefixes)]
        num_part = 13080 + occurrence
        return f"{prefix}-{num_part:05d}"
    else:
        # Alphanumeric with special characters: similar to F111-5665 - 410  #LFs22L1
        # Pattern: {letter}{num}-{num} - {num}  #{letters}s{num}L{num}
        prefix_chars = ["LF", "AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV", "WX", "YZ", "AA", "BB", "CC", "DD", "EE", "FF"]
        prefix = prefix_chars[(occurrence - 1) % len(prefix_chars)]
        # Use occurrence directly to ensure uniqueness
        letter = chr(65 + ((occurrence - 1) % 26))  # A-Z
        num1 = 111 + (occurrence - 1)
        num2 = 5665 + (occurrence - 1)
        num3 = 410 + (occurrence - 1)
        num4 = 22 + ((occurrence - 1) % 1000)
        last_digit = ((occurrence - 1) % 10) + 1
        return f"{letter}{num1}-{num2} - {num3}  #{prefix}s{num4:02d}L{last_digit}"


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
    csv_output_path = project_root / "products_generated.csv"

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

    # Generate all rows first
    rows = []
    seen_skus = set()  # Track SKUs to ensure uniqueness
    
    for i in range(1, num_rows + 1):
        # Cycle through the three SKU types (0, 1, 2)
        sku_type = (i - 1) % 3
        sku = generate_sku(sku_type, i)
        
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



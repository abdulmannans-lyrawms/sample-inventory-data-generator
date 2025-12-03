import csv
import argparse
from pathlib import Path


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
    args = parser.parse_args()

    num_rows = args.num_entries

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
        "Stock Prop Test",  # fulfilmentclient
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
        "5500",  # total_stock
        "1886",  # free_stock
        "2088",  # cycling_stock
        "0",  # anticipation_stock
        "202",  # backordered_stock
        "0",  # total_inventory_value
        "",  # next_expiration_date
        "0",  # stock_expiring_in_30_days
        "0",  # expired_stock
    ]

    # Generate all rows first
    rows = []
    for i in range(1, num_rows + 1):
        sku = f"GEN-SKU-{i:04d}"
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



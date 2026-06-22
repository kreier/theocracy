import os
import pandas as pd


import os
import openpyxl
import pandas as pd


def convert_to_markdown_table(input_file, output_file, link_column_text=None, date_columns=None):
    """Converts an Excel or CSV file into a Markdown table.

    Properly extracts hidden/embedded Excel hyperlinks.
    """
    file_ext = os.path.splitext(input_file)[1].lower()

    if file_ext == ".csv":
        # CSVs can't hide hyperlinks (they are always just text strings)
        df = pd.read_csv(input_file)

        # Apply standard URL text conversion for CSVs
        def make_markdown_link(cell_value):
            if isinstance(cell_value, str) and (
                cell_value.startswith("http://")
                or cell_value.startswith("https://")
            ):
                display_text = (
                    link_column_text if link_column_text else cell_value
                )
                return f"[{display_text}]({cell_value})"
            return cell_value

        df = df.map(make_markdown_link)

    elif file_ext in [".xlsx", ".xls"]:
        # Use openpyxl directly to catch the hidden hyperlink metadata
        wb = openpyxl.load_workbook(input_file, data_only=False)
        ws = wb.active  # Grabs the first sheet

        data = []
        # Loop through all rows in the Excel sheet
        for row in ws.iter_rows():
            row_data = []
            for cell in row:
                # Check if the cell has an embedded hyperlink object
                if cell.hyperlink and cell.hyperlink.target:
                    url = cell.hyperlink.target
                    # Use the cell's visible text as the anchor text
                    # (Fallback to custom text if link_column_text is provided)
                    display_text = (
                        link_column_text if link_column_text else str(cell.value)
                    )
                    row_data.append(f"[{display_text}]({url})")
                else:
                    row_data.append(cell.value)
            data.append(row_data)

        # Convert the parsed openpyxl rows into a Pandas DataFrame
        # First row becomes the header
        df = pd.DataFrame(data[1:], columns=data[0])

    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")

    # 2. Format Date Columns to YYYY-MM-DD
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")

    # 3. Clean remaining NaN/Empty values
    df = df.fillna("")

    # 4. Save to Markdown
    markdown_table = df.to_markdown(index=False)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_table)

    print(f"Successfully converted! Markdown file saved to: {output_file}")


# --- HOW TO USE IT ---
if __name__ == "__main__":
    # Convert the xlsx file to Markdown
    convert_to_markdown_table(
        input_file="../bookstudy.xlsx",
        output_file="excel_output.md",
    )    

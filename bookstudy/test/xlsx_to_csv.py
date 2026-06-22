import os
import pandas as pd


def convert_to_markdown_table(
    input_file, output_file, link_column_text="Link", date_columns=None
):
    """Converts an Excel or CSV file into a Markdown table with hyperlinks and formatted dates.

    :param input_file: Path to the .xlsx or .csv file.
    :param output_file: Path where the .md file should be saved.
    :param link_column_text: The anchor text to display for URLs.
    :param date_columns: A list of column names that contain dates (e.g.,
    ['Created Date', 'Deadline']).
    """
    # 1. Detect file type and load into a Pandas DataFrame
    file_ext = os.path.splitext(input_file)[1].lower()

    if file_ext == ".csv":
        df = pd.read_csv(input_file)
    elif file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")

    # 2. Format Date Columns to YYYY-MM-DD
    # Explicitly convert columns requested by the user (great for CSVs)
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

    # Automatically catch columns that Excel already flagged as datetime
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # .dt.strftime('%Y-%m-%d') forces the exact YYYY-MM-DD format
            df[col] = df[col].dt.strftime("%Y-%m-%d")

    # 3. Clean data: Fill NaN/Empty values with empty strings
    df = df.fillna("")

    # 4. Convert raw URLs into Markdown hyperlinks
    def make_markdown_link(cell_value):
        if isinstance(cell_value, str) and (
            cell_value.startswith("http://")
            or cell_value.startswith("https://")
        ):
            return f"[{link_column_text}]({cell_value})"
        return cell_value

    df = df.map(make_markdown_link)

    # 5. Convert the DataFrame to a Markdown Table string
    markdown_table = df.to_markdown(index=False)

    # 6. Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_table)

    print(f"Successfully converted! Markdown file saved to: {output_file}")


# --- HOW TO USE IT ---
if __name__ == "__main__":
    # Convert the test CSV file to Markdown
    convert_to_markdown_table(
        "../bookstudy.xlsx", "excel_output.md", link_column_text="Visit Site"
    )

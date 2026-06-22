import os
import pandas as pd


def convert_to_markdown_table(input_file, output_file, link_column_text="Link"):
    """Converts an Excel or CSV file into a Markdown table with active hyperlinks.

    :param input_file: Path to the .xlsx or .csv file.
    :param output_file: Path where the .md file should be saved.
    :param link_column_text: The anchor text to display instead of raw URLs
    (e.g., 'Click Here' or 'Link').
    """
    # 1. Detect file type and load into a Pandas DataFrame
    file_ext = os.path.splitext(input_file)[1].lower()

    if file_ext == ".csv":
        df = pd.read_csv(input_file)
    elif file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")

    # 2. Clean data: Fill NaN/Empty values with empty strings so they don't break
    df = df.fillna("")

    # 3. Convert raw URLs into Markdown hyperlinks
    # This checks every cell. If it's a string starting with http, it converts it.
    def make_markdown_link(cell_value):
        if isinstance(cell_value, str) and (
            cell_value.startswith("http://")
            or cell_value.startswith("https://")
        ):
            return f"[{link_column_text}]({cell_value})"
        return cell_value

    # Apply the link conversion function to the entire dataframe
    df = df.map(make_markdown_link)

    # 4. Convert the DataFrame to a Markdown Table string
    # index=False prevents pandas from adding an annoying row-number column
    markdown_table = df.to_markdown(index=False)

    # 5. Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_table)

    print(f"Successfully converted! Markdown file saved to: {output_file}")


# --- HOW TO USE IT ---
if __name__ == "__main__":
    # Convert the test CSV file to Markdown
    convert_to_markdown_table(
        "../bookstudy.xlsx", "excel_output.md", link_column_text="Visit Site"
    )

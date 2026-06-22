import io
import os
import re


def remove_class_style_from_file(path: str) -> None:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    with io.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # remove class="..." , style='...' , and unquoted variants
    cleaned = re.sub(r"\s+(class|style)\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", '', content, flags=re.IGNORECASE)

    # remove all "id" attributes
    cleaned = re.sub(r"\s+id\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", '', cleaned, flags=re.IGNORECASE)

    # remove all "width" attributes
    cleaned = re.sub(r"\s+width\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", '', cleaned, flags=re.IGNORECASE)   

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned)


if __name__ == '__main__':
    # assume bookstudy.html is in the same directory as this script
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, 'bookstudy3.html')
    remove_class_style_from_file(target)

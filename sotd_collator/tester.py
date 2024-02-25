import re


def extract_text(input_string):
    pattern = r"^([\w\s]*)+\[(\w+)\]\(https:\/\/[^)]+\)\s?([\w\s]*)"
    match = re.search(pattern, input_string)

    if match:
        # Capturing groups 1, 2, and 3 from the regex
        text_before_link = match.group(1).strip()
        link_text = match.group(2)
        text_after_link = match.group(3).strip()

        # Concatenate and return the result
        result = f"{text_before_link} {link_text} {text_after_link}"
        return result

    else:
        return None  # No match found


# Example usage
input_string = (
    "good day [today](https://somehappylink.com/link?id=12) with lots of sunshine"
)
result = extract_text(input_string)

if result:
    print(result)
else:
    print("No match found.")

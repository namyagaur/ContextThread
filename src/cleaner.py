import re

def clean_text(text):
    lines = text.splitlines()

    cleaned_lines = []
    previous_blank = False

    for line in lines:
        line = line.strip()

        if not line:
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    text = "\n".join(cleaned_lines).strip()

    # Repair line breaks inserted inside sentences.
    text = re.sub(r"(?<=[a-z])\n(?=[a-z])", " ", text)

    return text
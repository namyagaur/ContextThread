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

    return "\n".join(cleaned_lines).strip()
import html
import re


MAX_MESSAGE_LENGTH = 4000


SECTION_NAMES = {
    "1": "Service-wide Rules",
    "2": "Game Only Rules",
    "3": "Save Editing",
    "4": "Forum Rules",
    "5": "Disclaimer & Information",
}


def extract_sections(rules):
    if not rules:
        return {}

    pattern = (
        r"^##\s+§(\d+)\s*-\s*(.+?)\s*$"
    )

    matches = list(
        re.finditer(
            pattern,
            rules,
            re.MULTILINE,
        )
    )

    sections = {}

    for index, match in enumerate(matches):
        section_id = match.group(1)

        start = match.start()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(rules)

        sections[section_id] = (
            rules[start:end].strip()
        )

    return sections


def markdown_to_html(text):
    if not text:
        return ""

    text = text.replace(
        "\r\n",
        "\n",
    )

    text = text.replace(
        "\r",
        "\n",
    )

    text = html.escape(text)

    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )

    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        text,
    )

    text = re.sub(
        r"^##\s+(.+)$",
        r"<b>\1</b>",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        r"^---+$",
        "━━━━━━━━━━━━━━━━",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        r"^\*\s+",
        "• ",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        r"^-\s+",
        "• ",
        text,
        flags=re.MULTILINE,
    )

    lines = []

    for line in text.splitlines():
        lines.append(line.rstrip())

    return "\n".join(lines).strip()


def split_message(
    text,
    max_length=MAX_MESSAGE_LENGTH,
):
    if len(text) <= max_length:
        return [text]

    chunks = []
    current = ""

    paragraphs = text.split(
        "\n\n"
    )

    for paragraph in paragraphs:
        paragraph += "\n\n"

        if (
            len(current) + len(paragraph)
            <= max_length
        ):
            current += paragraph
            continue

        if current:
            chunks.append(
                current.strip()
            )

            current = ""

        while len(paragraph) > max_length:
            split_at = paragraph.rfind(
                "\n",
                0,
                max_length,
            )

            if split_at == -1:
                split_at = max_length

            chunks.append(
                paragraph[:split_at].strip()
            )

            paragraph = paragraph[
                split_at:
            ].strip()

        current = paragraph

    if current.strip():
        chunks.append(
            current.strip()
        )

    return chunks


def get_rule_section(
    rules,
    section_id,
):
    sections = extract_sections(
        rules
    )

    section = sections.get(
        str(section_id)
    )

    if section is None:
        return []

    formatted = markdown_to_html(
        section
    )

    return split_message(
        formatted
    )


def get_rule_title(section_id):
    return SECTION_NAMES.get(
        str(section_id),
        "Rules",
    )


import re
from datetime import datetime


# Words that suggest a network-related event
NETWORK_KEYWORDS = {
    "network",
    "interface",
    "connection",
    "packet",
    "monitoring",
    "router",
    "link",
    "peer",
    "carrier",
}


def is_network_event(context):
    """
    Check whether the text contains network-related keywords.
    """
    return any(
        re.search(
            r"\b" + re.escape(keyword) + r"\b",
            context,
            re.IGNORECASE
        )
        for keyword in NETWORK_KEYWORDS
    )


def get_context(lines, line_index, window=2):
    """
    Collect nearby lines around a timestamp.

    Stop at blank lines to avoid mixing separate event blocks.
    """
    context_lines = [lines[line_index]]

    # Look backward
    for i in range(
        line_index - 1,
        max(-1, line_index - window - 1),
        -1
    ):
        if not lines[i].strip():
            break

        context_lines.insert(0, lines[i])

    # Look forward
    for i in range(
        line_index + 1,
        min(len(lines), line_index + window + 1)
    ):
        if not lines[i].strip():
            break

        context_lines.append(lines[i])

    return " ".join(context_lines)


def extract_timestamps(log_text):
    """
    Extract valid timestamps associated with network events.

    Supported formats:
    - YYYY-MM-DD HH:mm:ss
    - DD/MM/YYYY HH:mm:ss
    - HH:mm:ss
    """

    patterns = [
        (
            r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S"
        ),
        (
            r"\b\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\b",
            "%d/%m/%Y %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S"
        ),
        (
            r"\b\d{2}:\d{2}:\d{2}\b",
            "%H:%M:%S",
            "%H:%M:%S"
        )
    ]

    matches = []

    # Step 1: Find and normalize timestamp 
    for pattern, input_format, output_format in patterns:
        for match in re.finditer(pattern, log_text):
            try:
                parsed = datetime.strptime(
                    match.group(),
                    input_format
                )

                normalized = parsed.strftime(output_format)

                matches.append((
                    match.start(),
                    match.end(),
                    normalized
                ))

            except ValueError:
                # Ignore invalid dates or times
                continue

    # Step 2: Prefer longer matches when timestamps overlap
    matches.sort(
        key=lambda item: (
            item[0],
            -(item[1] - item[0])
        )
    )

    selected = []

    for start, end, value in matches:
        overlaps = any(
            start < existing_end and end > existing_start
            for existing_start, existing_end, _ in selected
        )

        if not overlaps:
            selected.append((start, end, value))

    # Step 3: Preserve original log order
    selected.sort(key=lambda item: item[0])

    # Step 4: Find the context of each timestamp
    lines = log_text.splitlines(keepends=True)
    results = []

    for start, end, value in selected:

        position = 0
        line_index = 0

        # Find the line containing the timestamp
        for i, line in enumerate(lines):
            if position <= start < position + len(line):
                line_index = i
                break

            position += len(line)

        # Examine nearby lines
        context = get_context(lines, line_index, window=2)

        # Include only likely network-event timestamps
        if is_network_event(context):
            results.append(value)

    return results

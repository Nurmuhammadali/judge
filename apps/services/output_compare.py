def normalize(text: str) -> str:
    """
    Normalize output for comparison.
    - normalize newlines
    - trim trailing whitespace
    - ignore trailing empty lines
    """
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines = [line.rstrip() for line in lines]

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def is_equal(actual: str, expected: str) -> bool:
    return normalize(actual) == normalize(expected)

"""Example test: checks that parsed data is non-empty."""


def run(parsed_data):
    if not parsed_data:
        return {
            "name": "Non-empty data",
            "passed": False,
            "details": "Parsed data is empty. The file may be blank or unparseable.",
        }
    return {
        "name": "Non-empty data",
        "passed": True,
        "details": f"Data contains {len(parsed_data)} top-level keys.",
    }

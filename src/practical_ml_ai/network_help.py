"""Plain-language hints for failed dataset or model downloads."""
from urllib.error import URLError

WORKED_REPORTS = "https://ntious.github.io/ml_ai_it/examples.html"
_NETWORK_WORDS = ("urlopen error", "max retries", "connection", "tunnel", "proxy", "timed out",
                  "name or service not known", "getaddrinfo", "temporary failure in name resolution",
                  "network is unreachable", "huggingface.co", "archive.ics.uci.edu")


def is_network_error(error):
    """True when an error looks like a failed download rather than a problem with local files."""
    if isinstance(error, (URLError, ConnectionError, TimeoutError)):
        return True
    text = str(error).lower()
    return any(word in text for word in _NETWORK_WORDS)


def describe(error):
    """Return the error text, followed by a download hint when the error looks network-related."""
    if not is_network_error(error):
        return str(error)
    return (f"{error}\n\nThis step downloads a public dataset or model the first time it runs, "
            "and the download did not complete.\n"
            "Check that this computer is online and that a firewall or proxy allows "
            "archive.ics.uci.edu and huggingface.co, then run the same command again.\n"
            "If the retry says to use a fresh output directory, the failed run saved partial results: "
            "give --output (or --run) a new folder name. Keep the dataset and model caches.\n"
            "Once a download succeeds it is cached, and later runs work offline.\n"
            f"Meanwhile you can read the worked reports: {WORKED_REPORTS}")

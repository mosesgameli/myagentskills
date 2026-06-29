from mcp.server.fastmcp import FastMCP
from datetime import datetime
import pytz

mcp = FastMCP("myagentskills")

@mcp.tool()
def get_current_time(timezone: str | None = None, format_str: str = "%Y-%m-%dT%H:%M:%S%z") -> dict:
    """
    Get the current time, optionally in a specific timezone.
    
    Args:
        timezone: IAM timezone string (e.g. "America/New_York"). Optional.
        format_str: Date format string (Python strftime format). Defaults to ISO format.
    
    Returns:
        A dict with content list containing the formatted time string.
    """
    now = datetime.now()
    
    if timezone:
        tz = pytz.timezone(timezone)
        now = now.astimezone(tz)
    
    formatted_time = now.strftime(format_str)
    
    return {
        "content": [
            {"type": "text", "text": formatted_time}
        ]
    }


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

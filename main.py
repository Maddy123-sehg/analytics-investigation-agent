import os
from pathlib import Path

from analytics_agent.agent import InvestigationAgent
from analytics_agent.tools import AnalyticsTools


def load_local_env(path: Path) -> None:
    """Load simple KEY=VALUE settings without adding a dependency."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def main() -> None:
    project_dir = Path(__file__).parent
    load_local_env(project_dir / ".env")
    configured_path = Path(os.getenv("DATA_PATH", "data/sales.csv"))
    data_path = configured_path if configured_path.is_absolute() else project_dir / configured_path

    tools = AnalyticsTools(data_path)
    dates = tools.available_dates()
    if len(dates) < 2:
        raise ValueError("The dataset needs at least two dates.")

    agent = InvestigationAgent(tools)
    print(agent.investigate(current_date=dates[-1], previous_date=dates[-2]))
    print("\nAGENT TRACE")
    print("\n".join(agent.trace))


if __name__ == "__main__":
    main()

"""cost - show cost of resources matching a tag, over the last N days."""
from collections import defaultdict
from datetime import date, timedelta

import boto3

from commands._common import parse_kv


def run(args):
    """Entry point."""
    key, value = parse_kv(args.tag)
    end = date.today()
    start = end - timedelta(days=args.days)

    ce = boto3.client("ce")
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        Filter={"Tags": {"Key": key, "Values": [value]}},
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    totals = defaultdict(float)
    for result in resp.get("ResultsByTime", []):
        for group in result.get("Groups", []):
            service = group.get("Keys", ["(unknown)"])[0]
            amount = group.get("Metrics", {}).get("UnblendedCost", {}).get("Amount", "0")
            totals[service] += float(amount)

    print(
        f"Cost for {key}={value} over last {args.days} days "
        f"({start.isoformat()} -> {end.isoformat()}):"
    )
    print("-" * 60)
    grand_total = 0.0
    for service, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        grand_total += amount
        print(f"  {service:<46} $ {amount:7.2f}")
    print("-" * 60)
    print(f"  {'TOTAL':<46} $ {grand_total:7.2f}")

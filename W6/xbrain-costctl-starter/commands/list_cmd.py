"""list - list AWS resources by type, filter by tag / missing-tag."""
import boto3
from botocore.exceptions import ClientError

from commands._common import parse_kv, tags_to_dict, tags_match


def _list_ec2(want, missing):
    """List EC2 instances matching tag filters.

    Returns list of (instance_id, instance_type, state, tags_dict) tuples.
    """
    ec2 = boto3.client("ec2")
    rows = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = tags_to_dict(instance.get("Tags"))
                if tags_match(tags, want, missing):
                    rows.append(
                        (
                            instance["InstanceId"],
                            instance.get("InstanceType", ""),
                            instance.get("State", {}).get("Name", ""),
                            tags,
                        )
                    )
    return rows


def _list_rds(want, missing):
    """List RDS DB instances matching tag filters."""
    rds = boto3.client("rds")
    rows = []
    paginator = rds.get_paginator("describe_db_instances")
    for page in paginator.paginate():
        for db in page.get("DBInstances", []):
            tag_items = rds.list_tags_for_resource(
                ResourceName=db["DBInstanceArn"]
            ).get("TagList", [])
            tags = tags_to_dict(tag_items)
            if tags_match(tags, want, missing):
                rows.append(
                    (
                        db["DBInstanceIdentifier"],
                        db.get("DBInstanceClass", ""),
                        db.get("DBInstanceStatus", ""),
                        tags,
                    )
                )
    return rows


def _list_s3(want, missing):
    """List S3 buckets matching tag filters."""
    s3 = boto3.client("s3")
    rows = []
    for bucket in s3.list_buckets().get("Buckets", []):
        name = bucket["Name"]
        try:
            tag_items = s3.get_bucket_tagging(Bucket=name).get("TagSet", [])
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"NoSuchTagSet", "NoSuchTagSetError"}:
                raise
            tag_items = []
        tags = tags_to_dict(tag_items)
        if tags_match(tags, want, missing):
            rows.append((name, "bucket", "active", tags))
    return rows


def _list_volume(want, missing):
    """List EBS volumes matching tag filters."""
    ec2 = boto3.client("ec2")
    rows = []
    paginator = ec2.get_paginator("describe_volumes")
    for page in paginator.paginate():
        for volume in page.get("Volumes", []):
            tags = tags_to_dict(volume.get("Tags"))
            if tags_match(tags, want, missing):
                rows.append(
                    (
                        volume["VolumeId"],
                        f"{volume.get('VolumeType', '')}-{volume.get('Size', 0)}GB",
                        volume.get("State", ""),
                        tags,
                    )
                )
    return rows


DISPATCH = {
    "ec2": _list_ec2,
    "rds": _list_rds,
    "s3": _list_s3,
    "volume": _list_volume,
}


def run(args):
    """Entry point called by costctl.py."""
    want = [parse_kv(item) for item in args.tag]
    missing = args.missing_tag
    rows = DISPATCH[args.type](want, missing)

    filters = []
    filters.extend(f"{key}={value}" for key, value in want)
    filters.extend(f"missing:{key}" for key in missing)
    filter_text = f" {' '.join(filters)}" if filters else ""

    print(f"{args.type.upper()}{filter_text} - {len(rows)} found:")
    print("-" * 78)
    for rid, kind, state, tags in rows:
        tag_text = ", ".join(f"{key}={value}" for key, value in sorted(tags.items()))
        print(f"  {rid:<26} {kind:<14} {state:<12} {tag_text}")

"""tag - add or update tags on one resource."""
import boto3
from botocore.exceptions import ClientError

from commands._common import parse_kv


def _to_tags(set_args):
    """Convert ['k1=v1', 'k2=v2'] to [{'Key':'k1','Value':'v1'}, ...]."""
    return [{"Key": key, "Value": value} for key, value in (parse_kv(s) for s in set_args)]


def _tag_ec2(rid, tags):
    boto3.client("ec2").create_tags(Resources=[rid], Tags=tags)


def _tag_rds(rid, tags):
    rds = boto3.client("rds")
    db = rds.describe_db_instances(DBInstanceIdentifier=rid)["DBInstances"][0]
    rds.add_tags_to_resource(ResourceName=db["DBInstanceArn"], Tags=tags)


def _tag_s3(rid, tags):
    s3 = boto3.client("s3")
    try:
        existing = s3.get_bucket_tagging(Bucket=rid).get("TagSet", [])
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code not in {"NoSuchTagSet", "NoSuchTagSetError"}:
            raise
        existing = []

    merged = {item["Key"]: item["Value"] for item in existing}
    merged.update({item["Key"]: item["Value"] for item in tags})
    tag_set = [{"Key": key, "Value": value} for key, value in sorted(merged.items())]
    s3.put_bucket_tagging(Bucket=rid, Tagging={"TagSet": tag_set})


def _tag_volume(rid, tags):
    boto3.client("ec2").create_tags(Resources=[rid], Tags=tags)


DISPATCH = {
    "ec2": _tag_ec2,
    "rds": _tag_rds,
    "s3": _tag_s3,
    "volume": _tag_volume,
}


def run(args):
    """Entry point."""
    tags = _to_tags(args.set)
    DISPATCH[args.type](args.id, tags)
    tag_text = ", ".join(f"{tag['Key']}={tag['Value']}" for tag in tags)
    print(f"Applied {len(tags)} tag(s) to {args.type} {args.id}: {tag_text}")

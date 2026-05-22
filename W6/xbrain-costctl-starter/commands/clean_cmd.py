"""clean - bulk terminate resources matching a tag."""
import boto3

from commands._common import parse_kv, tags_to_dict


TERMINAL_INSTANCE_STATES = {"shutting-down", "terminated"}


def _find_targets(tag_key, tag_val):
    """Return {"ec2": [...], "volume": [...]} matching tag in deletable state."""
    ec2 = boto3.client("ec2")
    targets = {"ec2": [], "volume": []}

    instance_pages = ec2.get_paginator("describe_instances").paginate()
    for page in instance_pages:
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                state = instance.get("State", {}).get("Name", "")
                tags = tags_to_dict(instance.get("Tags"))
                if state not in TERMINAL_INSTANCE_STATES and tags.get(tag_key) == tag_val:
                    targets["ec2"].append(instance["InstanceId"])

    volume_pages = ec2.get_paginator("describe_volumes").paginate()
    for page in volume_pages:
        for volume in page.get("Volumes", []):
            tags = tags_to_dict(volume.get("Tags"))
            if volume.get("State") == "available" and tags.get(tag_key) == tag_val:
                targets["volume"].append(volume["VolumeId"])

    return targets


def run(args):
    """Entry point."""
    key, value = parse_kv(args.tag)
    targets = _find_targets(key, value)
    ec2_ids = targets["ec2"]
    volume_ids = targets["volume"]

    if not ec2_ids and not volume_ids:
        print("Nothing to clean.")
        return

    print(f"Clean plan for {key}={value}:")
    print(f"  EC2: {len(ec2_ids)}")
    for instance_id in ec2_ids:
        print(f"    {instance_id}")
    print(f"  Volumes: {len(volume_ids)}")
    for volume_id in volume_ids:
        print(f"    {volume_id}")

    if not args.apply:
        print("(dry-run - pass --apply to terminate/delete these resources)")
        return

    ec2 = boto3.client("ec2")
    if ec2_ids:
        ec2.terminate_instances(InstanceIds=ec2_ids)
        for instance_id in ec2_ids:
            print(f"Terminated EC2 {instance_id}")
    for volume_id in volume_ids:
        ec2.delete_volume(VolumeId=volume_id)
        print(f"Deleted volume {volume_id}")

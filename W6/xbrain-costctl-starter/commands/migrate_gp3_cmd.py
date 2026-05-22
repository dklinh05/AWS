"""migrate-gp3 - plan or apply gp2 to gp3 EBS migration."""
import boto3

GP2_PRICE = 0.10
GP3_PRICE = 0.08


def _attached_instance(volume):
    attachments = volume.get("Attachments", [])
    if not attachments:
        return "(none)"
    return attachments[0].get("InstanceId", "(unknown)")


def run(args):
    """Entry point."""
    ec2 = boto3.client("ec2")
    filters = [{"Name": "volume-type", "Values": ["gp2"]}]
    if args.volume_id:
        filters.append({"Name": "volume-id", "Values": [args.volume_id]})

    volumes = []
    paginator = ec2.get_paginator("describe_volumes")
    for page in paginator.paginate(Filters=filters):
        volumes.extend(page.get("Volumes", []))

    if not volumes:
        print("No gp2 volumes found.")
        return

    if not args.apply:
        price_delta = GP2_PRICE - GP3_PRICE
        total = 0.0
        print(f"gp2 volumes (price delta ${price_delta:0.3f}/GB-month):")
        print("-" * 78)
        for volume in volumes:
            size = volume["Size"]
            savings = size * price_delta
            total += savings
            print(
                f"  {volume['VolumeId']:<24} {size:>5}GB  "
                f"attached={_attached_instance(volume):<18} ${savings:0.2f}/mo savings"
            )
        print("-" * 78)
        print(f"  TOTAL projected savings: ${total:0.2f}/mo")
        print()
        print(
            "(dry-run - pass --apply --volume-id <id> to migrate one, "
            "or --apply to migrate ALL)"
        )
        return

    for volume in volumes:
        ec2.modify_volume(
            VolumeId=volume["VolumeId"],
            VolumeType="gp3",
            Iops=3000,
            Throughput=125,
        )
        print(
            f"  -> modify_volume issued for {volume['VolumeId']} "
            "(gp3, 3000 IOPS, 125 MiB/s)"
        )
    print()
    print("Volume(s) entering 'modifying' -> 'optimizing' state. App stays online.")
    print("Use `costctl list volume` after ~30 minutes to confirm 'in-use' + gp3.")

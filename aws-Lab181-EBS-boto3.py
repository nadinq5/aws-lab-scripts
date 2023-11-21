# Created an EBS volume.  
# Attached and mounted an EBS volume to an EC2 instance.  
# Created a snapshot of an EBS volume.  
# Created an EBS volume from a snapshot.

#!/usr/bin/python3
import boto3
import time

# Define the EC2 and EBS clients
ec2_client = boto3.client('ec2', region_name='us-west-2')
ebs_client = boto3.client('ec2', region_name='us-west-2')

################## Task 1: Creating a new EBS volume ##################
availability_zone = 'us-west-2a'
volume_type = 'gp2'
volume_size = 1
volume_name = 'My Volume'

response = ebs_client.create_volume(
    AvailabilityZone=availability_zone,
    VolumeType=volume_type,
    Size=volume_size,
)

volume_id = response['VolumeId']

# Add a tag to the volume
ebs_client.create_tags(
    Resources=[volume_id],
    Tags=[{'Key': 'Name', 'Value': volume_name}]
)

# Wait for the volume to be available
waiter = ebs_client.get_waiter('volume_available')
waiter.wait(VolumeIds=[volume_id])

print(f"Volume {volume_id} created successfully.")

################## Task 2: Attaching the volume to an EC2 instance ##################
instance_id = 'i-05e3cf4586ea73e8b'  # Replace with the actual instance ID

ebs_client.attach_volume(
    VolumeId=volume_id,
    InstanceId=instance_id,
    Device='/dev/sdf'  # The device name should match the one mentioned in the instructions
)

# Wait for the volume to be attached
waiter = ebs_client.get_waiter('volume_in_use')
waiter.wait(VolumeIds=[volume_id])

print(f"Volume {volume_id} attached to instance {instance_id} successfully.")

################## Task 3: Connecting to the Lab EC2 instance ##################
# Follow the manual steps in the instructions to connect to the EC2 instance.

################## Task 4: Creating and configuring the file system ##################
# Connect to the EC2 instance using an SSH client or EC2 Instance Connect to execute the following commands:
# df -h
# sudo mkfs -t ext3 /dev/sdf
# sudo mkdir /mnt/data-store
# sudo mount /dev/sdf /mnt/data-store
# echo "/dev/sdf   /mnt/data-store ext3 defaults,noatime 1 2" | sudo tee -a /etc/fstab
# cat /etc/fstab
# df -h
# sudo sh -c "echo some text has been written > /mnt/data-store/file.txt"
# cat /mnt/data-store/file.txt

################## Task 5: Creating an Amazon EBS snapshot ##################
# Execute the following commands on the EC2 instance:
# sudo rm /mnt/data-store/file.txt
# ls /mnt/data-store/file.txt

# Create a snapshot using Boto3
snapshot_name = 'My Snapshot'

response = ebs_client.create_snapshot(
    VolumeId=volume_id,
    TagSpecifications=[{'ResourceType': 'snapshot', 'Tags': [{'Key': 'Name', 'Value': snapshot_name}]}]
)

snapshot_id = response['SnapshotId']

# Wait for the snapshot to be completed
waiter = ebs_client.get_waiter('snapshot_completed')
waiter.wait(SnapshotIds=[snapshot_id])

print(f"Snapshot {snapshot_id} created successfully.")

################## Task 6: Restoring the Amazon EBS snapshot ##################
################## Task 6.1: Creating a volume by using the snapshot
# Replace 'your_region' with your AWS region
region_name = 'us-west-2'

# Create an EBS client
ebs_client = boto3.client('ec2', region_name=region_name)

# Replace 'your_snapshot_id' with the actual EBS snapshot ID
snapshot_id = 'snap-07dfb096309048014'

# Replace 'your_availability_zone' with the desired Availability Zone
availability_zone = 'us-west-2a'

restored_volume_name = 'Restored Volume'

# Create a new volume from the snapshot
response = ebs_client.create_volume(
    SnapshotId=snapshot_id,
    AvailabilityZone=availability_zone,
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {'Key': 'Name', 'Value': restored_volume_name}
            ]
        }
    ]
)

restored_volume_id = response['VolumeId']

print(f"Restored Volume {restored_volume_id} created successfully.")

# Wait for the volume to be available
waiter = ebs_client.get_waiter('volume_available')
waiter.wait(VolumeIds=[restored_volume_id])

print(f"Restored Volume {restored_volume_id} is now available.")

# Task 6.2: Attaching the restored volume to the EC2 instance
# Replace 'your_instance_id' with the actual instance ID
instance_id = 'i-05e3cf4586ea73e8b'

# Replace 'your_device_name' with the desired device name
device_name = '/dev/sdg'

# Attach the restored volume to the instance
ebs_client.attach_volume(


# Task 6.3: Mounting the restored volume
# Execute the following commands on the EC2 instance:
# sudo mkdir /mnt/data-store2
# sudo mount /dev/sdg /mnt/data-store2
# ls /mnt/data-store2/file.txt
# We should see the file.txt file.


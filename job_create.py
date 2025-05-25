"""
job_create.py

This script creates an OCI Data Science Job with a container runtime.
It configures the compartment, project, compute shape, logging, and
Object Storage mount, then submits the job definition.

Usage:
    - Fill in all `<YOUR_…>` placeholders below.
    - Run: python create_datascience_job.py
"""

from ads.jobs import Job, DataScienceJob, ContainerRuntime

# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

# Replace with your OCI Compartment OCID
COMPARTMENT_OCID = "<YOUR_COMPARTMENT_OCID>"

# Replace with your OCI Data Science Project OCID
PROJECT_OCID     = "<YOUR_PROJECT_OCID>"

# Replace with your OCI Container Registry image URL (e.g. fra.ocir.io/<TENANCY>/<REPO>:<TAG>)
IMAGE_URL        = "<YOUR_IMAGE_URL>"

# Compute shape settings
VM_SHAPE         = "<YOUR_VM_SHAPE>"      # e.g. "VM.Standard.E5.Flex"
OCPUS            = "<YOUR_NUMBER_OF_OCPUS>" # e.g. 1
MEMORY_GB        = "<YOUR_MEMORY_IN_GBS>"   # e.g. 4

# Network settings
SUBNET_OCID      = "<YOUR_SUBNET_OCID>"   # If mounting to a private subnet; leave blank for default

# Logging settings
LOG_GROUP_OCID   = "<YOUR_LOG_GROUP_OCID>"
LOG_OCID         = "<YOUR_LOG_OCID>"

# Job and storage settings
JOB_NAME         = "<YOUR_JOB_NAME>"
BUCKET           = "<YOUR_BUCKET_NAME>"
NAMESPACE        = "<YOUR_NAMESPACE>"

# ---------------------------------------
# BUILD INFRASTRUCTURE
# ---------------------------------------

infrastructure = (
    DataScienceJob()
    .with_compartment_id(COMPARTMENT_OCID)            # compartment for the Job
    .with_project_id(PROJECT_OCID)                    # Data Science project
    .with_shape_name(VM_SHAPE)                        # VM shape for compute
    .with_shape_config_details(memory_in_gbs=MEMORY_GB, ocpus=OCPUS)
    .with_block_storage_size(50)                      # GB of block storage
    .with_log_group_id(LOG_GROUP_OCID)                # log group for diagnostics
    .with_log_id(LOG_OCID)                            # specific log for the Job
    .with_storage_mount({
        "src": f"oci://{BUCKET}@{NAMESPACE}/",        # source Object Storage URI
        "dest": "objects"                             # mounts at /mnt/objects in the container
    })
)

# ---------------------------------------
# BUILD RUNTIME
# ---------------------------------------

runtime = (
    ContainerRuntime()
    .with_image(IMAGE_URL)                            # container image to run
)

# ---------------------------------------
# CREATE AND REGISTER JOB
# ---------------------------------------

job = (
    Job(name=JOB_NAME)                                # name of the Data Science Job
    .with_infrastructure(infrastructure)              # attach compute & storage settings
    .with_runtime(runtime)                            # attach container runtime
)

# Submit the job definition to OCI
job.create()

# Print the new Job OCID for reference
print(f"Job created. Job OCID: {job.id}")

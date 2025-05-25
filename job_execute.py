"""
job_execute.py

This script submits a series of OCI Data Science JobRun requests in batches.
For each batch, it passes the bucket, namespace, prefix, start index, and limit
to the container via environment variables, then submits the job and prints
its OCID.

Usage:
    - Fill in YOUR_JOB_OCID, YOUR_BUCKET_NAME, and YOUR_BUCKET_NAMESPACE.
    - Adjust batch_size and total_files as needed.
    - Run: python batch_run_jobs.py
"""

from ads.jobs import DataScienceJob

# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

# Replace with your OCI Data Science Job OCID (created via job_create.py)
job = DataScienceJob.from_id("<YOUR_JOB_OCID>")

# Object Storage parameters
bucket = "<YOUR_BUCKET_NAME>"         # The bucket where input files live
namespace = "<YOUR_BUCKET_NAMESPACE>" # Your tenancy’s Object Storage namespace
prefix = ""                           # Optional: a prefix/path under the bucket

# How many files to process per JobRun
batch_size = 1

# Total number of files you intend to process
total_files = 6

# ---------------------------------------
# BATCH SUBMISSION LOOP
# ---------------------------------------
for start in range(0, total_files, batch_size):
    # Prepare environment variables for the container
    env_overrides = {
        "BUCKET":    bucket,        # container will read INPUT bucket name
        "NAMESPACE": namespace,     # container will read namespace
        "PREFIX":    prefix,        # container will filter by this prefix
        "START":     str(start),    # start index of this batch
        "LIMIT":     str(batch_size) # number of files to process in this batch
    }
    
    print(f"Running batch for objects {start} to {start + batch_size - 1}")
    
    # Submit a JobRun with our environment overrides
    run = job.run(env_var=env_overrides)
    
    # If you want to stream logs in real time, uncomment:
    # run.watch()

    # Confirm submission and print the JobRun OCID
    print(f"Submitted JobRun {run.id} for batch {start}–{start + batch_size - 1}")

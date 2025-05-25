# OCI Data Science BYOC Jobs Example

This repository provides an example of using Oracle Cloud Infrastructure (OCI) Data Science Platform with Bring Your Own Container (BYOC) for batch processing jobs. The sample Dockerfile, Python scripts, and job definitions demonstrate how to package and run custom workloads as OCI Data Science Jobs.

## Repository Structure

```text
├── Dockerfile               # Base + file-size-checker stages for BYOC
├── app/
│   └── process_batch.py     # Example script to process files in Object Storage
├── create_job.py            # Script to create OCI Data Science Job definition
├── batch_run_jobs.py        # Script to submit multiple JobRuns in batches
└── README.md                # This documentation
```

## Prerequisites

* An OCI tenancy with Data Science service enabled
* OCI CLI installed and configured with a user who has Data Science and Object Storage permissions
* Python 3.12 (for local testing)
* Docker (for building the container image)

## Setup

1. **Build and push your container image**

   ```bash
   docker build -t <YOUR_REGISTRY>/<REPO>:<TAG> .
   docker push <YOUR_REGISTRY>/<REPO>:<TAG>
   ```

2. **Populate configuration**

   * Copy `create_job.py` and `batch_run_jobs.py` to your workspace.
   * Replace all `<YOUR_...>` placeholders with your OCIDs, namespace, bucket, and image URL.

3. **Create the OCI Data Science Job**

   ```bash
   python job_create.py
   ```

   This will print the OCID of the newly created Job definition.

4. **Submit batch runs**

   ```bash
   python job_execute.py
   ```

   This script submits JobRuns in batches, processing files from your Object Storage bucket.

## process\_batch.py

The `process_batch.py` script reads environment variables set by the JobRun, lists objects in Object Storage, and performs file-size checks (or any custom logic you define).

## Customization

* Modify the `prefix`, `batch_size`, and `total_files` in `batch_run_jobs.py` for your workload.
* Extend `process_batch.py` with your data processing logic.
* Adjust the compute shape, block storage, and logging settings in `create_job.py` as needed.

## Cleanup

To delete the Job definition once you're done:

```bash
oci data-science job delete --job-id <JOB_OCID>
```

---

Disclaimer: Use of the code in this repository is at your own responsibility only.

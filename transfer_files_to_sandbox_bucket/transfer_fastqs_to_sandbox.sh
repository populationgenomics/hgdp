#!/bin/bash

set -ex

# copy subset of hgdp fastq's to sandbox bucket
cat transfer_files_to_sandbox_bucket/list_of_hgdb_fastqs.txt | gsutil -m cp -I gs://cpg-sandbox-main-upload/

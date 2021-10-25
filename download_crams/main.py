#!/usr/bin/env python3

"""Copies HGDP CRAMs from EBI's FTP server."""

import csv
import gzip
import os
import hailtop.batch as hb
from analysis_runner import output_path

GCLOUD_AUTH = 'gcloud -q auth activate-service-account --key-file=/gsa-key/key.json'
ACCESS_LEVEL = os.getenv('ACCESS_LEVEL')


def main():
    """Main entry point."""
    service_backend = hb.ServiceBackend(
        billing_project=os.getenv('HAIL_BILLING_PROJECT'),
        bucket=os.getenv('HAIL_BUCKET'),
    )

    batch = hb.Batch(name='HGDP CRAMs download', backend=service_backend)

    with gzip.open('hgdp_sample_metadata.tsv.gz', mode='rt') as metadata_file:
        reader = csv.DictReader(metadata_file, delimiter='\t')
        file_count = 0
        for row in reader:
            url = row['url']
            if not url.endswith('.cram'):
                continue

            job = batch.new_job(name=url)
            job.image('ibmcom/aspera-cli:3.9')
            job.command(GCLOUD_AUTH)
            path_components = url.split('/')
            path = '/'.join(path_components[3:])  # Remove the ftp://host/ prefix.
            # Unfortunately, piping to stdout doesn't seem to work with ascp, so we
            # write locally first and then delocalize using Hail Batch.
            job.command(
                f'ascp -i /home/aspera/.aspera/cli/etc/asperaweb_id_dsa.openssh '
                f'-Tr -Q -l 100M -P33001 -L- '
                f'fasp-g1k@fasp.1000genomes.ebi.ac.uk:{path} {job.ofile}'
            )
            batch.write_output(job.ofile, output_path(path_components[-1]))
            job.cpu(0.25)  # Network bandwidth is the bottleneck, not CPU.

            file_count += 1
            if file_count > 5 and ACCESS_LEVEL == 'test':
                break  # Only copy a subset of CRAMs for 'test'.

    batch.run(wait=False)


if __name__ == '__main__':
    main()

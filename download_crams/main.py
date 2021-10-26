#!/usr/bin/env python3

"""Copies HGDP CRAMs from EBI's FTP server."""

import csv
import gzip
import os
import click
import hailtop.batch as hb
from analysis_runner import output_path

DOCKER_IMAGE = 'australia-southeast1-docker.pkg.dev/cpg-common/images/aspera:v1'
GCLOUD_AUTH = 'gcloud -q auth activate-service-account --key-file=/gsa-key/key.json'


@click.command()
# The range [index_begin, index_end) can be used to download a batch of samples.
@click.option(
    '--index_begin', help='Inclusive first sample index', required=True, type=int
)
@click.option(
    '--index_end', help='Exclusive last sample index ', required=True, type=int
)
def main(index_begin: int, index_end: int) -> None:
    """Main entry point."""
    service_backend = hb.ServiceBackend(
        billing_project=os.getenv('HAIL_BILLING_PROJECT'),
        bucket=os.getenv('HAIL_BUCKET'),
    )

    batch = hb.Batch(name='HGDP CRAMs download', backend=service_backend)

    jobs = []
    with gzip.open('hgdp_sample_metadata.tsv.gz', mode='rt') as metadata_file:
        reader = csv.DictReader(metadata_file, delimiter='\t')
        sample_index = 0
        for row in reader:
            url = row['url']
            if not url.endswith('.cram'):
                continue

            included = index_begin <= sample_index < index_end
            sample_index += 1
            if not included:
                continue

            path_components = url.split('/')
            path = '/'.join(path_components[3:])  # Remove the ftp://host/ prefix.
            filename = path_components[-1]

            job = batch.new_job(name=filename)
            job.image(DOCKER_IMAGE)
            job.command(GCLOUD_AUTH)
            # Unfortunately, piping to stdout doesn't seem to work with ascp, so we
            # write locally first and then copy the file.
            output = output_path(path_components[-1])
            job.command(
                # Print output file size in the background.
                f'(while true; do sleep 60; du -sh {job.ofile}*; echo; done) & '
                # We check the destination first, to make sure we're not doing redundant
                # work. That's why we can't use Hail Batch's built-in file
                # delocalization.
                f'if gsutil stat {output}; then '
                f'echo "{output} already exists"; else '
                f'/home/aspera/.aspera/connect/bin/ascp '
                f'-i /home/aspera/.aspera/connect/etc/asperaweb_id_dsa.openssh '
                f'-Tr -Q -l 1000M -P33001 -L- '
                f'fasp-g1k@fasp.1000genomes.ebi.ac.uk:{path} {job.ofile} && '
                # Transfer to GCS.
                f'gsutil cp {job.ofile} {output}; fi'
            )
            job.cpu(1)  # Network bandwidth is the bottleneck, not CPU.
            job.memory('standard')  # Use the standing worker cores.
            job.storage('50Gi')

            jobs.append(job)

    # Multiple concurrent downloads from the same IP don't seem to work well,
    # therefore add job sequencing.
    for index in range(1, index_end):
        jobs[index].depends_on(jobs[index - 1])

    batch.run(wait=False)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

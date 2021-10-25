#!/usr/bin/env python3

"""Copies HGDP CRAMs from EBI's FTP server."""

import csv
import gzip
import os
import click
import hailtop.batch as hb
from analysis_runner import output_path

DOCKER_IMAGE = 'australia-southeast1-docker.pkg.dev/cpg-common/images/aspera:v1'
ACCESS_LEVEL = os.getenv('ACCESS_LEVEL')


@click.command()
# The range [index_begin, index_end) can be used to download a batch of samples.
@click.option('--index_begin', help='Inclusive first sample index', required=True)
@click.option('--index_end', help='Exclusive last sample index ', required=True)
def main(index_begin: int, index_end: int) -> None:
    """Main entry point."""
    service_backend = hb.ServiceBackend(
        billing_project=os.getenv('HAIL_BILLING_PROJECT'),
        bucket=os.getenv('HAIL_BUCKET'),
    )

    batch = hb.Batch(name='HGDP CRAMs download', backend=service_backend)

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
            # Unfortunately, piping to stdout doesn't seem to work with ascp, so we
            # write locally first and then delocalize using Hail Batch.
            job.command(
                f'/home/aspera/.aspera/connect/bin/ascp '
                f'-i /home/aspera/.aspera/connect/etc/asperaweb_id_dsa.openssh '
                f'-Tr -Q -l 100M -P33001 -L- '
                f'fasp-g1k@fasp.1000genomes.ebi.ac.uk:{path} {job.ofile}'
            )
            batch.write_output(job.ofile, output_path(path_components[-1]))
            job.cpu(0.25)  # Network bandwidth is the bottleneck, not CPU.
            job.memory('standard')  # lowmem leads to OOMs.
            job.storage('50Gi')

    batch.run(wait=False)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

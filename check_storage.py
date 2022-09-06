#!/usr/bin/env python3

from cpg_utils.workflows.batch import get_batch
from cpg_utils.hail_batch import authenticate_cloud_credentials_in_job

b = get_batch('Check HGDP storage')
j = b.new_job('Check HGDP storage')
j.image('hail')
authenticate_cloud_credentials_in_job(j)
j.command('gsutil du -sh gs://cpg-hgdp-main/gvcf/')
j.command('gsutil du -sh gs://cpg-hgdp-main/cram/')
j.command('gsutil du -sh gs://cpg-hgdp-main/mt/oceania.mt')
j.command('gsutil du -sh gs://cpg-hgdp-main/mt/oceania_eur.mt')
b.run()

#!/usr/bin/env python3

from cpg_utils.workflows.batch import get_batch
from cpg_utils.hail_batch import authenticate_cloud_credentials_in_job, image_path, dataset_path

b = get_batch('Check HGDP storage')
j = b.new_job('Check HGDP storage')
j.image(image_path('hail'))
authenticate_cloud_credentials_in_job(j)
j.command(f'gsutil du -sh {dataset_path('gvcf')}')
j.command(f'gsutil du -sh {dataset_path('cram')}')
j.command(f'gsutil du -sh {dataset_path('mt/oceania.mt')}')
j.command(f'gsutil du -sh {dataset_path('mt/oceania_eur.mt')}')
b.run()

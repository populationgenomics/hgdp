# Download HGDP CRAMs from the EBI FTP server

The FTP server access [requires the Aspera software](https://www.internationalgenome.org/category/ftp/). Unfortunately, the `ibmcom/aspera-cli` Docker image isn't compatible with Hail Batch's file localization paths.

First, build the Docker image:

```sh
gcloud config set project cpg-common
gcloud builds submit --tag=australia-southeast1-docker.pkg.dev/cpg-common/images/aspera:v1 .
```

Then run the Hail Batch pipeline that uses the image:

```sh
analysis-runner --dataset hgdp --access-level test --output-dir cram/ebi --description "Copy HGDP CRAMs from EBI FTP" main.py --index_begin=0 --index_end=8
```

In order to restrict the bandwidth requirements on the FTP server, the `index_begin` and `index_end` parameters can be used to only download a particular batch of samples at a time.

# Genomic-API-lambda
Query VCF's or Tabix-indexed files using AWS Lambda

# Run python docker image to install cyvcf2
# Cd to bcftools function
docker run -v "$PWD":/var/task -it lambci/lambda:build bash
export share=/var/task
easy_install pip
pip install -t $share cyvcf2
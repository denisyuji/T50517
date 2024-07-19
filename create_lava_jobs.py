import subprocess
import json
import os
import secrets
from time import sleep

# Read the credentials
with open('credentials.json', 'r') as file:
    credentials = json.load(file)

filestack_key = credentials['filestack']
lava_token = credentials['lava']

# Read the params
with open('decoder-params.json', 'r') as file:
    data = json.load(file)

# Iterate through the jobs
for job in data['tests']:
    testname = job['name']
    testsuite = job['testsuite']
    decoders = job['decoders']
    platforms = job['platforms']

    # Create files for all combinations of decoders and platforms
    for decoder in decoders:
        for platform in platforms:
            job_name=f"{platform}-{testname}-{testsuite}-{decoder}"
            job_desc_file = f"lava-jobs/{job_name}.yaml"
            log_file = f"{platform}-{testname}"
            node_id = secrets.token_hex(12)  # 12 bytes = 24 hex digits

            subprocess.run(['cp', 'template.yaml', job_desc_file])
            subprocess.run(['sed', '-i', f's/JOB-NAME/{job_name}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/DEVICE-NAME/{platform}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/NODE-ID/{node_id}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/TESTSUITE/{testsuite}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/DECODERS/{decoder}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/FILESTACK-API-KEY/{filestack_key}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/DEVICE-NAME/{platform}/g', job_desc_file])
            subprocess.run(['sed', '-i', f's/TEST-NAME/{testname}/g', job_desc_file])
            result = subprocess.run(['lavacli','--uri',f'https://denis.shimizu:{lava_token}@lava.collabora.dev/RPC2/','jobs','submit',f'{job_desc_file}'], capture_output=True, text=True)
            job_id = result.stdout
            print(f"Job {job_name} submitted with ID {job_id}")

print("Files created successfully.") 

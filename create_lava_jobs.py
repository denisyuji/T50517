import subprocess
import json
import os
import secrets

# Read the JSON file
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
            job_name=f"{testname}-{testsuite}-{decoder}-{platform}"
            file_name = f"lava-jobs/{job_name}.txt"
            node_id = secrets.token_hex(12)  # 12 bytes = 24 hex digits

            subprocess.run(['cp', 'template.yaml', file_name])
            subprocess.run(['sed', '-i', f's/JOB-NAME/{job_name}/g', file_name])
            subprocess.run(['sed', '-i', f's/DEVICE-NAME/{platform}/g', file_name])
            subprocess.run(['sed', '-i', f's/NODE-ID/{node_id}/g', file_name])
            subprocess.run(['sed', '-i', f's/TESTSUITE/{testsuite}/g', file_name])
            subprocess.run(['sed', '-i', f's/DECODERS/{decoder}/g', file_name])

print("Files created successfully.") 

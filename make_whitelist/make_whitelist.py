date = '250129'
sample_ids_path = '/mnt/project/sample_metadata/ukb20279/sample_ids.txt'
withdrawn_ids_path = '/mnt/project/sample_metadata/ukb20279/w86805_20241217_withdrawn_samples_application_86805.csv'

with open(sample_ids_path, "r") as f:
    sample_ids = [line.strip() for line in f]
    
with open(withdrawn_ids_path, "r") as f:
    withdrawn_ids = [line.strip() for line in f]
    
filtered_sample_ids = [x for x in sample_ids if (x[0]!='W' and x not in withdrawn_ids)]

with open(f'{date}_whitelist.txt', 'w') as f:
    f.write('\n'.join(str(sample_id) for sample_id in filtered_sample_ids))
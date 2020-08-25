import os
import re


pattern = re.compile('".*?[SsNnAaPpHhOoTt]+?=t[0-9]+?\\.[IiNnFf]+?.*?"')
actions = [f for f in os.listdir() if f.endswith('.c') and f != 'pre_cci.c']

for action in actions:
    with open(action, 'r', encoding='utf-8') as f:
        action_new = ''
        snapshot_id = 10
        for line in f:
            if 'snapshot' in line.lower():
                snapshot = pattern.search(line).group()
                line = line.replace(snapshot, f'"Snapshot=t{snapshot_id}.inf"')
                snapshot_id += 10
            action_new += line
    with open(action, 'w') as f:
        f.write(action_new)

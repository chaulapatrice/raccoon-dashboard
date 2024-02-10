from dagster import asset, Failure
import os
from pathlib import Path

assets_path = Path(os.path.abspath(__file__))
# Go back 2 levels up to the base directory
base_path  = assets_path.parent.parent

@asset
def load_upcoming_launches(context):
    dlt_dir = base_path / 'dlt'
    exit_code = os.system(f'cd {dlt_dir} && python3 load_upcoming_launches.py')

    if os.waitstatus_to_exitcode(exit_code) != 0:
        raise Failure("Failed to load upcoming launches from Launch 2 API")
    
    return True

@asset
def create_data_mart(load_upcoming_launches):
    dbt_dir = base_path / 'dbt_upcoming_launches'
    exit_code = os.system(f'cd {dbt_dir} && dbt run')

    if os.waitstatus_to_exitcode(exit_code) != 0:
        raise Failure("Failed to create data mart")
    
    return True

@asset
def update_evidence_sources(create_data_mart):
    evidence_dir = base_path / 'evidence'
    exit_code = os.system(f'cd {evidence_dir} && npm install && npm run sources')

    if os.waitstatus_to_exitcode(exit_code) != 0:
        raise Failure("Failed to update evidence sources")
    
    return True
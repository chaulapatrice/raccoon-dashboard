from dagster import define_asset_job, ScheduleDefinition, repository

asset_job = define_asset_job("asset_job", "*")

five_minute_schedule = ScheduleDefinition(job=asset_job, cron_schedule='*/5 * * * *')
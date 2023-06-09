# deployment.py
# (ACTS AS A YAML FILE)

from scripts.bash_task import MakeFlow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import RRuleSchedule
from scripts.schedule_converter import ScheduleConverter
from scripts.parse_xml import ParseXML

def DeployFlow(schedule_file_name, plan_name, plan_file):
    deployment = Deployment.build_from_flow(
        flow=MakeFlow(plan_file, plan_name),
        name="PROD",
        parameters={'name': "Lars"},
        infra_overrides={
            "env": {"PREFECT_LOGGING_LEVEL": "DEBUG"}
        },
        work_pool_name='uc4_test',
        work_queue_name=ParseXML.GetQueueName(plan_file),
        schedule=(RRuleSchedule(rrule=ScheduleConverter(schedule_file_name, plan_name), timezone="Europe/Brussels"))
    )
    deployment.apply()

if __name__ == "__main__":
    DeployFlow()
    print("Succesfully deployed!")
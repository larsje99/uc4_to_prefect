import subprocess
import os
import sys
import prefect
from prefect import flow, task, get_run_logger
import time
from datetime import datetime
from scripts.parse_xml import ParseXML

plan = "P.HDPAWS.MASTER_SKIPI.D.90000"

def MakeFlow(plan_file, plan_name):
    for job in ParseXML.PlaceJobsInList(plan_file, plan_name):
        if  job == "START":
            @task(task_run_name="START",
                name="START")
            def Start():
                logger = get_run_logger()
                logger.info("TASK SUCCESFULLY STARTED!")
        
        if job == "END":
            @task(task_run_name="END",
                name="END")
            def End():
                logger = get_run_logger()
                logger.info("TASK SUCCESFULLY ENDED!")
        
        else:
            @task(task_run_name=job,
                name=job)
            def RunBash():
                # Command to execute
                command = ParseXML.GetBashCommand(plan_file, job)

                # Execute the command
                subprocess.call(command, shell=True)
                
                logger = get_run_logger()
                logger.info("Succesfully executed!")

    @flow(name=plan_name,
        description="ENTER DESCRIPTION HERE")
    def test_flow(name: str):
        task_start = Start()
        task_1 = RunBash()
        task_end = End()

    return test_flow

if __name__ == "__main__":
    name = sys.argv[0]
    MakeFlow(name)
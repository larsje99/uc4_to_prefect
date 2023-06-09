from deployment import DeployFlow
from scripts.parse_xml import ParseXML

plan_file = input("Please enter XML file name where the plan located: ")
plan_name = input("Please enter the name of the plan you want to convert: ")
schedule_file_name = input("Please enter XML file name where the schedule is located: ")

DeployFlow(schedule_file_name, plan_name, plan_file)

print("Job succesfully deployed!")
import xml.etree.cElementTree as et

# ////FYI////
# # DAY CONFIGURATION IN XML
# mondaxml = "EV_MONDAY"
# tuesday_xml = "EV_THUESDAY"
# wednesday_xml = "EV_WEDNESDAY"
# thursday_xml = "EV_THURSDAY"
# friday_xml = "EV_FRIDAY"
# saturday_xml = "EV_SATURDAY"
# sunday_xml = "EV_SUNDAY"

# # DAY CONFIGURATION IN RRULE
# monday_rrule = "MO"
# tuesday_rrule = "TU"
# wednesday_rrule = "WE"
# thursday_rrule = "TH"
# friday_rrule = "FR"
# saturday_rrule = "SA"
# sunday_rrule = "SU"

def ScheduleConverter(schedule_file_name, plan_name):
    tree=et.parse('uc4/schedules/' + schedule_file_name + '.xml')
    root=tree.getroot()

    for task in root.iter('task'):

        # FIND ALL THE NECESSARY TAGS + SLICE HOUR AND MINUTES
        if task.get('Object') == plan_name:
            name_list = task.get('Object')
            after_tag = task.find('after')
            erlst_st_time = after_tag.get('ErlstStTime')
            hour = erlst_st_time[0:2]
            minutes = erlst_st_time[3:5]
            
            # WHEN JOB IS CONTINUE
            if ".C." in name_list:
                for task in root.iter('task'):
                    if task.get('Object') == plan_name:
                        rrule = 'FREQ=DAILY;BYHOUR=' + hour + ';BYMINUTE=' + minutes + ';BYSECOND=0'
                        return rrule

            # WHEN JOB IS EXECUTED DAILY
            if ".D." in name_list:
                for task in root.iter('task'):
                    if task.get('Object') == plan_name:
                        rrule = 'FREQ=DAILY;BYHOUR=' + hour + ';BYMINUTE=' + minutes + ';BYSECOND=0'
                        return rrule

            #WHEN JOB IS EXECUTED WEEKLY        
            if ".W." in name_list:
                for task in root.iter('task'):
                    if task.get('Object') == plan_name:
                        cale_tag = task.find('calendars/cale')
                        cale_key_name = cale_tag.get('CaleKeyName')
                        if cale_key_name[3:] == "THUESDAY":
                            weekday = "TU"
                        else:
                            weekday = cale_key_name[3:5]
                        rrule = 'FREQ=WEEKLY;BYWEEKDAY=' + weekday + ';BYHOUR=' + hour + ';BYMINUTE=' + minutes + ';BYSECOND=0'
                        return rrule

            # WHEN JOB IS EXECUTED MONTHLY        
            if ".M." in name_list:
                for task in root.iter('task'):
                    if task.get('Object') == plan_name:
                        cale_tag = task.find('calendars/cale')
                        cale_key_name = cale_tag.get('CaleKeyName')
                        date = cale_key_name[3:5].replace("T", "")
                        rrule = 'FREQ=MONTHLY;BYMONTHDAY=' + date + ';BYHOUR=' + hour + ';BYMINUTE=' + minutes + ';BYSECOND=0'
                        return rrule
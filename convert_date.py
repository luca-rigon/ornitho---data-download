def convert_date(date, no_time):     #--> input: YYYY-MM-DDThh:mm:ss+xx:xx as a string; no_time is a bool
    date_out = f"{str(date[8:10])}/{str(date[5:7])}/{str(date[0:4])}"  #DD/MM/YYYY
    
    if no_time:
        time_ss = None
        time_mm = None
    else:
        time_ss = str(date[11:19])     #hh:mm:ss
        time_mm = time_ss[:-3]         #hh:mm
        
    return date_out, time_mm, time_ss

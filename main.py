import os
import pandas as pd
import datetime as dt
import schedule
# import time


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def main():
    default_val = 0
    # Running the aforementioned command and saving its output
    output = os.popen('wmic process get description, processid').read()

    # Displaying the output
    # print(output)

    process_list = [line.split(" ")[0].strip() for line in output[1:].split("\n\n")]
    app_set = set(process_list)
    app_set.remove("")

    try:
        app_time_df = pd.read_csv("screen_time.csv", usecols=["App", "Time"])
        for app in app_set:
            if app in list(app_time_df["App"]):
                for i in range(len(app_time_df)):
                    if app_time_df["App"][i] == app:
                        app_time_df["Time"][i] += 10
            else:
                app_time_df.loc[len(app_time_df)] = [app, default_val]
        app_time_df = app_time_df.sort_values(by=["App"])
        app_time_df = app_time_df.sort_values(ascending=False, by=["Time"])
        app_time_df.to_csv("screen_time.csv")
    except:
        app_time_list = zip(list(app_set), [default_val for _ in range(len(app_set))])
        app_time_df = pd.DataFrame(app_time_list, columns=["App", "Time"])
        app_time_df = app_time_df.sort_values(by=["App"])
        app_time_df = app_time_df.sort_values(ascending=False, by=["Time"])
        app_time_df.to_csv("screen_time.csv")

    for i in range(len(app_time_df)):
        conversion = dt.timedelta(seconds=int(app_time_df["Time"][i]))
        converted_time = str(conversion)
        app_time_df["Time"][i] = converted_time

    clear_console()
    print(app_time_df.to_markdown())


if __name__ == '__main__':
    with open("screen_time.csv", "w") as write_file:
        write_file.write("")
    try:
        main()
        schedule.every(10).seconds.do(main)
        while True:
            # s_t = time.time()
            schedule.run_pending()
            # time.sleep(10 - (time.time() - s_t))
    except:
        print("Something Went Wrong. Debug The Code!")


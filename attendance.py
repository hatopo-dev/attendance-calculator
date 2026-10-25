import csv
from datetime import date
from pathlib import Path
def format_time(minutes):
    hour = minutes//60
    minute = minutes % 60
    time_message = f'{hour:02d}:{minute:02d}'
    return time_message
def input_time():
    global time_flag
    is_valid = True
    if time_flag == 0:
        time_message = '出勤時刻(時)を入力してください：'
        max_time = 23
    elif time_flag == 1:
        time_message = '出勤時刻(分)を入力してください：'
        max_time = 59
    elif time_flag == 2:
        time_message = '退勤時刻(時)を入力してください：'
        max_time = 23
    elif time_flag == 3:
        time_message = '退勤時刻(分)を入力してください：'
        max_time = 59
    else:
        print('もう一度最初から入力してください')
        time_message = '出勤時刻(時)を入力してください：'
        max_time = 23
        time_flag = 0
    while is_valid:
        try:
            time = int (input(time_message))
            is_valid = input_check(time,max_time)
        except ValueError:
            print('数字で入力してください')
    time_flag += 1
    return time

def input_check(time,max_time):     #入力した数値が範囲内かのチェック
        if time >= 0 and time <= max_time:
            return False
        else:
            print('0~'+str(max_time)+'の数字を入力してください')
            return True
csv_file = Path('attendance.csv')
is_new_file =not csv_file.exists()
time_flag = 0        
standard_work_minutes = 480
fixed_over_minutes = 2700
total_working_minutes = 0
total_over_minutes = 0
is_inputting_time = True
is_inputting_day = True
day_working = {}
if not is_new_file:
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] in day_working:
                day_working[row[0]] += int(row[6])
            else:
                day_working[row[0]] = int(row[6])
            total_working_minutes += int(row[6])
            total_over_minutes += int(row[7])
        fixed_over_minutes = fixed_over_minutes - total_over_minutes
while is_inputting_day:
    is_checking_day = True
    while is_checking_day:
        try:
            year = int(input('年を入力してください：'))
            month = int(input('月を入力してください：'))
            day = int(input('日を入力してください：'))
            work_date = date(year, month, day)
            print(work_date)
            is_checking_day = False
        except ValueError:
            print('入力された日付が正しくありません')
    over_minutes = 0
    is_checking_continue = True
    while is_inputting_time:
        start_minutes = input_time() * 60
        start_minutes += input_time()
        start_time_text = format_time(start_minutes)
        end_minutes = input_time() * 60
        end_minutes += input_time()
        end_time_text = format_time(end_minutes)
        if start_minutes  < end_minutes:
            is_inputting_time = False
            is_valid = True
            while is_valid:
                try:
                    break_minutes = int(input('休憩時間(分)を入力してください：'))
                    elapsed_minutes = end_minutes - start_minutes #休憩時間を引いてない稼働時間:elapsed_minutes
                    working_minutes = elapsed_minutes - break_minutes #休憩時間を引いた時間:working_minutes
                    working_time_text = format_time(working_minutes)
                    if break_minutes <= elapsed_minutes and break_minutes >= 0:
                        is_valid = False
                    else:
                        print('正しい数字を入力してください')
                except ValueError:
                    print('数字で入力してください')
            print('実働時間：'+str(working_minutes//60)+'時間'+str(working_minutes%60)+'分')
            if working_minutes > standard_work_minutes: #残業時間が発生しているかの確認
                over_minutes = working_minutes - standard_work_minutes #残業時間:over_minutes
                print('残業時間：'+str(over_minutes//60)+'時間'+str(over_minutes%60)+'分')
                fixed_over_minutes = fixed_over_minutes - over_minutes #残りの固定残業時間
            else:
                print('残業時間はありません')
            if fixed_over_minutes >= 0:
                print('固定残業時間の残りは'+str(fixed_over_minutes//60)+'時間'+str(fixed_over_minutes%60)+'分')
            else:
                p_fixed_over_minutes = fixed_over_minutes * -1
                print('固定残業時間を'+str(p_fixed_over_minutes//60)+'時間'+str(p_fixed_over_minutes%60)+'分超過しています')
            total_working_minutes += working_minutes
            total_over_minutes += over_minutes
            print('今までの稼働時間の合計は'+str(total_working_minutes//60)+'時間'+str(total_working_minutes%60)+'分')
            print('今までの残業時間の合計は'+str(total_over_minutes//60)+'時間'+str(total_over_minutes%60)+'分')
        else:
            print('出勤時間と退勤時間に誤りがあります')
            time_flag = 0
    over_time_text = format_time(over_minutes)
    with open(csv_file, 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow(['日付', '出勤', '退勤', '休憩時間', '実働時間', '残業時間','実働(分)', '残業(分)'])
            is_new_file = False
        writer.writerow([work_date,start_time_text,end_time_text,break_minutes,working_time_text,over_time_text,working_minutes,over_minutes])
        if str(work_date) in day_working:
            day_working[str(work_date)] += working_minutes
        else:
            day_working[str(work_date)] = working_minutes
    while is_checking_continue:
        try:
            next_day_continue = int(input('続けて入力しますか？1:続行 2:中断'))
            if next_day_continue == 1:
                time_flag = 0
                is_inputting_time = True
                is_checking_continue = False
            elif next_day_continue == 2:
                is_inputting_day = False
                is_checking_continue = False
                print('-----日別集計-----')
                for day,minutes in day_working.items():
                    print(day+':'+str(minutes//60)+'時間'+str(minutes%60)+'分')
            else:
                print('「1」か「2」で入力して下さい')
        except ValueError:
            print('「1」か「2」で入力して下さい')
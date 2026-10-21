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
time_flag = 0        
standard_work_minutes = 480
fixed_over_minutes = 2700
total_working_minutes = 0
total_over_minutes = 0
is_inputting_time = True
is_inputting_day = True

while is_inputting_day:
    over_minutes = 0
    is_checking_continue = True
    while is_inputting_time:
        start_minutes = input_time() * 60
        start_minutes += input_time()
        end_minutes = input_time() * 60
        end_minutes += input_time()
        if start_minutes  < end_minutes:
            is_inputting_time = False
            is_valid = True
            while is_valid:
                try:
                    break_minutes = int(input('休憩時間(分)を入力してください：'))
                    elapsed_minutes = end_minutes - start_minutes #休憩時間を引いてない稼働時間:elapsed_minutes
                    working_minutes = elapsed_minutes - break_minutes #休憩時間を引いた時間:working_minutes
                    if break_minutes <= elapsed_minutes and break_minutes >= 0 and break_minutes <=60:
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
            else:
                print('「1」か「2」で入力して下さい')

        except ValueError:
            print('「1」か「2」で入力して下さい')
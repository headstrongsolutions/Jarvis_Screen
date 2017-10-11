from datetime import datetime
from datetime import timedelta


class timecycle:
    # describes the type
    typeDescription = 'Creates a timeable instance we can use for timing cycles of things'

    def __init__(self):
        self.wait_time = 15
        self.alarm_start = datetime.now()
        self.wait_time_delta = timedelta(minutes=self.wait_time)
        self.alarm_time = self.alarm_start + self.wait_time_delta
        self.force_alarm = False

    def reset_alarm(self):
        self.force_alarm = False
        self.alarm_start = datetime.now()
        self.wait_time_delta = timedelta(minutes=self.wait_time)
        self.alarm_time = self.alarm_start + self.wait_time_delta

    def is_alarming(self):
        now = datetime.now().strftime("%s")
        print("now = " + now)
        alarm_time = self.alarm_time.strftime("%s")
        print("alarm time = " + alarm_time)
        if now > alarm_time or self.force_alarm:
            self.reset_alarm()
            return True
        else:
            return False

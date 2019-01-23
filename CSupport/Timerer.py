import time
from datetime import datetime


class Timerer(object):

    def __init__(self):
        self.set_decimal_places(2)

    # MAIN METHODS ---------------------------------------------------------------------------------

    def set_initial_timestamp(self, print_results=True):
        """
        Starts timer and saves the time. Optionally prints results to console.

        :param print_results: Boolean. If print results to console.
        """
        self.start_time_measurement()

        if print_results:
            print("-Date and Time of Starting Execution: " +
                  self.as_date(self.global_start_time).strftime("%d/%m/%Y") + " " +
                  self.as_date(self.global_start_time).strftime("%X"))

    def set_meantime(self, label=None, print_results=True):
        """
        Creates meantime - interval with appropriate label. Optionally prints results to consol.

        :param label: String. Description of the interval.
        :param print_results: Boolean. If print results to console.
        """
        """
        

        :param print_results: Boolean. If print results to console.
        :return:
        """
        t = time.time()
        self.meantimes_in_sec.append(t - self.start_meantime)
        self.meantimes_labels.append(label)
        self.start_meantime = t

        if print_results:
            caption = "--Meantime Duration is: "
            if label is not None:
                caption = "--Meantime Duration of " + label + " is: "
            print(caption +
                  str(round(self.meantimes_in_sec[-1] / 60, self.dec_places)) + " minutes / " +
                  str(round(self.meantimes_in_sec[-1], self.dec_places)) + " seconds")

    def set_final_timestamp(self, label=None, print_results=True):
        """
        Ends timer and saves the time. Optionally prints results to console.

        :param label: String. Label of last interval.
        :param print_results: Boolean. If print results to console.
        """
        self.end_time_measurement(label)

        if print_results:
            caption = "Meantime Duration is: "
            if label is not None:
                caption = "Meantime Duration of " + label + " is: "
            print(caption +
                  str(round(self.meantimes_in_sec[-1] / 60, self.dec_places)) + " minutes / " +
                  str(round(self.meantimes_in_sec[-1], self.dec_places)) + " seconds")
            print("-Date and Time of Ending Execution: " +
                  self.as_date(self.global_end_time).strftime("%d/%m/%Y") + " " +
                  self.as_date(self.global_end_time).strftime("%X"))
            print("-Overall Time Duration Is: " +
                  str(round((self.global_end_time -
                             self.global_start_time) / 60, self.dec_places)) + " minutes / " +
                  str(round((self.global_end_time -
                             self.global_start_time), self.dec_places)) + " seconds")

    # GETTERS -------------------------------------------------------------------------------------

    def get_start_time(self):
        """
        Returns global start time as timestamp/float.

        :return: Timestamp/float.
        """
        return self.global_start_time

    def get_end_time(self):
        """
        Returns global end time as timestamp/float.

        :return: Timestamp/float.
        """
        return self.global_end_time

    def get_meantimes(self):
        """
        Returns meantimes durations and labels.

        :return: Tuple of two lists - meantimes duration in seoconds and
                 meantime labels.
        """
        return self.meantimes_in_sec, self.meantimes_labels

    # HELPER FUNCTIONS ----------------------------------------------------------------------------

    def as_date(self, timestamp):
        """
        Converts timestamp in float format to date format.

        :param timestamp: Float. Date as float.
        :return: Datetime format.
        """
        return datetime.utcfromtimestamp(timestamp)

    def set_decimal_places(self, d):
        """
        Sets default decimal places for float numbers.

        :param d: Int.
        """
        self.dec_places = d

    def start_time_measurement(self):
        """
        Starts global time measurement.
        """
        self.global_start_time = time.time()
        self.global_end_time = None
        self.start_meantime = self.global_start_time

        self.meantimes_in_sec = []
        self.meantimes_labels = []

    def end_time_measurement(self, label):
        """
        Ends global time measurement.

        :param labels: String. Label of last interval.
        """
        self.global_end_time = time.time()
        self.meantimes_in_sec.append(self.global_end_time - self.start_meantime)
        self.meantimes_labels.append(label)

if __name__ == "__main__":
    t = Timerer()

    t.set_initial_timestamp(print_results=True)
    time.sleep(0.2)

    t.set_meantime(label="Firts Interval", print_results=True)
    time.sleep(0.3)

    t.set_meantime(label="Second Interval", print_results=True)
    time.sleep(0.1)

    t.set_final_timestamp(label="Last Interval", print_results=True)

    (mt, mt_l) = t.get_meantimes()

    print(round(sum(mt), 2))

    print(t.get_start_time())
    print(t.get_end_time())
    print(mt)
    print(mt_l)

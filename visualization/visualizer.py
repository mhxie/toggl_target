#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Minghao Xie <mihxie@gmail.com>

from cmath import exp
import pandas as pd
import seaborn as sns
from datetime import date


class Visualizer(object):
    """ A collection of visualizing scipts
    """

    def __init__(self):
        sns.set(style="whitegrid")
        today = date.today()
        self.today = int(today.strftime("%d"))

    def plot_progress_this_month(self, df_last_month, df_this_month, w, t=None, project=None):
        """ Visualizing the progress of the month
        """
        print("\nPlotting progress this month...")
        if t:
            normal_min_hours, crunch_min_hours = t.get_minimum_daily_hours(
                w.business_days_left_count, w.days_left_count)
        end_date = w.month_end.day
        if not project:
            df = pd.DataFrame(columns=['month', 'date', 'hours'])
            # aggregate entries to project
            cum_hours_last_month = 0
            cum_hours_this_month = 0
            end_of_this_month = self.today
            for i in range(1, end_date):
                last_month_list = df_last_month[df_last_month["Date"] == i]
                cum_hours_last_month += last_month_list["Hours"].sum()
                dfi0 = pd.DataFrame({'Month': 'Last Month', 'Date': i,
                                     'Hours': cum_hours_last_month}, index=[i-1])
                if i > self.today and w is None:
                    df = pd.concat([df, dfi0], ignore_index=True)
                else:
                    if i <= self.today:
                        this_month_list = df_this_month[df_this_month["Date"] == i]
                        cum_hours_this_month += this_month_list["Hours"].sum()
                        dfi1 = pd.DataFrame({'Month': 'This Month', 'Date': i,
                                             'Hours': cum_hours_this_month}, index=[i-1])
                        dfi2 = pd.DataFrame({'Month': 'Expected', 'Date': i,
                                             'Hours': cum_hours_this_month}, index=[i-1])
                        df = pd.concat([df, dfi0, dfi1, dfi2],
                                       ignore_index=True)
                    else:
                        cum_hours_this_month += crunch_min_hours
                        dfi1 = pd.DataFrame({'Month': 'Expected', 'Date': i,
                                             'Hours': cum_hours_this_month}, index=[i-1])
                        df = pd.concat([df, dfi0, dfi1], ignore_index=True)

            # plot
            hue_order = ['Expected', 'Last Month', 'This Month']
            g = sns.lineplot(x="Date", y="Hours", hue="Month",
                             hue_order=hue_order, data=df)
            path = "month_progress.png"
            g.figure.savefig(path, dpi=300)
            return path

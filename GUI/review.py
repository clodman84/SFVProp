import logging
import threading
import time

import dearpygui.dearpygui as dpg
import numpy as np
from pyparsing import itertools

from GUI.utils import modal_message

logger = logging.getLogger("Core.Kharon")

course_average = np.random.randint(40, 60, 10)
quota = course_average / 2


class ReviewPanel:
    def __init__(self, ID: int):
        with dpg.window(
            label=f"Performance Report for {ID}",
        ) as self.window:
            self.erased = False
            self.data = [[], [], [], []]
            self.time = []
            self.t_signal = 0
            self.base_frequency = 1
            self.amplitude = 1
            self.ID = ID
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text(
                        "Imagine some personal \ninformation and a \npicture of the guy here"
                    )
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Erase?", callback=self.erase)
                with dpg.plot(tag=f"{ID}_ecg_plot", width=-1):
                    dpg.add_plot_axis(dpg.mvXAxis, tag=f"{ID}xaxis")
                    dpg.set_axis_limits(dpg.last_item(), -10, 0)
                    dpg.add_plot_axis(dpg.mvYAxis, tag=f"{ID}yaxis")
                    dpg.set_axis_limits(dpg.last_item(), -2, 1.5)
                    dpg.add_line_series([], [], tag=f"{ID}line0", parent=f"{ID}yaxis")
                    dpg.add_line_series([], [], tag=f"{ID}line1", parent=f"{ID}yaxis")
                    dpg.add_line_series([], [], tag=f"{ID}line2", parent=f"{ID}yaxis")
                    dpg.add_line_series([], [], tag=f"{ID}line3", parent=f"{ID}yaxis")

            with dpg.item_handler_registry(tag=f"{ID}ecg_plot_ref"):
                dpg.add_item_visible_handler(callback=self.update_plot)
            dpg.bind_item_handler_registry(f"{ID}_ecg_plot", dpg.last_container())

            limits_group_series = [-0.5, 9.5]
            with dpg.plot(label="Performance", height=400, width=-1):
                dpg.add_plot_legend()
                student_score = np.random.randint(0, 20, 10)
                ilabels = ["Average", "Quota", "Score"]
                glabels = (
                    ("S1", 0),
                    ("S2", 1),
                    ("S3", 2),
                    ("S4", 3),
                    ("S5", 4),
                    ("S6", 5),
                    ("S7", 6),
                    ("S8", 7),
                    ("S9", 8),
                    ("S10", 9),
                )
                groups_c = 3

                # create x axis
                dpg.add_plot_axis(
                    dpg.mvXAxis,
                    tag=f"{ID}_xaxis_bar_group",
                    no_gridlines=True,
                    auto_fit=True,
                )
                dpg.set_axis_limits(dpg.last_item(), *limits_group_series)
                dpg.set_axis_ticks(dpg.last_item(), glabels)

                # create y axis
                with dpg.plot_axis(
                    dpg.mvYAxis,
                    label="Score",
                    tag=f"{ID}_yaxis_bar_group",
                    auto_fit=True,
                ):
                    dpg.set_axis_limits(dpg.last_item(), 0, 110)
                    dpg.add_bar_group_series(
                        values=list(
                            itertools.chain(course_average, quota, student_score)
                        ),
                        label_ids=ilabels,
                        group_size=groups_c,
                        tag=f"{ID}_bar_group_series",
                        label="Final Exam",
                    )

    def update_plot(self):
        self.t_signal += dpg.get_delta_time()
        dpg.set_axis_limits(f"{self.ID}xaxis", self.t_signal - 10, self.t_signal)
        self.time.append(self.t_signal)
        for i in range(4):
            self.data[i].append(
                self.amplitude * np.sin(self.base_frequency * i * self.t_signal)
            )
            dpg.set_value(f"{self.ID}line{i}", [self.time, self.data[i]])

    def erase(self):
        self.erased = not self.erased
        thread = threading.Thread(target=self.obliterating)
        thread.start()

    def obliterating(self):
        start = time.time()
        record = 0
        associate = 0
        while True:
            now = time.time()
            if now - start > 0.015:
                if record < 500:
                    self.base_frequency += 0.001
                    logger.warning(f"Purging Record: {record}")
                    record += 1
                    start = now
                else:
                    self.amplitude = self.amplitude - 0.004
                    logger.critical(f"Handling Association: {associate}")
                    associate += 1
                    start = now
            if associate > 250:
                break
        modal_message(f"Done!")

    def close(self):
        dpg.delete_item(self.window)

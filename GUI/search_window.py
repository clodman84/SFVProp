import logging

import dearpygui.dearpygui as dpg

from Application import SearchMachine
from GUI.review import ReviewPanel
from GUI.tablez import TableManager9000

logger = logging.getLogger("GUI.Bill")


class SearchWindow:
    def __init__(self):
        self.search_machine = SearchMachine()
        self.num_rows = 45

        with dpg.window(
            label=f"Psychostasia Portal",
            width=-1,
            height=-1,
            no_close=True,
        ) as self.window:
            with dpg.group(horizontal=True):
                dpg.add_text("Search")
                input = dpg.add_input_text(width=250)

            with dpg.group(horizontal=True) as parent:
                self.suggestions_panel = dpg.add_child_window(parent=parent)
                self.suggestion_table = TableManager9000(
                    parent=self.suggestions_panel,
                    rows=self.num_rows,
                    headers=["Name", "ID", "Bhawan", "Room"],
                )
                self.suggestion_table["Name"] = dpg.add_text, {"label": ""}
                self.suggestion_table["ID"] = dpg.add_button, {
                    "label": "",
                    "show": False,
                    "callback": lambda s, a, u: self.review_performance(u),
                }
                self.suggestion_table["Bhawan"] = dpg.add_text, {"label": ""}
                self.suggestion_table["Room"] = dpg.add_text, {"label": ""}
                self.suggestion_table.construct()
                # TODO: the review panel code goes in here

            dpg.set_item_callback(input, self.suggest)

    def review_performance(self, user):
        ReviewPanel(user)

    def suggest(self, sender, app_data, user_data):
        if len(app_data) > 0:
            matches = self.search_machine.search(app_data)
        else:
            return

        if not matches:
            for row in range(self.num_rows):
                for column, cell in self.suggestion_table[row].items():
                    if column == "ID":
                        dpg.hide_item(cell)
                    dpg.set_value(cell, "")
            dpg.set_value(self.suggestion_table[0]["Name"], "No matches")
        else:
            for row, item in enumerate(matches):
                if row == self.num_rows - 1:
                    break
                for j, column in enumerate(self.suggestion_table.headers):
                    if column == "ID":
                        dpg.set_item_label(
                            self.suggestion_table[row][column], item.idno
                        )
                        dpg.set_item_user_data(
                            self.suggestion_table[row][column], item.idno
                        )
                        dpg.show_item(self.suggestion_table[row][column])
                    dpg.set_value(self.suggestion_table[row][column], item[j])

            for row in range(len(matches), self.num_rows):
                for column in self.suggestion_table.headers:
                    if column == "ID":
                        dpg.hide_item(self.suggestion_table[row][column])
                    dpg.set_value(self.suggestion_table[row][column], "")

    def close(self):
        dpg.delete_item(self.window)

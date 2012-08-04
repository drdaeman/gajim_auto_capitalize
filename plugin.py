"""
Gajim automatic capitalization plugin.
Copyright (c) 2012, Aleksey Zhukov.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import gtk
import unicodedata
from common import helpers
from common import gajim

from plugins import GajimPlugin
from plugins.helpers import log_calls, log

SENTENCE_TERMINATORS = u".!?\u203d\u2e2e"

class CapitalizePlugin(GajimPlugin):
    @log_calls("CapitalizePlugin")
    def init(self):
        self.description = _("Automatically changes first letters of sentence to uppercase.")
        self.config_dialog = None
        self.controls = []
        self.gui_extension_points = {
            "chat_control_base": (
                self.connect_with_chat_control,
                self.disconnect_from_chat_control
            )
        }

    @log_calls("CapitalizePlugin")
    def activate(self):
        pass

    @log_calls("CapitalizePlugin")
    def deactivate(self):
        pass

    @log_calls("CapitalizePlugin")
    def connect_with_chat_control(self, chat_control):
        self.chat_control = chat_control
        control = Base(self, self.chat_control)
        self.controls.append(control)

    @log_calls("CapitalizePlugin")
    def disconnect_from_chat_control(self, chat_control):
        for control in self.controls:
            control.disconnect_from_chat_control()
        self.controls = []

class Base(object):
    def __init__(self, plugin, chat_control):
        self.plugin = plugin
        self.chat_control = chat_control
        self.textview = self.chat_control.conv_textview

        self.event = self.chat_control.msg_textview.connect("key_press_event", self.on_keypress)
        self.chat_control.handlers[self.event] = self.chat_control.msg_textview

    def disconnect_from_chat_control(self):
        if self.chat_control.msg_textview.handler_is_connected(self.event):
            self.chat_control.msg_textview.disconnect(self.event)

    def on_keypress(self, widget, event):
        default_editable = self.chat_control.msg_textview.get_editable()
        buf = self.chat_control.msg_textview.get_buffer()
        i = buf.get_start_iter()

        state = "capitalize"
        while True:
            c = i.get_char()
            cc = unicodedata.category(c)

            if state == "normal" and c in SENTENCE_TERMINATORS:
                state = "expect_space"
            elif state == "expect_space":
                state = "capitalize" if cc.startswith("Z") else "wait_space"
            elif state == "wait_space" and cc.startswith("Z"):
                state = "normal"
            elif state == "capitalize":
                if not (cc.startswith("Z") or cc.startswith("P") or cc.startswith("C")):
                    if cc == "Ll":
                        uc = c.upper()
                        if uc != c:
                            p = i.copy()
                            p.forward_char()
                            if buf.delete_interactive(i, p, default_editable):
                                buf.insert_interactive(i, uc, default_editable)
                    state = "normal"
            if not i.forward_char():
                break

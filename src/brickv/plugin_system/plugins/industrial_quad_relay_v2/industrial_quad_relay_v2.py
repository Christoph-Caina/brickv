# -*- coding: utf-8 -*-
"""
Industrial Quad Relay Plugin
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

industrial_quad_relay_v2.py: Industrial Quad Relay 2.0 Plugin Implementation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from PyQt4.QtCore import Qt, pyqtSignal, QTimer

from brickv.plugin_system.comcu_plugin_base import COMCUPluginBase
from brickv.plugin_system.plugins.industrial_quad_relay_v2.ui_industrial_quad_relay_v2 import Ui_IndustrialQuadRelayV2
from brickv.bindings.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from brickv.async_call import async_call
from brickv.load_pixmap import load_masked_pixmap

class IndustrialQuadRelayV2(COMCUPluginBase, Ui_IndustrialQuadRelayV2):
    qtcb_monoflop = pyqtSignal(int, int)

    def __init__(self, *args):
        COMCUPluginBase.__init__(self, BrickletIndustrialQuadRelayV2, *args)

        self.setupUi(self)

        self.iqr = self.device

        self.open_pixmap = load_masked_pixmap('plugin_system/plugins/industrial_quad_relay/relay_open.bmp')
        self.close_pixmap = load_masked_pixmap('plugin_system/plugins/industrial_quad_relay/relay_close.bmp')

        self.relay_buttons = [self.b0, self.b1, self.b2, self.b3]
        self.relay_button_icons = [self.b0_icon, self.b1_icon, self.b2_icon, self.b3_icon]
        self.relay_button_labels = [self.b0_label, self.b1_label, self.b2_label, self.b3_label]
        for icon in self.relay_button_icons:
            icon.setPixmap(self.open_pixmap)
            icon.show()


        def get_button_lambda(button):
            return lambda: self.relay_button_clicked(button)

        for i in range(len(self.relay_buttons)):
            self.relay_buttons[i].clicked.connect(get_button_lambda(i))

        self.qtcb_monoflop.connect(self.cb_monoflop)
        self.iqr.register_callback(self.iqr.CALLBACK_MONOFLOP_DONE,
                                   self.qtcb_monoflop.emit)

        self.monoflop_pin.currentIndexChanged.connect(self.monoflop_pin_changed)
        self.monoflop_go.clicked.connect(self.monoflop_go_clicked)
        self.monoflop_time_before = [1000] * 4
        self.monoflop_pending = [False] * 4

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.setInterval(50)
        
    def get_output_value_async(self, value):
        for button in range(4):
            if value[button]:
                self.relay_buttons[button].setText('Switch Off')
                self.relay_button_icons[button].setPixmap(self.close_pixmap)
            else:
                self.relay_buttons[button].setText('Switch On')
                self.relay_button_icons[button].setPixmap(self.open_pixmap)
        
    def start(self):
        async_call(self.iqr.get_output_value, None, self.get_output_value_async, self.increase_error_count)

    def stop(self):
        self.update_timer.stop()

    def destroy(self):
        pass

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletIndustrialQuadRelayV2.DEVICE_IDENTIFIER

    def get_current_value(self):
        value = 0
        i = 0
        for b in self.relay_buttons:
            if 'Off' in b.text():
                value |= (1 << i)
            i += 1
        return value

    def relay_button_clicked(self, button):
        value = self.get_current_value()
        if 'On' in self.relay_buttons[button].text():
            value |= (1 << button)
            self.relay_buttons[button].setText('Switch Off')
            self.relay_button_icons[button].setPixmap(self.close_pixmap)
        else:
            value &= ~(1 << button)
            self.relay_buttons[button].setText('Switch On')
            self.relay_button_icons[button].setPixmap(self.open_pixmap)

        self.iqr.set_selected_output_value(button, value)

        self.update_timer.stop()

        for pin in range(4):
            self.monoflop_pending[pin] = False

        pin = int(self.monoflop_pin.currentText().replace('Pin ', ''))
        self.monoflop_time.setValue(self.monoflop_time_before[pin])
        self.monoflop_time.setEnabled(True)

    def cb_monoflop(self, pin, value):
        self.monoflop_pending[pin] = False

        if value:
            self.relay_buttons[pin].setText('Switch Off')
            self.relay_button_icons[pin].setPixmap(self.close_pixmap)
        else:
            self.relay_buttons[pin].setText('Switch On')
            self.relay_button_icons[pin].setPixmap(self.open_pixmap)

        if sum(self.monoflop_pending) == 0:
            self.update_timer.stop()

        current_pin = int(self.monoflop_pin.currentText().replace('Pin ', ''))
        if current_pin == pin:
            self.monoflop_time.setValue(self.monoflop_time_before[current_pin])
            self.monoflop_time.setEnabled(True)

    def monoflop_pin_changed_async(self, monoflop):
        _, _, time_remaining = monoflop
        self.monoflop_time.setValue(time_remaining)

    def monoflop_pin_changed(self):
        try:
            pin = int(self.monoflop_pin.currentText().replace('Pin ', ''))
        except ValueError:
            return

        if self.monoflop_pending[pin]:
            async_call(self.iqr.get_monoflop, pin, self.monoflop_pin_changed_async, self.increase_error_count)
            self.monoflop_time.setEnabled(False)
        else:
            self.monoflop_time.setValue(self.monoflop_time_before[pin])
            self.monoflop_time.setEnabled(True)

    def monoflop_go_clicked(self):
        pin = int(self.monoflop_pin.currentText().replace('Pin ', ''))
        if self.monoflop_pending[pin]:
            time = self.monoflop_time_before[pin]
        else:
            time = self.monoflop_time.value()

        value = self.monoflop_state.currentIndex() == 0

        self.monoflop_time.setEnabled(False)
        self.monoflop_time_before[pin] = time
        self.monoflop_pending[pin] = True
        self.iqr.set_monoflop(pin, value, time)

        if value:
            self.relay_buttons[pin].setText('Switch Off')
            self.relay_button_icons[pin].setPixmap(self.close_pixmap)
        else:
            self.relay_buttons[pin].setText('Switch On')
            self.relay_button_icons[pin].setPixmap(self.open_pixmap)

        self.update_timer.start()

    def update_async(self, pin, value, time, time_remaining):
        if self.monoflop_pending[pin]:
            self.monoflop_time.setValue(time_remaining)

    def update(self):
        try:
            pin = int(self.monoflop_pin.currentText().replace('Pin ', ''))
        except ValueError:
            return

        async_call(self.iqr.get_monoflop, pin, lambda monoflop: self.update_async(pin, *monoflop), self.increase_error_count)

# -*- coding: utf-8 -*-
"""
UV Light Plugin
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

uv_light.py: UV Light Bricklet Plugin Implementation

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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QVBoxLayout

from brickv.plugin_system.plugin_base import PluginBase
from brickv.bindings.bricklet_uv_light import BrickletUVLight
from brickv.plot_widget import PlotWidget, FixedSizeLabel
from brickv.async_call import async_call
from brickv.callback_emulator import CallbackEmulator

class IndexLabel(FixedSizeLabel):
    def setText(self, text):
        super(IndexLabel, self).setText('UV Index: ' + text)

class UVLight(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, BrickletUVLight, *args)

        self.uv_light = self.device

        self.cbe_uv_light = CallbackEmulator(self.uv_light.get_uv_light,
                                             self.cb_uv_light,
                                             self.increase_error_count)

        self.index_label = IndexLabel('UV Index:')

        self.current_uv_light = None

        plots = [('UV Light', Qt.red, lambda: self.current_uv_light, u'{} µW/cm²'.format)]
        self.plot_widget = PlotWidget(u'UV Light [µW/cm²]', plots, extra_key_widgets=[self.index_label])

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)

    def start(self):
        async_call(self.uv_light.get_uv_light, None, self.cb_uv_light, self.increase_error_count)
        self.cbe_uv_light.set_period(100)

        self.plot_widget.stop = False

    def stop(self):
        self.cbe_uv_light.set_period(0)

        self.plot_widget.stop = True

    def destroy(self):
        pass

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletUVLight.DEVICE_IDENTIFIER

    def cb_uv_light(self, uv_light):
        self.current_uv_light = uv_light

        index = round(uv_light/250.0, 1)
        self.index_label.setText(unicode(index))

        if index < 2.5:
            color = 'green'
        elif index < 5.5:
            color = 'yellow'
        elif index < 7.5:
            color = 'orange'
        elif index < 10.5:
            color = 'red'
        else:
            color = 'magenta'

        self.index_label.setStyleSheet('QLabel {{ color : {0} }}'.format(color))

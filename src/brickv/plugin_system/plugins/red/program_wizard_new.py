# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

program_wizard_new.py: New Program Wizard

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
from PyQt4.QtGui import QWizard
from brickv.plugin_system.plugins.red.program_wizard_utils import *
from brickv.plugin_system.plugins.red.program_page_general import ProgramPageGeneral
from brickv.plugin_system.plugins.red.program_page_files import ProgramPageFiles
from brickv.plugin_system.plugins.red.program_page_java import ProgramPageJava
from brickv.plugin_system.plugins.red.program_page_python import ProgramPagePython
from brickv.plugin_system.plugins.red.program_page_ruby import ProgramPageRuby
from brickv.plugin_system.plugins.red.program_page_shell import ProgramPageShell
from brickv.plugin_system.plugins.red.program_page_arguments import ProgramPageArguments
from brickv.plugin_system.plugins.red.program_page_stdio import ProgramPageStdio
from brickv.plugin_system.plugins.red.program_page_schedule import ProgramPageSchedule
from brickv.plugin_system.plugins.red.program_page_summary import ProgramPageSummary
from brickv.plugin_system.plugins.red.program_page_upload import ProgramPageUpload

class ProgramWizardNew(QWizard):
    def __init__(self, session, identifiers, script_manager, *args, **kwargs):
        QWizard.__init__(self, *args, **kwargs)

        self.session = session
        self.identifiers = identifiers
        self.script_manager = script_manager
        self.canceled = False

        self.setWindowFlags(self.windowFlags() | Qt.Tool)
        self.setWindowTitle('New Program')

        self.setPage(Constants.PAGE_GENERAL, ProgramPageGeneral(title_prefix='Step 1 or 8: '))
        self.setPage(Constants.PAGE_FILES, ProgramPageFiles(title_prefix='Step 2 or 8: '))
        self.setPage(Constants.PAGE_JAVA, ProgramPageJava(title_prefix='Step 3 or 8: '))
        self.setPage(Constants.PAGE_PYTHON, ProgramPagePython(title_prefix='Step 3 or 8: '))
        self.setPage(Constants.PAGE_RUBY, ProgramPageRuby(title_prefix='Step 3 or 8: '))
        self.setPage(Constants.PAGE_SHELL, ProgramPageShell(title_prefix='Step 3 or 8: '))
        self.setPage(Constants.PAGE_ARGUMENTS, ProgramPageArguments(title_prefix='Step 4 or 8: '))
        self.setPage(Constants.PAGE_STDIO, ProgramPageStdio(title_prefix='Step 5 or 8: '))
        self.setPage(Constants.PAGE_SCHEDULE, ProgramPageSchedule(title_prefix='Step 6 or 8: '))
        self.setPage(Constants.PAGE_SUMMARY, ProgramPageSummary(title_prefix='Step 7 or 8: '))
        self.setPage(Constants.PAGE_UPLOAD, ProgramPageUpload(title_prefix='Step 8 or 8: '))

        self.rejected.connect(lambda: self.set_canceled(True))

    # overrides QWizard.sizeHint
    def sizeHint(self):
        size = QWizard.sizeHint(self)

        if size.width() < 550:
            size.setWidth(550)

        if size.height() < 700:
            size.setHeight(700)

        return size

    # overrides QWizard.nextId
    def nextId(self):
        currentId = self.currentId()

        if currentId == Constants.PAGE_GENERAL:
            return Constants.PAGE_FILES
        elif currentId == Constants.PAGE_FILES:
            language = self.field(Constants.FIELD_LANGUAGE).toInt()[0]

            if language == Constants.LANGUAGE_JAVA:
                return Constants.PAGE_JAVA
            elif language == Constants.LANGUAGE_PYTHON:
                return Constants.PAGE_PYTHON
            elif language == Constants.LANGUAGE_RUBY:
                return Constants.PAGE_RUBY
            elif language == Constants.LANGUAGE_SHELL:
                return Constants.PAGE_SHELL
            else:
                return Constants.PAGE_GENERAL
        elif currentId in (Constants.PAGE_JAVA, Constants.PAGE_PYTHON, Constants.PAGE_RUBY, Constants.PAGE_SHELL):
            return Constants.PAGE_ARGUMENTS
        elif currentId == Constants.PAGE_ARGUMENTS:
            return Constants.PAGE_STDIO
        elif currentId == Constants.PAGE_STDIO:
            return Constants.PAGE_SCHEDULE
        elif currentId == Constants.PAGE_SCHEDULE:
            return Constants.PAGE_SUMMARY
        elif currentId == Constants.PAGE_SUMMARY:
            return Constants.PAGE_UPLOAD
        elif currentId == Constants.PAGE_UPLOAD:
            return -1
        else:
            return Constants.PAGE_GENERAL

    def set_canceled(self, canceled):
        self.canceled = canceled

    @property
    def available_files(self):
        available_files = []

        for upload in self.page(Constants.PAGE_FILES).get_uploads():
            available_files.append(upload.target)

        return available_files

    @property
    def available_directories(self):
        return self.page(Constants.PAGE_FILES).get_directories()

    @property
    def program(self):
        return self.page(Constants.PAGE_UPLOAD).program

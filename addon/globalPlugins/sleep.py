# A global plugin to sleep the pc  after given time and stop sayall.
# Copyright Derek Riemer, Quin Marilyn 2016-2021
# All of the terms that apply to the NVDA license apply for this plugin.

from threading import Timer
import globalPluginHandler
import speech.sayAll
import speech
import subprocess
import wx
import gui

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	_timer = None

	def _hibernate(self):
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		si.wShowWindow = subprocess.SW_HIDE
		self._proc = subprocess.Popen(["shutdown.exe", "/h"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=si)

	def _stopSayAll(self):
		""" Thread function to stop sayall. Also initiates hibernate."""
		self._timer = None
		if speech.sayAll.SayAllHandler.isRunning():
			speech.cancelSpeech()
		if self._hibernateAfter:
			self._hibernate()

	def script_userQueryTime(self, gesture):
		d = wx.TextEntryDialog(gui.mainFrame, "Enter the number of minutes to wait before stopping sayall and hybernating.", "Reading is fun")
		def callback(result):
			if result != wx.ID_OK:
				return

			hibernate = gui.messageBox("Hibernate after say all?", "Reading is awesome!", style=wx.YES | wx.NO)
			self._hibernateAfter = hibernate == wx.YES
			if self._timer:
				self._timer.cancel()
				self._timer = None
			self._timer = Timer(float(d.GetValue())*60, self._stopSayAll)
			self._timer.start()
		gui.runScriptModalDialog(d, callback)

	script_userQueryTime.__doc__ = "Stops sayAll after the given time, and puts the computer in hibernate mode."

	def terminate(self):
		if self._timer:
			self._timer.cancel()

	__gestures = {
		"kb:nvda+/" : "userQueryTime",
	}

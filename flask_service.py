import win32serviceutil
import win32service
import win32event
import servicemanager
import os
from subprocess import Popen

class FlaskAppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask App Windows Service"
    _svc_description_ = "Runs a Flask application as a Windows Service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.process:
            self.process.terminate()

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Starting Flask application...")
        self.run()

    def run(self):
        venv_path = r"C:\root\dev\src\trust-app\venv\Scripts"
        app_path = r"C:\root\dev\src\trust-app\myapp.py"

        # Activate virtual environment and run Flask app using Waitress
        self.process = Popen(
            [os.path.join(venv_path, "python.exe"), app_path],
            cwd=os.path.dirname(app_path),
        )
        self.process.wait()


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FlaskAppService)

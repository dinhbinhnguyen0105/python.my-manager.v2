# src/robot/browser_worker.py
from time import sleep
from typing import List, Tuple, Dict, Optional, Callable
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal

import io, pycurl, json
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright
from undetected_playwright import Tarnished
from playwright_stealth import stealth_sync

from src.my_types import RobotTaskType, SucceededType, FailedType
from src.robot.browser_actions import ACTION_MAP


class WorkerSignals(QObject):
    success_signal = pyqtSignal(SucceededType)
    error_signal = pyqtSignal(FailedType)
    invalid_proxy_signal = pyqtSignal(dict)
    finished = pyqtSignal(RobotTaskType)


class BrowserWorker(QRunnable):
    def __init__(
        self,
        proxy_url: Optional[str],
        task: Optional[RobotTaskType],
        callback: Callable,
    ):
        super().__init__()
        self._proxy_url = proxy_url
        self._task = task
        self._callback = callback
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        # fetch proxy
        proxy = None
        try:
            proxy_res = get_proxy(self._proxy_url)

            if proxy_res.get("status") != 100:
                self.signals.invalid_proxy_signal.emit(
                    {
                        "status": proxy_res.get("status"),
                        "message": proxy_res.get("message"),
                        "task": self._task,
                        "proxy_url": self._proxy_url,
                    }
                )
                print("Finished with invalid proxy.")
                self.finished.emit(self._task)
                return False
            proxy = proxy_res.get("data")

        except Exception as e:
            print(f"[{self.__class__.__name__}.run] Error: {e}")
            self.signals.error_signal.emit(
                FailedType(
                    user_info=self._task.user_info,
                    udd=self._task.udd,
                    headless=self._task.headless,
                    action_name=self._task.action_name,
                    error_message="Error fetching proxy. Check log.",
                )
            )
        # fetch action
        try:
            if self._task.action_name not in ACTION_MAP.keys():
                raise ValueError(f"Invalid action name: {self._task.action_name}.")
            action_func = ACTION_MAP[self._task.action_name]
            if self._task:
                print(f"Running uid [{self._task.user_info.uid}] with proxy [{proxy}].")
                # action_name = "launch_browser"
                with sync_playwright() as p:
                    # user_agent = (self.browser_info.user_agent,)

                    context = p.chromium.launch_persistent_context(
                        user_data_dir=self._task.udd,
                        headless=self._task.headless,
                        args=["--disable-blink-features=AutomationControlled"],
                        ignore_default_args=["--enable-automation"],
                        proxy=proxy,
                    )
                    Tarnished.apply_stealth(context)
                    page = context.new_page()
                    if self._task.action_name == "launch_browser":
                        action_func(page, self._task, self.signals)

                self.signals.success_signal.emit(
                    SucceededType(
                        headless=self._task.headless,
                        user_info=self._task.user_info,
                        udd=self._task.udd,
                        action_name=self._task.action_name,
                        is_success=True,
                    )
                )
        except Exception as e:
            print(f"[{self.__class__.__name__}.run] Error: {e}")
            # self.signals.error_signal.emit(FailedType(
            #     user_info=self._tasks
            # ))
            return False
        finally:
            self._callback(self._proxy_url)
            self.signals.finished.emit(self._task)


def get_proxy(proxy_url: str) -> dict:
    buffer = io.BytesIO()
    curl = pycurl.Curl()
    # https://proxyxoay.shop/api/get.php?key=[keyxoay]&&nhamang=random&&tinhthanh=0
    curl.setopt(pycurl.URL, proxy_url)
    curl.setopt(pycurl.CONNECTTIMEOUT, 60)
    curl.setopt(pycurl.TIMEOUT, 60)
    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-US,en;q=0.9",
        "Referer: https://proxyxoay.shop/",
        "Connection: keep-alive",
    ]
    curl.setopt(pycurl.HTTPHEADER, headers)
    curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
    curl.perform()
    try:
        code = curl.getinfo(pycurl.RESPONSE_CODE)
        if code != 200:
            return {"status": code, "message": "Error fetching proxy"}
        body = buffer.getvalue().decode("utf-8")
        res = json.loads(body)
        data = None
        if res.get("status") == 100 and "proxyhttp" in res:
            raw = res["proxyhttp"]
            ip, port, user, pwd = raw.split(":", 3)
            # proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
            data = {
                "username": user,
                "password": pwd,
                "server": f"{ip}:{port}",
            }

        return {
            "data": data,
            "status": res.get("status"),
            "message": res.get("message"),
        }
    except Exception as e:
        print(f"[get_proxy] Error: {e}")
        raise e

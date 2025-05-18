from time import sleep
from typing import Optional
from PyQt6.QtCore import QRunnable

import io, pycurl, json
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright
from undetected_playwright import Tarnished

from src.my_types import RobotTaskType, BrowserWorkerSignals
from src.robot.browser_actions import ACTION_MAP


class BrowserWorker(QRunnable):

    def __init__(
        self,
        task: Optional[RobotTaskType],
        proxy: str,
    ):
        super().__init__()
        self.task = task
        self.raw_proxy = proxy
        self.signals = BrowserWorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            proxy = None

            try:
                res = get_proxy(self.raw_proxy)
                if int(res.get("status")) == 100:
                    proxy = res.get("data")
                elif int(res.get("status")) == 101:
                    proxy = None
                    print(
                        f"[{self.task.user_info.uid}] Not ready proxy ({self.raw_proxy})"
                    )
                    sleep(60)
                    self.signals.proxy_not_ready_signal.emit(self.task, self.raw_proxy)
                elif int(res.get("status")) == 102:
                    proxy = None
                    self.signals.proxy_unavailable_signal.emit(
                        self.task, self.raw_proxy
                    )
            except Exception as e:
                self.signals.error_signal.emit(
                    self.task,
                    f"An error occurred while fetching proxy: {e}",
                )

            if proxy and self.task.action_name in ACTION_MAP.keys():
                action_func = ACTION_MAP[self.task.action_name]
                with sync_playwright() as p:
                    context = p.chromium.launch_persistent_context(
                        user_data_dir=self.task.udd,
                        headless=self.task.headless,
                        args=["--disable-blink-features=AutomationControlled"],
                        ignore_default_args=["--enable-automation"],
                        proxy=proxy,
                    )
                    Tarnished.apply_stealth(context)
                    page = context.new_page()
                    if self.task.action_name == "launch_browser":
                        action_func(page, self.task, self.signals)

                self.signals.succeeded_signal.emit(
                    self.task, self.raw_proxy, "Succeeded."
                )
        except Exception as e:
            self.signals.error_signal.emit(self.task, "message")


def get_proxy(proxy_url: str) -> dict:
    buffer = io.BytesIO()
    curl = pycurl.Curl()
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
        parsed_url = urlparse(proxy_url)
        domain = parsed_url.netloc
        if domain == "proxyxoay.shop":
            if res.get("status") == 100 and "proxyhttp" in res:
                raw = res["proxyhttp"]
                ip, port, user, pwd = raw.split(":", 3)
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
        raise Exception(e)

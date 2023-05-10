#!/usr/bin/python3
"""
rofi-auto-desk.py

a simple python script for applying auto-desk layouts.


By: Calacuda | MIT License | Epoch 
"""


# import argparse
import socket
import os
import sys
import tomllib


LAYOUT_EXT = {"layout", "yml", "yaml"}

def api_send(payload: str) -> bool:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(auto_desk_socket())  # TODO: add path to socket file  
            s.send(bytes(payload, 'ascii'))
            s.shutdown(1)  # tells the server im done sending data and it can reply now.
            res = s.recv(1024)  # .decode('utf-8')
            try:
                # TODO: make this use mycroft to say "Loading layout ___"
                return int(res[0]) == 0
            except IndexError:
                return True


def load_layout(layout: str) -> bool:
    layout = ".".join(os.path.basename(layout).split(".")[:-1])
    return api_send(f"load-layout {layout}")


def auto_desk_socket() -> str:
    with open(os.path.expanduser("~/.config/desktop-automater/config.toml"), "rb") as f:
        data = tomllib.load(f)
        return data.get("server").get("listen_socket")


def is_layout_f(layout: str) -> bool:
    """returns true if the file is a layout file"""
    return layout.split(".")[-1] in LAYOUT_EXT


def print_layouts(directory: str) -> None:
    """prints all the layouts in dir"""
    layouts = os.listdir(directory)
    layouts.sort()
    [print(layout) for layout in layouts if is_layout_f(layout)]


def main():
    if is_layout_f(sys.argv[-1]):
        # print("loading layout")
        load_layout(sys.argv[-1])
    else:
        # print("printing layouts")
        print_layouts(os.path.expanduser("~/.config/desktop-automater/layouts/"))


if __name__ == "__main__":
    main()
#!/usr/bin/python

# jack-alsa-ctl
# Copyright (C) 2022 DCsunset
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import re
from pathlib import Path
import subprocess
from enum import Enum
from .lib import get_volume_cmd, mute_cmd, mic_mute_cmd, raise_volume_cmd, lower_volume_cmd, get_jack_device, list_cards

def error(msg: str):
	print(msg, file=sys.stderr)
	sys.exit(1)
	
def run_cmd(cmd: list[str] | str):
	if isinstance(cmd, list):
		for c in cmd:
			subprocess.run(c, shell=True)
	else:
		subprocess.run(cmd, shell=True)


volume_types = ("Capture", "Playback")

def get_volume(volume_type: str):
	if volume_type not in volume_types:
		error(f"Invalid volume type: {volume_type}")

	res = subprocess.run(get_volume_cmd(), shell=True, capture_output=True)
	out = res.stdout.decode("utf-8")
	# filter capture volume
	regex = re.compile(f"{volume_type}.*\\[\\d?\\d?\\d%\\]")
	print("\n".join(
		map(
			lambda l: l.strip(),
			filter(
				lambda l: regex.search(l) is not None,
				out.splitlines()
			)
		)
	))

def main():
	if len(sys.argv) < 2:
		error("Usage: audio_cmd.py <cmd> [args]")

	cmd = sys.argv[1]

	if cmd == "list_cards":
		max_num = 0
		if len(sys.argv) == 3:
			max_num = int(sys.argv[2])
		elif len(sys.argv) > 3:
			error("Invalid num of args")
		print("\n".join(list_cards(max_num)))

	elif cmd == "get_device":
		print(get_jack_device())

	elif cmd == "get_volume":
		volume_type = "Playback"
		if len(sys.argv) == 3:
			volume_type = sys.argv[2]
		elif len(sys.argv) > 3:
			error("Invalid num of args")
		get_volume(volume_type)

	elif cmd == "mute":
		run_cmd(mute_cmd())

	elif cmd == "mic_mute":
		run_cmd(mic_mute_cmd())
		
	elif cmd == "raise_volume":
		step = 2
		if len(sys.argv) == 3:
			step = int(sys.argv[2])
		elif len(sys.argv) > 3:
			error("Invalid num of args")
		run_cmd(raise_volume_cmd(step))

	elif cmd == "lower_volume":
		step = 2
		if len(sys.argv) == 3:
			step = int(sys.argv[2])
		elif len(sys.argv) > 3:
			error("Invalid num of args")
		run_cmd(lower_volume_cmd(step))

	else:
		error(f"Invalid command: {cmd}")

if __name__ == "__main__":
	main()

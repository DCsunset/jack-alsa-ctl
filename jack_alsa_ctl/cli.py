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
from pathlib import Path
import subprocess
from .lib import get_volume_cmd, mute_cmd, mic_mute_cmd, raise_volume_cmd, lower_volume_cmd, get_jack_device, list_cards

def error(msg: str):
	print(msg, file=sys.stderr)
	sys.exit(1)

def get_volume():
	res = subprocess.run(get_volume_cmd(), shell=True, capture_output=True)
	out = res.stdout.decode("utf-8")
	print(out)
	# filter capture volume
	print("\n".join(filter(lambda l: "Capture" not in l, out.splitlines())))

def mute():
	subprocess.run(mute_cmd(), shell=True)

def mic_mute():
	subprocess.run(mic_mute_cmd(), shell=True)

def raise_volume(step: int):
	subprocess.run(raise_volume_cmd(step), shell=True)

def lower_volume(step: int):
	subprocess.run(lower_volume_cmd(step), shell=True)


def main():
	if len(sys.argv) < 2:
		error("Usage: audio_cmd.py <cmd> [args]")

	cmd = sys.argv[1]

	if cmd != "get_volume":
		with open("/tmp/audio_cmd.log", "a") as f:
			f.write(f"{Path().absolute()} {cmd}\n")

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
		get_volume()
	elif cmd == "mute":
		mute()
	elif cmd == "raise_volume":
		step = 2
		if len(sys.argv) == 3:
			step = int(sys.argv[2])
		elif len(sys.argv) > 3:
			error("Invalid num of args")
		raise_volume(step)
	elif cmd == "lower_volume":
		step = 2
		if len(sys.argv) == 3:
			step = int(sys.argv[2])
		elif len(sys.argv) > 3:
			error("Invalid num of args")
		lower_volume(step)
	else:
		print(f"Invalid command: {cmd}", file=sys.stderr)
		sys.exit(1)

if __name__ == "__main__":
	main()

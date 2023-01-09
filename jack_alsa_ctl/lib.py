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

import subprocess
import sys
import re

VOLUME_TYPES = ("Playback", "Capture")

global_options = {
	"card": ""	# Empty means using the default card 0
}

# List all sound cards
# max_num <= 0 means no limit
def list_cards(max_num: int = 0) -> list[str]:
	with open("/proc/asound/cards", "r") as f:
		out = f.read()
	regex = re.compile(r"\[\s*(.+?)\s*\]")
	cards = regex.findall(out)
	if max_num > 0:
		n = min(max_num, len(cards))
		# prioritize cards from the end
		# because they are external
		cards = cards[-n:]
	return cards
   

# Get current jack2 sound card using jack_control
def get_jack_card():
	print(global_options)
	# return the provided card
	if len(global_options["card"]) > 0:
		return global_options["card"]

	try:
		res = subprocess.run(["jack_control", "dp"], capture_output=True)
		if res.returncode != 0:
			return "0"
		lines = res.stdout.decode("utf-8").splitlines()
		for line in lines:
			l = line.strip()
			if l.startswith("device:"):
				# l[:-1] removes the last parathesis
				return l[:-1].split(":")[-1]
	except Exception as e:
		print(e, file=sys.stderr)
	# return default card on failure
	return "0"

# Set/change current jack card
def set_jack_card_cmd(dev: str) -> list[str]:
	return [
		f"jack_control dps device hw:{dev}",
		# Restart jack after setting dev
		"jack_control stop",
		"jack_control start"
	]

# Get scontrols of a sound card
def get_amixer_scontrols(card: str) -> list[str]:
	try:
		res = subprocess.run(["amixer", "-c", card, "scontrols"], capture_output=True)
		if res.returncode != 0:
			return []
			
		names = []
		lines = res.stdout.decode("utf-8").splitlines()
		p = re.compile(r"'(.+)'")
		for l in lines:
			# find the last occurrence of the quoted name
			name = p.search(l).groups()[-1]
			names.append(name)
		return names
	except Exception as e:
		print(e, file=sys.stderr)

	# return empty on failure
	return []

# Get volume types of a specific scontrol (check for Playback and Capture)
def get_scontrol_volume_types(card: str, scontrol: str) -> list[str]:
	try:
		res = subprocess.run(["amixer", "-c", card, "sget", scontrol], capture_output=True)
		if res.returncode != 0:
			return []
			
		types = []
		for volume_type in VOLUME_TYPES:
			regex = re.compile(f"{volume_type}.*\\[\\d?\\d?\\d%\\]")
			output = res.stdout.decode("utf-8")
			# find the last occurrence of the quoted name
			if len(regex.findall(output)) > 0:
				types.append(volume_type)
		return types
	except Exception as e:
		print(e, file=sys.stderr)

	# return empty on failure
	return []

	
# Get current volume scontrol and card for amixer
def get_current_control(volume_type: str) -> tuple[str, str]:
	card = get_jack_card()
	scontrols = get_amixer_scontrols(card)

	# possible scontrols for volume
	amixer_volume_scontrols = ["Master", "Headset", "Capture"]
	for sc in amixer_volume_scontrols:
		if sc in scontrols:
			types = get_scontrol_volume_types(card, sc)
			if volume_type in types:
				return card, sc
	
	print(f"No suitable amixer volume control for card {card}", file=sys.stderr)
	return card, ""

def get_volume_cmd(volume_type: str) -> str:
	card, scontrol = get_current_control(volume_type)
	return f"amixer -c '{card}' sget '{scontrol}'"

def toggle_cmd(volume_type: str) -> str:
	card, scontrol = get_current_control(volume_type)
	return f"amixer -c '{card}' sset '{scontrol}' '{volume_type}' toggle"

def lower_volume_cmd(volume_type: str, step: int) -> str:
	card, scontrol = get_current_control()
	return f"amixer -c '{card}' sset '{scontrol}' '{volume_type}' {step}-"

def raise_volume_cmd(volume_type: str, step: int) -> str:
	card, scontrol = get_current_control()
	return f"amixer -c '{card}' sset '{scontrol}' '{volume_type}' {step}+"


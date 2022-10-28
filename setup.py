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

from distutils.core import setup
from pathlib import Path

repo_dir = Path(__file__).parent.absolute()

# get version
main_ns = {}
with open(repo_dir.joinpath("jack_alsa_ctl", "_version.py")) as f:
	exec(f.read(), main_ns)

# Long description
readme = repo_dir.joinpath('README.md')
with open(readme, "r") as f:
	long_description = f.read()

setup(
	name="jack-alsa-ctl",
	version=main_ns["__version__"],
	description="Control JACK audio with ALSA driver easily",
	long_description=long_description,
	author="DCsunset",
	author_email='DCsunset@protonmail.com',
	license="AGPL-3.0",
	url="https://github.com/DCsunset/jack-alsa-ctl",
	packages=["jack_alsa_ctl"],
	scripts=["bin/jack-alsa-ctl"],
	classifiers=[
		"Environment :: Console",
		"Topic :: Multimedia :: Sound/Audio",
		'Intended Audience :: End Users/Desktop',
		'Programming Language :: Python',
		"License :: OSI Approved :: GNU Affero General Public License v3"
	]
)

# jack-alsa-ctl

[![PyPI](https://img.shields.io/pypi/v/jack-alsa-ctl)](https://pypi.org/project/jack-alsa-ctl/)

Control JACK audio with ALSA driver (or ALSA only) easily.

## Dependencies

`jack-alsa-ctl` depends on the following programs in your PATH:

* `jack_control` (only required by `get_card` and `set_card`)
* `amixer`

In addition, JACK server should be started and managed by jack_control and configured to use ALSA driver.


## Installation

From pypi (recommended):

```sh
pip install jack-alsa-ctl
```

From git repo (for dev version)

```sh
pip install git+https://github.com/DCsunset/jack-alsa-ctl
```

Or clone and install locally (for dev):

```sh
git clone https://github.com/DCsunset/jack-alsa-ctl
cd jack-alsa-ctl
pip install .
```

## Usage

### CLI

Use the command `jack-alsa-ctl` directly:

```sh
jack-alsa-ctl --help
jack-alsa-ctl get_card
jack-alsa-ctl get_volume
```

See help messages for more usage.

### Library

```py
from jack_alsa_ctl.lib import get_jack_card
print(get_jack_card())
```


## LICENSE

AGPL-3.0. Copyright notice:

    jack-alsa-ctl
    Copyright (C) 2022-2023 DCsunset

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


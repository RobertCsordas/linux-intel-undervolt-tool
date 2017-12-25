Intel CPU and GPU undervolting tool for linux
=============================================

Disclaimers
-----------

**THIS SCRIPT MAY PHYSICALLY DAMAGE YOUR SYSTEM. USE ONLY AT YOUR OWN RISK. I AM NOT RESPONSIBLE TO ANY DAMAGE CAUSED BY USING THESE SCRIPTS.**

Notes
-----

Should work with all i* CPUs that are newer or equal than 6th gen.

Tested for i7 7th gen CPU on XPS 15 9560. It seems to be stable with around -100mV for both CPU and GPU.

The script is based on an [tutorial which reverse engineered the MSR configuration used by the regulators](https://github.com/mihic/linux-intel-undervolt). There
is no official documentation available, so this is all based on guess-work and reverse engineering.

Installation
------------

Run ./install.sh as root. This will set up the config file, the systemd scripts and the script itself. **It also enables systemd startup**.
Edit /etc/undervolt.json and fill your values (in negative millivolts).

**Please always test your values** just by running sudo undervolt -cpu <value> -gpu <value> **before writing them to the config file, as if
may result in an unbootable system** if the voltages are switched to unstable value during boot time.

Requirements
------------

The script is written in python3. msr kernel module is required for accessing CPU MSR registers.

Checking the results
--------------------

CPU voltage can be checked with i7z util, by running it as root.
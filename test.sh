#!/bin/bash
python logs2netcdfs.py --help
python calibrate_align.py --help
python logs2netcdfs.py --auv_name Dorado389 --mission 2020.245.00 --portal http://stoqs.mbari.org:8080/auvdata/v1 -v
pytest
exit $?

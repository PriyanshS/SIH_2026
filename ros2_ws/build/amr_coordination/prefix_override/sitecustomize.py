import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/neer/Desktop/SIH/ros2_ws/install/amr_coordination'

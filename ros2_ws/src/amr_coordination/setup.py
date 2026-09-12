from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'amr_coordination'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SIH Team',
    maintainer_email='team@sih.org',
    description='Decentralized coordination nodes for warehouse AMR fleet',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'path_sharer = amr_coordination.path_sharer:main',
            'conflict_detector = amr_coordination.conflict_detector:main',
            'choke_negotiator = amr_coordination.choke_negotiator:main',
            'obstacle_relay = amr_coordination.obstacle_relay:main',
            'goal_sequencer = amr_coordination.goal_sequencer:main',
            'metrics_logger = amr_coordination.metrics_logger:main',
            'goal_dispatcher = amr_coordination.goal_dispatcher:main',
            'send_goal = amr_coordination.send_goal:main',
            'web_bridge_node = amr_coordination.web_bridge_node:main',
        ],
    },
)

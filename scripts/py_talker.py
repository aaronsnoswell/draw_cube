#!/usr/bin/env python

import math
import rospy
from raven_2.msg import raven_automove, raven_state


def main():
    rospy.init_node('py_talker')

    # Frequency to tick at
    # We also use the value for the length of the publisher queue
    # ANDY: For ROS Hyrdo, try with line 18 (below) commented out, as it is now
    tick_hz = 1000;
    pub = rospy.Publisher(
        '/raven_automove',
        raven_automove,
        #queue_size=tick_hz
    )

    # Scale of the velocity commands, units is microns
    scale = 3.0;

    # Record start time
    start_time = rospy.Time.now()

    rate = rospy.Rate(tick_hz)
    while not rospy.is_shutdown():

        # Make a new automove message
        msg = raven_automove()
        msg.hdr.stamp = rospy.Time.now()

        # Find elapsed time in seconds
        elapsed_time = (msg.hdr.stamp - start_time).to_sec()
        
        # Command velocity with 2*pi period (in seconds) sine wave
        pos = scale * math.sin(elapsed_time)
        msg.tf_incr[0].translation.y = pos
        msg.tf_incr[0].translation.z = pos
        msg.tf_incr[1].translation.y = pos
        msg.tf_incr[1].translation.z = pos

        # Make quaternions valid unit quaternions
        msg.tf_incr[0].rotation.w = 1.0
        msg.tf_incr[1].rotation.w = 1.0

        rospy.loginfo("Sending raven_automove")
        pub.publish(msg)

        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

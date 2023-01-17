# From equations to actions A system-level design research experience of an undergraduate student

## What each folder contains

* ### windows-scripts

The windows-scripts folder contains scripts that can be run on a windows computer using the windows webcam.

* ### jetbot-scripts

The jetbot-scripts folder contains scripts that require the jetbot to run due to Robot() library commands.

* ### media

The media folder contains demo images and videos.

## What each script does

* ### jetbot-segment

This script uses a single pixel intensity value, turns the image into grey scale and counts the number of pixels either above or below that threshhold.  It uses this counted area to calculate looming and move the jetbot forward or backward to maintain a looming value of zero.

* ### jetbot-contours/windows-contours

This script uses a range of pixel color values in HSV color space to single out the object we would like to track to calculate looming.  It then creates a window with a mask of the pixel values in that color range.  We then add a gausian blur to the video capture and go through each contour in the mask finding the largest one.  We display a green perimeter around the largest contour and use the area of the largest contour to calculate looming.  This looming value moves the jetbot forward or backward to maintain a looming value of 0.

* ### jetbot-follow/windows-follow

This script is an addition to jetbot-contours/windows-contours script but also tracks where on the screen the object being tracked for looming is by finding the center point of the largest contour.  The screen is split based on its width into 5 sections Left, Mid-left, Middle, Mid-right and Right and depending on which section the center point of the object is in the jetbot will veer in a certian direction.  Additionally, I added a range of values the jetbot will remain still for between -0.05 looming and 0.05 looming.

* ### jetbot-pid

This script is an update to the jetbot-follow script with the aim of eliminating the need for set sections of the screen [left, mid-left, center, mid-right and right] to control how much the jetbot turns to follow the object.  Instead we calculate an error value for how far off the jetbot is from having the object in the center of the screen and use that error to continuously adjust the left and right wheel values in the main while loop.

## Helpful links

Installing CURL and VSCode onto Jetson Nano
* https://youtu.be/Fegmuh6_mEg

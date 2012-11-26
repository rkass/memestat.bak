# Install script for directory: /home/ryan/OpenCV-2.4.2/include

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv" TYPE FILE FILES
    "/home/ryan/OpenCV-2.4.2/include/opencv/cxcore.h"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cxeigen.hpp"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cvaux.h"
    "/home/ryan/OpenCV-2.4.2/include/opencv/ml.h"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cxcore.hpp"
    "/home/ryan/OpenCV-2.4.2/include/opencv/highgui.h"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cvwimage.h"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cxmisc.h"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cvaux.hpp"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cv.hpp"
    "/home/ryan/OpenCV-2.4.2/include/opencv/cv.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2" TYPE FILE FILES "/home/ryan/OpenCV-2.4.2/include/opencv2/opencv.hpp")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")


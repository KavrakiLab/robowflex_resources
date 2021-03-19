cmake_minimum_required(VERSION 2.8.3)

# handling lesser cmake versions
cmake_policy(SET CMP0017 NEW)
if(NOT ${CMAKE_VERSION} VERSION_LESS 3.0.0)
  cmake_policy(SET CMP0042 NEW)
endif()

project(robowflex_resources)
find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY fetch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

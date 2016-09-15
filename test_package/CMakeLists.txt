cmake_minimum_required( VERSION 2.8.12 )
project( PackageTest )

include( ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake )
conan_basic_setup()

find_library(BREAKPAD NAMES Breakpad)
if (BREAKPAD)
  message(STATUS "BREAKPAD: ${BREAKPAD}")
endif()
if (NOT BREAKPAD)
  message(FATAL_ERROR "Breakpad not found")
endif()

add_executable( example example.cpp )
target_link_libraries( example ${BREAKPAD} )

file(COPY ${BREAKPAD} DESTINATION Frameworks)
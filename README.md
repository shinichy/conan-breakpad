# conan-breakpad
[Conan](https://conan.io) package for the breakpad library (https://chromium.googlesource.com/breakpad/breakpad/).

[![badge](https://img.shields.io/badge/conan.io-breakpad%2F1.0.0-green.svg?logo=data:image/png;base64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAA1VBMVEUAAABhlctjlstkl8tlmMtlmMxlmcxmmcxnmsxpnMxpnM1qnc1sn85voM91oM11oc1xotB2oc56pNF6pNJ2ptJ8ptJ8ptN9ptN8p9N5qNJ9p9N9p9R8qtOBqdSAqtOAqtR%2BrNSCrNJ/rdWDrNWCsNWCsNaJs9eLs9iRvNuVvdyVv9yXwd2Zwt6axN6dxt%2Bfx%2BChyeGiyuGjyuCjyuGly%2BGlzOKmzOGozuKoz%2BKqz%2BOq0OOv1OWw1OWw1eWx1eWy1uay1%2Baz1%2Baz1%2Bez2Oe02Oe12ee22ujUGwH3AAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfgBQkREyOxFIh/AAAAiklEQVQI12NgAAMbOwY4sLZ2NtQ1coVKWNvoc/Eq8XDr2wB5Ig62ekza9vaOqpK2TpoMzOxaFtwqZua2Bm4makIM7OzMAjoaCqYuxooSUqJALjs7o4yVpbowvzSUy87KqSwmxQfnsrPISyFzWeWAXCkpMaBVIC4bmCsOdgiUKwh3JojLgAQ4ZCE0AMm2D29tZwe6AAAAAElFTkSuQmCC)](http://www.conan.io/source/breakpad/1.0.0/shinichy/stable)

[![Build status](https://ci.appveyor.com/api/projects/status/9tg8injdma6q8vts?svg=true)](https://ci.appveyor.com/project/shinichy/conan-breakpad)

## Example

The following example shows how to use this Conan package with CMake.  See Conan's
documentation for other generators if you are not using CMake.

Add the package to your project's *conanfile.txt*:

```
[requires]
breakpad/1.0.0@shinichy/stable

[generators]
cmake
```

Your *CMakeLists.txt*:

```CMake
cmake_minimum_required( VERSION 2.8.12 )
project( PackageTest )

include( ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake )
conan_basic_setup()

if (APPLE)
  find_library(BREAKPAD NAMES Breakpad)
  if (NOT BREAKPAD)
    message(FATAL_ERROR "Breakpad not found")
  endif()
elseif (MSVC)
  find_package(BREAKPAD)
  if(NOT BREAKPAD_FOUND)
    message(FATAL_ERROR "Breakpad not found")
  endif ()
  set(CMAKE_CXX_FLAGS "/wd4091 /wd4577")
endif ()

add_executable( example example.cpp )

if (APPLE)
  target_link_libraries( example ${BREAKPAD} )
  file(COPY ${BREAKPAD} DESTINATION Frameworks)
elseif (MSVC)
  include_directories(${BREAKPAD_INCLUDE_DIRS})
  target_link_libraries( example ${BREAKPAD_LIBRARIES} )
endif ()
```

And then your *example.cpp*:

```cpp
#ifdef __APPLE__
#include "client/mac/handler/exception_handler.h"

static bool dumpCallback(const char* _dump_dir, const char* _minidump_id, void* context, bool success) {
  printf("Dump path: %s\n", _dump_dir);
  return success;
}
#endif

#ifdef _WIN32
#include "client/windows/handler/exception_handler.h"

bool dumpCallback(const wchar_t* _dump_dir,
                  const wchar_t* _minidump_id,
                  void* context,
                  EXCEPTION_POINTERS* exinfo,
                  MDRawAssertionInfo* assertion,
                  bool success) {
  wprintf(L"Dump path: %s\n", _dump_dir);
  return true;
}
#endif

void makeCrash() { volatile int* a = (int*)(NULL); *a = 1; }

int main(int argc, char* argv[]) {
#ifdef __APPLE__
  std::string path = "/tmp";
  google_breakpad::ExceptionHandler eh(path, NULL, dumpCallback, NULL, true, NULL);
#endif

#ifdef _WIN32
  std::wstring path = L"C:\\tmp";
  google_breakpad::ExceptionHandler eh(path, 0, dumpCallback, 0, google_breakpad::ExceptionHandler::HandlerType::HANDLER_ALL);
#endif

  makeCrash();
  return 0;
}

```

Then you can use it as:

```bash
$ mkdir build && cd build
$ conan install ..
$ cmake .. -G "Visual Studio 14 Win64"
$ cmake --build . --config Release
$ bin/example
```

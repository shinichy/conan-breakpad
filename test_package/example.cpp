#include "client/mac/handler/exception_handler.h"

static bool dumpCallback(const char* _dump_dir, const char* _minidump_id, void* context, bool success) {
  printf("Dump path: %s\n", _dump_dir);
  return success;
}

void makeCrash() { volatile int* a = (int*)(NULL); *a = 1; }

int main(int argc, char* argv[]) {
  std::string path = "/tmp";
  google_breakpad::ExceptionHandler eh(path, NULL, dumpCallback, NULL, true, NULL);
  makeCrash();
  return 0;
}

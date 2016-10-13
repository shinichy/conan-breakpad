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

int main(int argc, char* argv[]) {
#ifdef __APPLE__
  std::string path = "/tmp";
  google_breakpad::ExceptionHandler eh(path, NULL, dumpCallback, NULL, true, NULL);
#endif

#ifdef _WIN32
  std::wstring path = L"C:\\tmp";
  google_breakpad::ExceptionHandler eh(path, 0, dumpCallback, 0, google_breakpad::ExceptionHandler::HandlerType::HANDLER_ALL);
#endif

  return 0;
}

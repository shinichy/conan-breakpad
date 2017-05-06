from conans import ConanFile, AutoToolsBuildEnvironment
import os, shutil

class BreakpadConan( ConanFile ):
  name = 'breakpad'
  version = '1.0.0'
  license = 'https://chromium.googlesource.com/breakpad/breakpad/+/master/LICENSE'
  url = 'https://github.com/shinichy/conan-breakpad'
  settings = 'os', 'compiler', 'build_type', 'arch'
  generators = 'cmake'
  branch = 'chrome_53'
  exports = ["FindBREAKPAD.cmake", "patch/*"]

  def source( self ):
    self.run('git clone https://chromium.googlesource.com/breakpad/breakpad --branch %s --depth 1' % self.branch)
    if self.settings.os == 'Linux':
      self.run('git clone https://chromium.googlesource.com/linux-syscall-support breakpad/src/third_party/lss')

  def build( self ):
    if self.settings.os == 'Macos':
      arch = 'i386' if self.settings.arch == 'x86' else self.settings.arch
      self.run( 'xcodebuild -project breakpad/src/client/mac/Breakpad.xcodeproj -sdk macosx -target Breakpad ARCHS=%s ONLY_ACTIVE_ARCH=YES -configuration %s' % (arch, self.settings.build_type) )
    elif self.settings.os == 'Windows':
      self.run( 'cd breakpad & C:\\msys64\\usr\\bin\\patch -p1 --binary -N < ..\\patch\\common.gypi.patch' )
      self.run( 'gyp --no-circular-check -D win_release_RuntimeLibrary=2 -D win_debug_RuntimeLibrary=3 breakpad/src/client/windows/breakpad_client.gyp' )
      self.run( 'MSBuild.exe /p:Configuration=%s /p:VisualStudioVersion=%s breakpad/src/client/windows/common.vcxproj' % ( self.settings.build_type, self.settings.compiler.version ) )
      self.run( 'MSBuild.exe /p:Configuration=%s /p:VisualStudioVersion=%s /p:DisableSpecificWarnings="4091;2220" breakpad/src/client/windows/handler/exception_handler.vcxproj' % ( self.settings.build_type, self.settings.compiler.version ) )
      self.run( 'MSBuild.exe /p:Configuration=%s /p:VisualStudioVersion=%s breakpad/src/client/windows/crash_generation/crash_generation_client.vcxproj' % ( self.settings.build_type, self.settings.compiler.version ))
      self.run( 'MSBuild.exe /p:Configuration=%s /p:VisualStudioVersion=%s breakpad/src/client/windows/crash_generation/crash_generation_server.vcxproj' % ( self.settings.build_type, self.settings.compiler.version ))
      self.run( 'MSBuild.exe /p:Configuration=%s /p:VisualStudioVersion=%s breakpad/src/client/windows/sender/crash_report_sender.vcxproj' % ( self.settings.build_type, self.settings.compiler.version ))
    elif self.settings.os == 'Linux':
      env_build = AutoToolsBuildEnvironment(self)
      env_build.configure('breakpad/')
      env_build.make()

  def package( self ):
    self.copy("FindBREAKPAD.cmake", ".", ".")
    self.copy( '*.h', dst='include/common', src='breakpad/src/common' )

    if self.settings.os == 'Macos':
      self.copy( '*.h', dst='include/client/mac', src='breakpad/src/client/mac' )
      # self.copy doesn't preserve symbolic links
      shutil.copytree('breakpad/src/client/mac/build/%s/Breakpad.framework' % self.settings.build_type, os.path.join(self.package_folder, 'lib', 'Breakpad.framework'), symlinks=True)
    elif self.settings.os == 'Windows':
      self.copy( '*.h', dst='include/client/windows', src='breakpad/src/client/windows' )
      self.copy( '*.h', dst='include/google_breakpad', src='breakpad/src/google_breakpad' )
      self.copy( '*.lib', dst='lib', src='breakpad/src/client/windows/%s' % self.settings.build_type, keep_path=False )
      self.copy( '*.lib', dst='lib', src='breakpad/src/client/windows/handler/%s' % self.settings.build_type, keep_path=False )
      self.copy( '*.lib', dst='lib', src='breakpad/src/client/windows/crash_generation/%s' % self.settings.build_type, keep_path=False )
      self.copy( '*.lib', dst='lib', src='breakpad/src/client/windows/sender/%s' % self.settings.build_type, keep_path=False )
      self.copy( '*.exe', dst='bin', src='breakpad/src/tools/windows/binaries' )
    elif self.settings.os == 'Linux':
      self.copy("*.h", dst="include/client/linux", src="breakpad/src/client/linux")
      self.copy("*.h", dst="include/google_breakpad/", src="breakpad/src/google_breakpad")
      self.copy("*.h", dst="include/third_party/", src="breakpad/src/third_party")
      self.copy("*.a", dst="lib", src="src/client/linux")

  def package_info( self ):
    self.cpp_info.libs = ['breakpad']
    self.env_info.path.append(os.path.join(self.package_folder, "bin"))

from conans import ConanFile

class BreakpadConan( ConanFile ):
  name = 'breakpad'
  version = '1.0.0'
  license = 'https://chromium.googlesource.com/breakpad/breakpad/+/master/LICENSE'
  url = 'https://github.com/silkedit/conan-breakpad'
  settings = 'os', 'compiler', 'build_type', 'arch'
  generators = 'cmake'
  branch = 'chrome_53'

  def source( self ):
    self.run('git clone https://chromium.googlesource.com/breakpad/breakpad --branch %s --depth 1' % self.branch)

  def build( self ):
    if self.settings.os == 'Macos':
      self.run( 'xcodebuild -project breakpad/src/client/mac/Breakpad.xcodeproj -sdk macosx -target Breakpad ARCHS=x86_64 ONLY_ACTIVE_ARCH=YES -configuration %s' % self.settings.build_type )

  def package( self ):
    if self.settings.os == 'Macos':
      # Exclude Breakpad.framework/Versions because copy doesn't preserve symbolic links
      self.copy( 'Breakpad.framework*', dst='lib', src='breakpad/src/client/mac/build/%s' % self.settings.build_type )
#      self.copy( 'Breakpad.framework/Headers*', dst='lib', src='breakpad/src/client/mac/build/%s' % self.settings.build_type )
#      self.copy( 'Breakpad.framework/Resources*', dst='lib', src='breakpad/src/client/mac/build/%s' % self.settings.build_type )
      self.copy( '*.h', dst='include/client', src='breakpad/src/client' )
      self.copy( '*.h', dst='include/common', src='breakpad/src/common' ) 
    elif self.settings.os == 'Windows':    
      self.copy( '*breakpad*.lib', dst='lib', keep_path=False )
      self.copy( '*breakpad*.dll', dst='bin', keep_path=False )

  def package_info( self ):
    self.cpp_info.libs = ['breakpad']

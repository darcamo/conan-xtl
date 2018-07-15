import os

from conans import ConanFile, CMake, tools
import shutil


class XtlConan(ConanFile):
    name = "xtl"
    version = "0.4.12"
    license = "BSD-3"
    url = "https://github.com/darcamo/conan-xtl"
    description = "Basic tools (containers, algorithms) used by other quantstack packages"
    no_copy_source = True
    homepage = "https://github.com/QuantStack/xtl"
    generators = "cmake"
    # No settings/options are necessary, this is header only

    def requirements(self):
        self.requires("nlohmann-json/3.1.2@darcamo/stable")

    def source(self):
        '''retrieval of the source code here. Remember you can also put the code
        in the folder and use exports instead of retrieving it with this
        source() method
        '''
        tools.get("https://github.com/QuantStack/xtl/archive/{0}.zip".format(self.version))
        shutil.move("xtl-{0}".format(self.version), "sources")

        tools.replace_in_file("sources/CMakeLists.txt", "project(xtl)",
                              """project(xtl)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.install()

    def package_info(self):
        try:
            shutil.move("lib64", "lib")
        except Exception:
            pass

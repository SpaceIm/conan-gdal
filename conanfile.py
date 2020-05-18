import glob
import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools

class GdalConan(ConanFile):
    name = "gdal"
    description = "GDAL is an open source X/MIT licensed translator library " \
                  "for raster and vector geospatial data formats."
    license = "MIT"
    topics = ("conan", "gdal", "osgeo", "geospatial", "raster", "vector")
    homepage = "https://github.com/OSGeo/gdal"
    url = "https://github.com/conan-io/conan-center-index"
    exports_sources = "patches/**"
    generators = "pkg_config"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "simd_intrinsics": [None, "sse", "ssse3", "avx"],
        "threadsafe": [True, False],
        "with_zlib": [True, False],
        "with_lzma": [True, False],
        "with_zstd": [True, False],
        "with_pg": [True, False],
        "with_cfitsio": [True, False],
        "with_pcraster": [True, False],
        "with_png": [True, False], # still required ?
        # "with_dds": [True, False],
        "with_gta": [True, False],
        "with_pcidsk": [True, False],
        "with_jpeg": [True, False],
        "with_charls": [True, False],
        "with_gif": [True, False],
        # "with_ogdi": [True, False],
        # "with_fme": [True, False],
        # "with_sosi": [True, False],
        # "with_mongocxx": [True, False],
        "with_hdf4": [True, False],
        "with_hdf5": [True, False],
        # "with_netcdf": [True, False],
        "with_jasper": [True, False],
        "with_openjpeg": [True, False],
        # "with_fgdb": [True, False],
        # "with_mysql": [True, False],
        "with_xerces": [True, False],
        "with_expat": [True, False],
        "with_libkml": [True, False],
        # "with_odbc": [True, False],
        # "with_dods_root": [True, False],
        "with_curl": [True, False],
        "with_xml2": [True, False],
        # "with_spatialite": [True, False],
        "with_sqlite3": [True, False],
        # "with_rasterlite2": [True, False],
        "with_pcre": [True, False],
        # "with_epsilon": [True, False],
        "with_webp": [True, False],
        "with_geos": [True, False],
        # "with_sfcgal": [True, False],
        "with_qhull": [True, False],
        # "with_opencl": [True, False],
        # "with_freexl": [True, False],
        "without_pam": [True, False],
        "enable_pdf_plugin": [True, False],
        # "with_poppler": [True, False],
        # "with_podofo": [True, False],
        # "with_pdfium": [True, False],
        # "with_tiledb": [True, False],
        # "with_rasdaman": [True, False],
        # "with_armadillo": [True, False],
        # "with_cryptopp": [True, False],
        "with_crypto": [True, False],
        "without_lerc": [True, False],
        "with_null": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "simd_intrinsics": "sse",
        "threadsafe": True,
        "with_zlib": True,
        "with_lzma": False,
        "with_zstd": False,
        "with_pg": False,
        "with_cfitsio": False,
        "with_pcraster": False,
        "with_png": False,
        # "with_dds": True,
        "with_gta": False,
        "with_pcidsk": False,
        "with_jpeg": False,
        "with_charls": False,
        "with_gif": False,
        # "with_ogdi": True,
        # "with_fme": True,
        # "with_sosi": True,
        # "with_mongocxx": True,
        "with_hdf4": False,
        "with_hdf5": False,
        # "with_netcdf": True,
        "with_jasper": False,
        "with_openjpeg": False,
        # "with_fgdb": True,
        # "with_mysql": True,
        "with_xerces": False,
        "with_expat": False,
        "with_libkml": False,
        # "with_odbc": True,
        # "with_dods_root": True,
        "with_curl": False,
        "with_xml2": False,
        # "with_spatialite": False,
        "with_sqlite3": False,
        # "with_rasterlite2": False,
        "with_pcre": False,
        # "with_epsilon": False,
        "with_webp": False,
        "with_geos": False,
        # "with_sfcgal": True,
        "with_qhull": False,
        # "with_opencl": False,
        # "with_freexl": True,
        "without_pam": False,
        "enable_pdf_plugin": False,
        # "with_poppler": False,
        # "with_podofo": False,
        # "with_pdfium": False,
        # "with_tiledb": False,
        # "with_rasdaman": False,
        # "with_armadillo": False,
        # "with_cryptopp": True,
        "with_crypto": False,
        "without_lerc": True,
        "with_null": False,
    }

    _autotools= None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        if self.settings.os == "Linux":
            self.build_requires("autoconf/2.69")

    def requirements(self):
        self.requires("flatbuffers/1.12.0")
        self.requires("json-c/0.13.1")
        self.requires("libgeotiff/1.5.1")
        self.requires("libpng/1.6.37") # should be controlled by self.options.with_png, but MRT raster driver depends on it
        self.requires("libtiff/4.1.0")
        self.requires("proj/7.0.0")
        self.requires("shapelib/1.5.0")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11")
        if self.options.with_lzma:
            self.requires("xz_utils/5.2.4")
        if self.options.with_zstd:
            self.requires("zstd/1.4.4")
        if self.options.with_pg:
            self.requires("libpq/11.5")
        if self.options.with_cfitsio:
            self.requires("cfitsio/3.470")
        # if self.options.with_pcraster:
        #     self.requires("pcraster-rasterformat/x.x.x")
        # if self.options.with_dds:
        #     self.requires("crunch/x.x.x")
        if self.options.with_gta:
            self.requires("libgta/1.2.1")
        # if self.options.with_pcidsk:
        #     self.requires("pcidsk/x.x.x")
        if self.options.with_jpeg:
            self.requires("libjpeg/9d")
        if self.options.with_charls:
            self.requires("charls/2.1.0")
        if self.options.with_gif:
            self.requires("giflib/5.1.4")
        # if self.options.with_ogdi:
        #     self.requires("ogdi/x.x.x")
        # if self.options.with_fme:
        #     self.requires("fme/x.x.x")
        # if self.options.with_sosi:
        #     self.requires("fyba/x.x.x")
        # if self.options.with_mongocxx:
        #     self.requires("mongocxx/x.x.x")
        if self.options.with_hdf4:
            self.requires("hdf4/4.2.15")
        if self.options.with_hdf5:
            self.requires("hdf5/1.12.0")
        # if self.options.with_netcdf:
        #     self.requires("netcdf-c/x.x.x")
        if self.options.with_jasper:
            self.requires("jasper/2.0.16")
        if self.options.with_openjpeg:
            self.requires("openjpeg/2.3.1")
        # if self.options.with_fgdb:
        #     self.requires("file-geodatabase-api/x.x.x")
        # if self.options.with_mysql:
        #     self.requires("xxxx/x.x.x") # which one to use?
        if self.options.with_xerces:
            self.requires("xerces-c/3.2.2")
        if self.options.with_expat:
            self.requires("expat/2.2.9")
        if self.options.with_libkml:
            self.requires("libkml/1.3.0")
        # if self.options.with_dods_root:
        #     self.requires("libdap/x.x.x")
        if self.options.with_curl:
            self.requires("libcurl/7.69.1")
        if self.options.with_xml2:
            self.requires("libxml2/2.9.10")
        # if self.options.with_spatialite:
        #     self.requires("spatialite/x.x.x")
        if self.options.with_sqlite3:
            self.requires("sqlite3/3.31.1")
        # if self.options.with_rasterlite2:
        #     self.requires("rasterlite2/x.x.x")
        if self.options.with_pcre:
            self.requires("pcre/8.41")
        # if self.options.with_epsilon:
        #     self.requires("epsilon/x.x.x")
        if self.options.with_webp:
            self.requires("libwebp/1.1.0")
        if self.options.with_geos:
            self.requires("geos/3.8.1")
        # if self.options.with_sfcgal:
        #     self.requires("sfcgal/x.x.x")
        # if self.options.with_qhull:
        #     self.requires("qhull/x.x.x")
        # if self.options.with_freexl:
        #     self.requires("freexl/x.x.x")
        # if self.options.with_poppler:
        #     self.requires("poppler/x.x.x")
        # if self.options.with_podofo:
        #     self.requires("podofo/x.x.x")
        # if self.options.with_pdfium:
        #     self.requires("pdfium/x.x.x")
        # if self.options.with_tiledb:
        #     self.requires("tiledb/x.x.x")
        # if self.options.with_rasdaman:
        #     self.requires("raslib/x.x.x")
        # if self.options.with_armadillo:
        #     self.requires("armadillo/x.x.x")
        # if self.options.with_cryptopp:
        #     self.requires("cryptopp/x.x.x")
        if self.options.with_crypto:
            self.requires("openssl/1.1.1g")
        if not self.options.without_lerc:
            self.requires("lerc/2.1")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        configure_dir=os.path.join(self._source_subfolder, "gdal")
        with tools.chdir(configure_dir):
            self.run("autoconf -i")
        self._autotools = AutoToolsBuildEnvironment(self)

        args = []
        # Shared/Static
        if self.options.shared:
            args.extend(["--disable-static", "--enable-shared"])
        else:
            args.extend(["--disable-shared", "--enable-static"])
        # Debug
        if self.settings.build_type == "Debug":
            args.append("--enable-debug")
        # SIMD Intrinsics
        simd_intrinsics = self.options.get_safe("simd_intrinsics", False)
        if not simd_intrinsics:
            args.extend(["--without-sse", "--without-ssse3", "--without-avx"])
        elif simd_intrinsics == "sse":
            args.extend(["--with-sse", "--without-ssse3", "--without-avx"])
        elif simd_intrinsics == "ssse3":
            args.extend(["--with-sse", "--with-ssse3", "--without-avx"])
        elif simd_intrinsics == "avx":
            args.extend(["--with-sse", "--with-ssse3", "--with-avx"])
        # LTO (disabled)
        args.append("--disable-lto")
        # 
        args.append("--with-hide_internal_symbols")
        args.append("--without-rename-internal-libtiff-symbols")
        args.append("--without-rename-internal-libgeotiff-symbols")
        args.append("--without-rename-internal-shapelib-symbols")
        #
        args.append("--without-local")
        # Threadsafe
        args.append("--with-threads" if self.options.threadsafe else "--without-threads")
        # Mandatory dependencies:
        args.append("--with-proj=yes")
        # Optional dependencies:
        args.append("--with-libz={}".format(self.deps_cpp_info["zlib"].rootpath if self.options.with_zlib else "no"))
        args.append("--with-liblzma" if self.options.with_lzma else "--without-liblzma")
        args.append("--with-zstd={}".format(self.deps_cpp_info["zstd"].rootpath if self.options.with_zstd else "no"))
        # Drivers:
        args.append("--with-pg" if self.options.with_pg else "--without-libpq")
        args.extend(["--without-grass", "--without-libgrass"]) # GRASS (not supported in this recipe)
        args.append("--with-cfitsio={}".format(self.deps_cpp_info["cfitsio"].rootpath if self.options.with_cfitsio else "no"))
        args.append("--with-pcraster={}".format("internal" if self.options.with_pcraster else "no")) # TODO: args.append("--with-pcraster={}".format(self.deps_cpp_info["pcraster-rasterformat"].rootpath if self.options.with_pcraster else "no"))
        args.append("--with-png=external")
        args.append("--without-dds") # TODO: args.append("--with-dds={}".format(self.deps_cpp_info["crunch"].rootpath if self.options.with_dds else "no"))
        args.append("--with-gta={}".format(self.deps_cpp_info["libgta"].rootpath if self.options.with_gta else "no"))
        args.append("--with-pcidsk={}".format("internal" if self.options.with_pcidsk else "no")) # TODO: args.append("--with-pcidsk={}".format(self.deps_cpp_info["pcidsk"].rootpath if self.options.with_pcidsk else "no"))
        args.append("--with-libtiff=yes") # libtiff (required !)
        args.append("--with-geotiff=yes") # libgeotiff (required !)
        args.append("--with-jpeg={}".format(self.deps_cpp_info["libjpeg"].rootpath if self.options.with_jpeg else "no"))
        args.append("--with-charls={}".format("yes" if self.options.with_charls else "no"))
        args.append("--with-gif={}".format(self.deps_cpp_info["giflib"].rootpath if self.options.with_gif else "no"))
        args.append("--without-ogdi") # TODO: args.append("--with-ogdi={}".format(self.deps_cpp_info["ogdi"].rootpath if self.options.with_ogdi else "no"))
        args.append("--without-fme") # TODO: args.append("--with-fme={}".format(self.deps_cpp_info["fme"].rootpath if self.options.with_fme else "no"))
        args.append("--without-sosi") # TODO: args.append("--with-sosi={}".format(self.deps_cpp_info["fyba"].rootpath if self.options.with_sosi else "no"))
        args.append("--without-mongocxx") # TODO: args.append("--with-mongocxx={}".format(self.deps_cpp_info["mongocxx"].rootpath if self.options.with_mongocxx else "no"))
        args.append("--with-hdf4={}".format(self.deps_cpp_info["hdf4"].rootpath if self.options.with_hdf4 else "no"))
        args.append("--with-hdf5={}".format(self.deps_cpp_info["hdf5"].rootpath if self.options.with_hdf5 else "no"))
        args.append("--without-kea")
        args.append("--without-netcdf") # TODO: args.append("--with-netcdf={}".format(self.deps_cpp_info["netcdf-c"].rootpath if self.options.with_netcdf else "no"))
        args.append("--with-jasper={}".format(self.deps_cpp_info["jasper"].rootpath if self.options.with_jasper else "no"))
        args.append("--with-openjpeg={}".format("yes" if self.options.with_openjpeg else "no"))
        args.append("--without-fgdb") # TODO: args.append("--with-fgdb={}".format(self.deps_cpp_info["file-geodatabase-api"].rootpath if self.options.with_fgdb else "no"))
        args.append("--without-ecw") # commercial library
        args.append("--without-kakadu") # commercial library
        args.extend(["--without-mrsid", "--without-jp2mrsid", "--without-mrsid_lidar"]) # commercial library
        args.append("--without-jp2lura") # commercial library
        args.append("--without-msg") # commercial library
        args.append("--with-gnm") # ?
        args.append("--without-mysql") # TODO
        args.append("--without-ingres") # commercial library
        args.append("--with-xerces={}".format(self.deps_cpp_info["xerces-c"].rootpath if self.options.with_xerces else "no"))
        args.append("--with-expat={}".format(self.deps_cpp_info["expat"].rootpath if self.options.with_expat else "no"))
        args.append("--with-libkml={}".format(self.deps_cpp_info["libkml"].rootpath if self.options.with_libkml else "no"))
        args.append("--without-odbc") # TODO
        args.append("--without-dods-root") # libdap
        args.append("--with-curl={}".format(os.path.join(self.deps_cpp_info["libcurl"].bin_paths, "curl-config") if self.options.with_curl else "no"))
        args.append("--with-xml2={}".format(os.path.join(self.deps_cpp_info["libxml2"].bin_paths, "xml2-config") if self.options.with_xml2 else "no"))
        args.append("--without-spatialite") #
        args.append("--with-sqlite3={}".format(self.deps_cpp_info["sqlite3"].rootpath if self.options.with_sqlite3 else "no")) # TODO: Probably broken
        args.append("--without-rasterlite2") # TODO: args.append("--with-rasterlite2={}".format(self.deps_cpp_info["rasterlite2"].rootpath if self.options.with_rasterlite2 else "no"))
        args.append("--with-pcre={}".format("yes" if self.options.with_pcre else "no"))
        args.append("--without-teigha") # commercial library
        args.append("--without-idb") # commercial library
        args.append("--without-sde") # commercial library
        args.append("--without-epsilon") # TODO: args.append("--with-epsilon={}".format(self.deps_cpp_info["epsilon"].rootpath if self.options.with_epsilon else "no"))
        args.append("--with-webp={}".format(self.deps_cpp_info["libwebp"].rootpath if self.options.with_webp else "no"))
        args.append("--with-geos={}".format(os.path.join(self.deps_cpp_info["geos"].bin_paths, "geos-config") if self.options.with_geos else "no")) # TODO: Probably broken
        args.append("--without-sfcgal") # TODO: args.append("--with-sfcgal={}".format(self.deps_cpp_info["sfcgal"].rootpath if self.options.with_sfcgal else "no")) # Probably broken
        args.append("--with-qhull={}".format("internal" if self.options.with_qhull else "no"))
        args.append("--without-opencl") # TODO
        args.append("--without-freexl") # TODO: args.append("--with-freexl={}".format(self.deps_cpp_info["freexl"].rootpath if self.options.with_freexl else "no"))
        args.append("--with-libjson-c=yes") # jsonc-c (required !)
        if self.options.without_pam:
            args.append("--without-pam")
        if self.options.enable_pdf_plugin:
            args.append("--enable-pdf-plugin")
        args.append("--without-poppler") # TODO: args.append("--with-poppler={}".format(self.deps_cpp_info["poppler"].rootpath if self.options.with_poppler else "no"))
        args.append("--without-podofo") # TODO: args.append("--with-podofo={}".format(self.deps_cpp_info["podofo"].rootpath if self.options.with_podofo else "no"))
        args.append("--without-pdfium") # TODO: args.append("--with-pdfium={}".format(self.deps_cpp_info["pdfium"].rootpath if self.options.with_pdfium else "no"))
        args.append("--without-perl")
        args.append("--without-python")
        args.append("--without-java")
        args.append("--without-hdfs")
        args.append("--without-tiledb") # TODO: args.append("--with-tiledb={}".format(self.deps_cpp_info["tiledb"].rootpath if self.options.with_tiledb else "no"))
        args.append("--without-mdb")
        args.append("--without-rasdaman") # TODO: args.append("--with-rasdaman={}".format(self.deps_cpp_info["raslib"].rootpath if self.options.with_rasdaman else "no"))
        args.append("--without-armadillo") # TODO: args.append("--with-armadillo={}".format(self.deps_cpp_info["armadillo"].rootpath if self.options.with_armadillo else "no"))
        args.append("--without-cryptopp") # TODO: args.append("--with-cryptopp={}".format(self.deps_cpp_info["cryptopp"].rootpath if self.options.with_cryptopp else "no"))
        args.append("--with-crypto={}".format(self.deps_cpp_info["openssl"].rootpath if self.options.with_crypto else "no"))
        args.append("--with-lerc={}".format("no" if self.options.without_lerc else "yes")) # TODO: use lerc from conan, not internal one ?
        if self.options.with_null:
            args.append("--with-null")

        with tools.chdir(configure_dir):
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        autotools = self._configure_autotools()
        with tools.chdir(os.path.join(self._source_subfolder, "gdal")):
            autotools.make()

    def package(self):
        self.copy("LICENSE.TXT", dst="licenses", src=os.path.join(self._source_subfolder, "gdal"))
        autotools = self._configure_autotools()
        with tools.chdir(os.path.join(self._source_subfolder, "gdal")):
            autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "gdalplugins"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        for la_file in glob.glob(os.path.join(self.package_folder, "lib", "*.la")):
            os.remove(la_file)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "GDAL"
        self.cpp_info.names["cmake_find_package_multi"] = "GDAL"
        self.cpp_info.names["pkg_config"] = "gdal"
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["m", "pthread"])
        if not self.options.shared and self._stdcpp_library:
            self.cpp_info.system_libs.append(self._stdcpp_library)

    @property
    def _stdcpp_library(self):
        libcxx = self.settings.get_safe("compiler.libcxx")
        if libcxx in ("libstdc++", "libstdc++11"):
            return "stdc++"
        elif libcxx in ("libc++",):
            return "c++"
        else:
            return False


import time
from StringIO import StringIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


class FakeFile(StringIO):
    files = []

    def __init__(self, filename, mode='r'):
        self.filename = filename
        StringIO.__init__(self)
        self.files.append(self)

    def close(self):
        pass

    def really_close(self):
        StringIO.close(self)

    def __repr__(self):
        return "FakeFile(%s)" % self.filename

    @classmethod
    def zip(cls):
        now = time.localtime(time.time())
        zipio = StringIO()
        zipfile = ZipFile(zipio, 'w', ZIP_DEFLATED)
        for file in cls.files:
            zipinfo = ZipInfo(file.filename, date_time=now)
            zipinfo.external_attr = 0644 << 16L
            zipfile.writestr(zipinfo, file.getvalue())
        zipfile.close()
        return zipio
        
    @classmethod
    def clear(cls):
        for file in cls.files:
            file.really_close()
        del cls.files[:]

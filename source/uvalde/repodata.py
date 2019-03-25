import pathlib

import createrepo_c


def createrepo(base: pathlib.Path):
    if not base.exists() or not base.is_dir():
        raise FileExistsError(f'No such directory: {base}')

    repodata = Repodata(base)

    # gather packages
    all_rpm_files = set(base.glob('**/*.rpm'))
    debug_rpm_files = set(base.glob('debug/**/*.rpm'))
    rpm_files = sorted(all_rpm_files - debug_rpm_files)

    repodata.set_num_of_pkgs(len(rpm_files))

    for rpm_file in rpm_files:
        pkg = createrepo_c.package_from_rpm(f'{rpm_file}')
        pkg.location_href = f'{rpm_file.relative_to(base)}'
        repodata.add_pkg(pkg)

    repodata.save()


class Repodata:
    __slots__ = ['path', 'primary', 'filelists', 'other']

    def __init__(self, parent: pathlib.Path):
        self.path = parent / 'repodata'
        if not self.path.exists():
            self.path.mkdir()

        self.primary = Primary(self.path)
        self.filelists = Filelists(self.path)
        self.other = Other(self.path)

    def set_num_of_pkgs(self, num: int):
        self.primary.xml.set_num_of_pkgs(num)
        self.filelists.xml.set_num_of_pkgs(num)
        self.other.xml.set_num_of_pkgs(num)

    def add_pkg(self, pkg: createrepo_c.Package):
        self.primary.xml.add_pkg(pkg)
        self.filelists.xml.add_pkg(pkg)
        self.other.xml.add_pkg(pkg)

    def save(self):
        self.primary.xml.close()
        self.filelists.xml.close()
        self.other.xml.close()

        repomd = createrepo_c.Repomd()
        repomd.set_record(self.primary.get_record())
        repomd.set_record(self.filelists.get_record())
        repomd.set_record(self.other.get_record())

        with (self.path / 'repomd.xml').open(mode='w') as f:
            f.write(repomd.xml_dump())


class XmlGzFile:
    __slots__ = ['name', 'xml_class', 'path', 'xml']

    def __init__(self, parent: pathlib.Path):
        self.path = (parent / self.name).with_suffix('.xml.gz')
        if self.path.exists():
            self.path.unlink()
        self.xml = self.xml_class(f'{self.path}')

    def get_record(self) -> createrepo_c.RepomdRecord:
        record = createrepo_c.RepomdRecord(self.name, f'{self.path}')
        record.fill(createrepo_c.SHA256)
        return record


class Primary(XmlGzFile):
    name = 'primary'
    xml_class = createrepo_c.PrimaryXmlFile


class Filelists(XmlGzFile):
    name = 'filelists'
    xml_class = createrepo_c.FilelistsXmlFile


class Other(XmlGzFile):
    name = 'other'
    xml_class = createrepo_c.OtherXmlFile

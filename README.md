# uvalde: yum repository management tool

[![build status](https://api.cirrus-ci.com/github/carlwgeorge/uvalde.svg)](https://cirrus-ci.com/github/carlwgeorge/uvalde/master)

Uvalde is a simple CLI tool for managing yum repositories.  There is no daemon
and no web interface, just a directory of yum repositories and a small sqlite
database to remember what RPMs were built from the same SRPM.

![Garner State Park](https://tpwd.texas.gov/state-parks/garner/gallery/GARNER-SP_HDR_3941.jpg)

## Usage

#### Configuration

Before running the application, create a config file to define the repositories
you want to manage.  The base directory doesn't need to exist yet, uvalde will
create it if needed.

`~/.config/uvalde/repos.ini`
```ini
[my-repo]
base = /home/me/my-repo
architectures = i686, x86_64

[my-other-repo]
base = /home/me/my-other-repo
architectures = i686, x86_64
```
```
$ uvalde list repos
my-repo
my-other-repo
```

Now you can import RPM files and they will be placed at the appropriate
locations relative to your repository base.  Repository metadata will also be
generated.

```
$ uvalde import --repo my-repo cello-*.rpm
importing RPMs
generating repodata
```

The relationships between RPMs and SRPMs are stored in an sqlite database so
that you can manage the files collectively, referencing them by the NVR
(name-version-release) string.  When RPMs are moved the repository metadata
will be regenerated as needed.

```
$ uvalde list all
my-repo
  cello-1.0-1
my-other-repo
```
```
$ uvalde move --from my-repo --to my-other-repo cello-1.0-1
moving RPMs
generating repodata
```
```
$ uvalde list all
my-repo
my-other-repo
  cello-1.0-1
```
```
$ uvalde remove --repo my-other-repo cello-1.0-1
deleting RPMs
generating repodata
```
```
$ uvalde list all
my-repo
my-other-repo
```

## Installation

RPM packages coming soon!  In the meantime, you can install from source.

#### Install the [createrepo_c build dependencies](https://github.com/rpm-software-management/createrepo_c/blob/master/README.md#building)

* Fedora:

```
dnf install cmake gcc make bzip2-devel expat-devel file-devel glib2-devel libcurl-devel libxml2-devel openssl-devel python3-devel rpm-devel sqlite-devel xz-devel zlib-devel
```

* CentOS:

```
yum install cmake gcc make bzip2-devel expat-devel file-devel glib2-devel libcurl-devel libxml2-devel openssl-devel python36-devel rpm-devel sqlite-devel xz-devel zlib-devel
```

#### Clone the repository

```
git clone https://github.com/carlwgeorge/uvalde.git
cd uvalde
```

#### Create a virtual environment

```
python3 -m venv .env
```

#### Install in editable mode

```
.env/bin/pip install --editable .
```

#### Optional: install testing dependencies

```
.env/bin/pip install --editable .[tests]
```

#### Optional: add command to PATH

```
ln -s $PWD/.env/bin/uvalde ~/.local/bin/
```

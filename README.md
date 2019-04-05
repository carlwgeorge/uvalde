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
$ uvalde import my-repo cello-*.rpm
cello-1.0-1.i686.rpm -> /home/me/my-repo/i686/packages/c/
cello-1.0-1.src.rpm -> /home/me/my-repo/src/packages/c/
cello-1.0-1.x86_64.rpm -> /home/me/my-repo/x86_64/packages/c/
cello-debuginfo-1.0-1.i686.rpm -> /home/me/my-repo/i686/debug/packages/c/
cello-debuginfo-1.0-1.x86_64.rpm -> /home/me/my-repo/x86_64/debug/packages/c/
cello-debugsource-1.0-1.i686.rpm -> /home/me/my-repo/i686/debug/packages/c/
cello-debugsource-1.0-1.x86_64.rpm -> /home/me/my-repo/x86_64/debug/packages/c/
cello-extra-1.0-1.noarch.rpm -> /home/me/my-repo/i686/packages/c/
cello-extra-1.0-1.noarch.rpm -> /home/me/my-repo/x86_64/packages/c/
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
$ uvalde move my-repo my-other-repo cello-1.0-1
/home/me/my-repo/i686/packages/c/cello-1.0-1.i686.rpm -> /home/me/my-other-repo/i686/packages/c/
/home/me/my-repo/src/packages/c/cello-1.0-1.src.rpm -> /home/me/my-other-repo/src/packages/c/
/home/me/my-repo/x86_64/packages/c/cello-1.0-1.x86_64.rpm -> /home/me/my-other-repo/x86_64/packages/c/
/home/me/my-repo/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm -> /home/me/my-other-repo/i686/debug/packages/c/
/home/me/my-repo/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm -> /home/me/my-other-repo/x86_64/debug/packages/c/
/home/me/my-repo/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm -> /home/me/my-other-repo/i686/debug/packages/c/
/home/me/my-repo/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm -> /home/me/my-other-repo/x86_64/debug/packages/c/
/home/me/my-repo/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm -> /home/me/my-other-repo/x86_64/packages/c/
/home/me/my-repo/i686/packages/c/cello-extra-1.0-1.noarch.rpm -> /home/me/my-other-repo/i686/packages/c/
```
```
$ uvalde list all
my-repo
my-other-repo
  cello-1.0-1
```
```
$ uvalde remove my-other-repo cello-1.0-1
/home/me/my-other-repo/i686/packages/c/cello-1.0-1.i686.rpm X
/home/me/my-other-repo/src/packages/c/cello-1.0-1.src.rpm X
/home/me/my-other-repo/x86_64/packages/c/cello-1.0-1.x86_64.rpm X
/home/me/my-other-repo/i686/debug/packages/c/cello-debuginfo-1.0-1.i686.rpm X
/home/me/my-other-repo/x86_64/debug/packages/c/cello-debuginfo-1.0-1.x86_64.rpm X
/home/me/my-other-repo/i686/debug/packages/c/cello-debugsource-1.0-1.i686.rpm X
/home/me/my-other-repo/x86_64/debug/packages/c/cello-debugsource-1.0-1.x86_64.rpm X
/home/me/my-other-repo/i686/packages/c/cello-extra-1.0-1.noarch.rpm X
/home/me/my-other-repo/x86_64/packages/c/cello-extra-1.0-1.noarch.rpm X
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

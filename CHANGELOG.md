# 2.0.1

* Re-add createrepo\_c and selinux dependencies

# 2.0.0

* Remove `config show` command
* Rename `import` command to `add`
* Add `index` command
* Add hidden config option to hide some repos by default
* New database schema and new database filename
* Add prefix config option to customize directory structure

# 1.1.1

* Fix bug in NVR label creation

# 1.1.0

* Combine `list` commands
* Restore selinux context on imported files

# 1.0.0

* Remove empty parent directories when removing nvrs
* Use progress bars for visual feedback
* Add `--name` flag to filter list output
* Rename `--keep-original` flag to just `--keep`
* Convert repo arguments to prompted options (`--repo`, `--from`, and `--to`)

# 0.3.0

* Add `uvalde config show` command
* Abort import on unconfigured architecture
* Add `uvalde remove` command
* Improve test coverage

# 0.2.0

* Defer database initialization until runtime
* Add tests
* Fix Python 3.6 compatibility
* Record all artifacts for noarch packages in database

# 0.1.0

* Initial release

[![Build Status](https://travis-ci.org/AnObfuscator/WireMockManager.svg?branch=master)](https://travis-ci.org/AnObfuscator/WireMockManager)

## Introduction

WireMock Manager (WMM) is a tool for managing multiple WireMock instances, and managing the recorded or created output files in a consistent manner. WMM expects (and can create) a specific directory structure. It also needs a local copy of the standalone WireMock jar, which WMM will download if necessary.

## Installation

Install with pip from GitHub:

```
pip install -e git+https://github.com/AnObfuscator/WireMockManager.git#egg=WireMockManager
```

## Usage
Note that you can also get usage help from the wmm command line:

```
wmm -h
wmm [command] -h
```

### Mocking
```
wmm mock --api=service_name --version=service_version --port=1234 --https-port=2345
```

Start an instance of WireMock to mock of the specified API and version. This will serve the defined behaviors located in the directory 'services/[api]/[version]'. If 'services/[api]/[version]' does not exist, this command will return with an error.

### Recording
```
wmm record --url=http://url.to.service --name=[service_name] --version=[service_version] --port=1234 --https-port=2345
```

Start an instance to record the calls to the specified URL. Name and version can be anything you like, as long as they are valid directory names for your OS.  The recorded interactions will be stored in the directory 'recordings/[name]/[version]'. If you do not specify a name, it will be filed under 'unknown'. If you do not specify a version, it will be versioned with a UNIX timestamp.

*Warning:* If 'recordings/[name]/[version]' already exists, some existing content may be overwritten. 


### Status
```
wmm status
```

List all running instances as a table, with type (record/mock), api, version, url (if recording), port, and https port.

### Stop
```
wmm stop
```

Stop all running instances.

### Setup
```
wmm setup
```

Setup WMM folder structure in the current directory. Specifically, this will create directories called 'services' and 'recordings', if they are missing. In addition, this will create directories 'wmm/logs' and 'wmm/libs'. If the WireMock jar is not in 'wmm/libs', this will download the WM jar into that directory.


## WMM Directory Structure
```
(WorkingDir)
  -- services
  -- recordings
  -- wmm
     -- [lib]
         -- [wiremock.jar]
     -- [logs]
         -- [services]
         -- [recordings]
```

If services or recordings is missing, directory structure is 'invalid'

If ```[wmm/lib]``` or ```[wmm/logs]``` is missing, directory structure is 'uninitialized'
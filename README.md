Introduction

WireMock Manager (WMM) is a tool for managing multiple WireMock instances, and managing the recorded or created output files in a consistent manner.
WMM expects (and can create) a specific directory structure. It also needs a local copy of the standalone WireMock jar, which WMM will download if necessary.

Installation

Install with pip from GitHub:
```
pip install -e git+https://github.com/AnObfuscator/WireMockManager.git#egg=WireMockManager
```

Usage

```
wmm start --api=service_name --version=service_version --port=1234 --https-port=2345
```

```
wmm record --url=http://url.to.service --name=[service_name] --version=[service_vesion]
```

```
wmm status
```

```
wmm stop
```

```
wmm setup
```

<a name="readme-top"></a>

<!-- PROJECT NAME -->
<br />
<div align="center">
  <h3 align="center">tinyCUCM</h3>
  <p align="center">Cisco Unified Call Manager AXL Methods Collection.</p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
    <summary>Table of Contents</summary>
    <ol>
        <li><a href="#about-the-project">About The Project</a></li>
        <li><a href="#installation">Installation</a></li>
        <li>
            <a href="#usage">Usage</a>
            <ul>
                <li><a href="#instance-create">Instance Create</a></li>
                <li><a href="#axl-collection">AXL Collection</a></li>
                <ul>
                    <li><a href="#get-methods">Get Methods</a></li>
                    <li><a href="#remove-methods">Remove Methods</a></li>
                    <li><a href="#update-methods">Update Methods</a></li>
                </ul>
                <li><a href="#sql-collection">SQL Collection</a></li>
                <li><a href="#create-yor-own-methods">Create Your Own Methods</a></li>
            </ul>
        </li>
        <li><a href="#license">License</a></li>
        <li><a href="#contact">Contact</a></li>
    </ol>
</details>

---

<!-- ABOUT THE PROJECT -->
## About The Project

This project is for informational purposes only and is intended to study the capabilities of the Cisco Unified Call Manager's API. 
Methods have been tested on CUCM ver. 11.5.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- INSTALLATION -->
## Installation

Installation is as simple as:

   ```sh
   pip install tinyCUCM
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage



### Instance Create

Download `Cisco AXL Toolkit` from the station (`Application` -> `Plugins`) and put it into the folder with your project.
Create a new instance of the `CucmAxlClient` class and assigns this object to the local variable `cucm`.

<span style="color:#ff0000">**Don't store sensitive information in source code. For example use ".env" file.**</span>

```python
from pathlib import Path
from tinyCUCM import CucmAxlClient


BASE_DIR = Path(__file__).resolve().parent
settings = {
    "pub_fqdn": "cucm.example.com",
    "pub_version": "11.5",
    "user_login": "Your-CUCM-Account",
    "user_password": "You%wILL#&neVeR!gUEss",
    "toolkit_path": BASE_DIR / "axlsqltoolkit",
    "cert_path": BASE_DIR / "cucm.crt",
    "session_verify": False,
    "session_timeout": 15,
}

if __name__ == "__main__":
    cucm = CucmAxlClient(**settings)
    # Get All AXL Method Names
    print(cucm.axlAllMethods())

# (
#     'addAarGroup', 
#     'addAdvertisedPatterns', 
#     'addAnnouncement', 
#     'addAppServerInfo', 
#     'addAppUser', 
#     ...,
#     'updateWifiHotspot', 
#     'updateWirelessAccessPointControllers', 
#     'updateWlanProfileGroup', 
#     'wipePhone'
# )
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### AXL Collection

#### Get Methods

Common `Get` Methods:
* `axlGetDeviceProfile` -  expected: `uuid` or `name`
* `axlGetLine` - expected: `uuid` or `pattern` or `pattern` and `routePartitionName`
* `axlGetPhone` - expected: `uuid` or `name`
* `axlGetRemoteDestination` - expected: `uuid` or `destination`
* `axlGetRemoteDestinationProfile` - expected: `uuid` or `name`
* `axlGetTranslationPattern` - expected: `uuid` or `pattern` or `pattern` and `routePartitionName`

```python
cucm = ...
print("Result:", cucm.axlGetPhone(**{"uuid": "........-....-....-....-............"}))
# Result: {
#     'name': '...',
#     ...,  
#     'lines': {
#         'line': [
#             {
#                 'index': 1,
#                  ...,
#                 'dirn': {
#                     'pattern': '...',
#                     'routePartitionName': {'_value_1': '...', 'uuid': '{........-....-....-....-............}'},
#                     'uuid': '{........-....-....-....-............}'
#                 },
#                 'uuid': '{........-....-....-....-............'
#             }
#         ], 
#         'lineIdentifier': None
#     }, 
#     'uuid': '{........-....-....-....-............}'
# }
```

#### Remove Methods

Common `Remove` Methods:
* `axlRemoveDeviceProfile` -  expected: `uuid` or `name`
* `axlRemoveLine` - expected: `uuid` or `pattern` or `pattern` and `routePartitionName`
* `axlRemovePhone` - expected: `uuid` or `name`
* `axlRemoveRemoteDestination` - expected: `uuid` or `destination`
* `axlRemoveRemoteDestinationProfile` - expected: `uuid` or `name`
* `axlRemoveTranslationPattern` - expected: `uuid` or `pattern` or `pattern` and `routePartitionName`

```python
cucm = ...
print("Result:", cucm.axlRemoveLine(**{"uuid": "........-....-....-....-............"}))
# Result: {
#     'return': '{........-....-....-....-............}',
#     'sequence': None
# }
# Result: {"uuid": "...", ..., "": ""} 
```

#### Update Methods

```python
cucm = ...
print("Result:", cucm)
# Result: {"uuid": "...", ..., "": ""} 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### SQL Collection

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Create Your Own Methods

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Luarvick - lu.luarvick@gmail.com

Project Link: [https://github.com/luarvick/tinyCUCM](https://github.com/luarvick/tinyCUCM)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

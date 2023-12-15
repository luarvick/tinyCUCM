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
                    <li><a href="#add-methods">Add Methods</a></li>
                    <li><a href="#do-methods">Do Methods</a></li>
                    <li><a href="#get-methods">Get Methods</a></li>
                    <li><a href="#remove-methods">Remove Methods</a></li>
                    <li><a href="#update-methods">Update Methods</a></li>
                </ul>
                <li><a href="#sql-collection">SQL Collection</a></li>
                <ul>
                    <li><a href="#execute-query">Execute Query</a></li>
                    <li><a href="#update-query">Update Query</a></li>
                    <li><a href="#predefined-queries">Predefined Queries</a></li>
                </ul>
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
Methods have been tested on CUCM ver. 11.5.\
[Cisco UCM AXL Schemas & SQL Data Dictionaries Documentation](https://developer.cisco.com/docs/axl/#!archived-references)

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

Download `Cisco AXL Toolkit` from the station (`Application` -> `Plugins`) and put it into the folder with your project.\
Create an Cisco UCM application account or local end user with `Standard CCM Super Users` privileges (Assing Access Control Group to `Your-CUCM-Account`).\
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

#### Add Methods

Common `Add` Methods:

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Do Methods

Common `Do` Methods:
* `axlDoAuthenticateUser` -  expected keys: (`userid`, `password`) or (`userid`, `pin`)
* `axlDoDeviceLogin` -  expected keys: (`deviceName`, `loginDuration`, `profileName`, `userId`)\
    Key `loginDuration: str = "0"` - Logout disabled\
    Key `loginDuration: str = "36000"` - Logout after 10h
* `axlDoDeviceLogout` -  expected keys: `deviceName`
* `axlDoLdapSync` -  expected keys: (`uuid`, `sync`) or (`name`, `sync`)\
    Key `sync: bool = True` - Start Synchronization\
    Key `sync: bool = False` - Cancel the Synchronization which is currently under process

```python
cucm = ...
print("Result:", cucm.axlDoAuthenticateUser(**{"userid": "...", "password": "..."}))
# Result: {'return': {'userAuthenticated': 'true', 'code': 0, 'daysToExpiry': 0, 'isWarningNeeded': 'false'}, 'sequence': None}
# Result: {'return': {'userAuthenticated': 'false', 'code': 1, 'daysToExpiry': 0, 'isWarningNeeded': 'false'}, 'sequence': None}

print("Result:", cucm.axlDoDeviceLogin(**{"deviceName": "SEP...", "loginDuration": "...", "profileName":"...", "userid": "..."}))
# Result {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlDoDeviceLogout(**{"deviceName": "SEP..."}))
# Result {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlDoLdapSync(**{"uuid": "........-....-....-....-............", "sync": True}))
# Result: {'return': 'Sync initiated successfully', 'sequence': None}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Get Methods

Common `Get` Methods:
* `axlGetDeviceProfile` -  expected keys: `uuid` or `name`
* `axlGetLine` - expected keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetPhone` - expected keys: `uuid` or `name`
* `axlGetRemoteDestination` - expected keys: `uuid` or `destination`
* `axlGetRemoteDestinationProfile` - expected keys: `uuid` or `name`
* `axlGetTranslationPattern` - expected keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Remove Methods

Common `Remove` Methods:
* `axlRemoveDeviceProfile` -  expected keys: `uuid` or `name`
* `axlRemoveLine` - expected keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemovePhone` - expected keys: `uuid` or `name`
* `axlRemoveRemoteDestination` - expected keys: `uuid` or `destination`
* `axlRemoveRemoteDestinationProfile` - expected keys: `uuid` or `name`
* `axlRemoveTranslationPattern` - expected keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)

```python
cucm = ...
print("Result:", cucm.axlRemoveLine(**{"uuid": "........-....-....-....-............"}))
# Result: {
#     'return': '{........-....-....-....-............}',
#     'sequence': None
# }
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Update Methods

Common `Update` Methods:

```python
cucm = ...
print("Result:", cucm)
# Result: {"uuid": "........-....-....-....-............", ...,} 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### SQL Collection


#### Execute Query

```python
cucm = ...
sql_query = """
    SELECT d.pkid, d.name, d.description
    FROM device d
    WHERE d.name LIKE '%your_value%'
"""
print(cucm.sqlExecuteQuery(sql_query=sql_query))
# Result: (
#     {'pkid': '........-....-....-....-............', 'name': 'SEP...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'RDP...', 'description': '...'}, 
#     {'pkid': '........-....-....-....-............', 'name': 'UDP...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'TCT...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'BOT...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'CSF...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'TAB...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'CIPC...', 'description': '...'},
# )
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Update Query

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Predefined Queries

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Create Your Own Methods

<span style="color:#ff0000">**Don't store sensitive information in source code. For example use ".env" file.**</span>

```python
from pathlib import Path
from typing import Union
from tinyCUCM import CucmSettings, cucm_logging


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


class CucmAxlCustom(CucmSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @cucm_logging
    def axlYourOwnGetMethod(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Your Own Get Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return self._axl.getCallManager(**kwargs)["return"]

if __name__ == "__main__":
    cucm = CucmAxlCustom(**settings)
    print("Result:", cucm.axlYourOwnGetMethod(**{"uuid": "........-....-....-....-............"}))
    # Result: {
    #     'callManager': {
    #         'name': 'CM_...',
    #         'description': '...',
    #         'autoRegistration': {
    #             'startDn': None,
    #             'endDn': None,
    #             'nextDn': None,
    #             'routePartitionName': {
    #                 '_value_1': None,
    #                 'uuid': None
    #             },
    #             'e164Mask': None,
    #             'autoRegistrationEnabled': None,
    #             'universalDeviceTemplate': {
    #                 '_value_1': None,
    #                 'uuid': None
    #             },
    #             'lineTemplate': {
    #                 '_value_1': None,
    #                 'uuid': None
    #             }
    #         },
    #         'ports': {
    #             'ethernetPhonePort': ...,
    #             'mgcpPorts': {
    #                 'listen': ...,
    #                 'keepAlive': ...
    #             },
    #             'sipPorts': {
    #                 'sipPhonePort': ...,
    #                 'sipPhoneSecurePort': ...
    #             }
    #         },
    #         'processNodeName': {
    #             '_value_1': '...',
    #             'uuid': '{........-....-....-....-............}'
    #         },
    #         'lbmGroup': {
    #             '_value_1': None,
    #             'uuid': None
    #         },
    #         'ctiid': ...,
    #         'uuid': '{........-....-....-....-............}'
    #     }
    # }
```

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

from enum import Enum
from pydantic import BaseModel, model_validator
from typing import Optional, Self


""" ######################################################### """
""" ************** TINY CUCM SQL SEARCH MODELS ************** """
""" ######################################################### """


class CucmSqlBaseSearchModel(BaseModel):
    value: Optional[str] = None


########################################################################################################################


CUCM_SQL_SEARCH_CALL_PICKUP_GROUPS_CRITERIA = {
    "Name": "cpg.name",
    "Description": "npg.description",
    "Pattern": "npg.dnorpattern",
    "Line Number": "npm.dnorpattern",
    "Line Description": "npm.description",
}

class CucmSqlSearchCallPickupGroupsEnum(str, Enum):
    name = "Name"
    description = "Description"
    pattern = "Pattern"
    line_number = "Line Number"
    line_description = "Line Description"

class CucmSqlSearchCallPickupGroupsModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchCallPickupGroupsEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_CALL_PICKUP_GROUPS_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_DEVICES_CRITERIA = {
    "Name": "d.name",
    "Description": "d.description",
    "Line Number": "np.dnorpattern",
    "Line Description": "np.description",
    "User ID": "eu.userid",
    "Device Pool": "dp.name",
    "Device Type": "tprod.name",
}

class CucmSqlSearchDevicesEnum(str, Enum):
    name = "Name"
    description = "Description"
    line_number = "Line Number"
    line_description = "Line Description"
    user_id = "User ID"
    device_pool = "Device Pool"
    device_type = "Device Type"

class CucmSqlSearchDevicesModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchDevicesEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_DEVICES_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_END_USERS_CRITERIA = {
    "User ID": "eu.userid",
    "Display Name": "eu.displayname",
    "Last Name": "eu.lastname",
    "First Name": "eu.firstname",
    "Phone Number": "eu.telephonenumber",
    "Mobile Number": "eu.mobile",
    "Email": "eu.mailid",
    "Directory URI": "eu.directoryuri",
}

class CucmSqlSearchEndUsersEnum(str, Enum):
    user_id = "User ID"
    display_name = "Display Name"
    last_name = "Last Name"
    first_name = "First Name"
    phone_number = "Phone Number"
    mobile_number = "Mobile Number"
    email = "Email"
    directory_uri = "Directory URI"

class CucmSqlSearchEndUsersModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchEndUsersEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_END_USERS_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_LINE_FORWARDS_CRITERIA = {
    "Line Number": "np.dnorpattern",
    "Line Description": "np.description",
    "Forward Destination": "np.cf"
}

class CucmSqlSearchLineForwardsEnum(str, Enum):
    line_number = "Line Number"
    line_description = "Line Description"
    forward_destination = "Forward Destination"

class CucmSqlSearchLineForwardsModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchLineForwardsEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_LINE_FORWARDS_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_LINE_GROUPS_CRITERIA = {
    "Name": "lg.name",
    "Line Number": "np.dnorpattern",
    "Line Description": "np.description",
}

class CucmSqlSearchLineGroupsEnum(str, Enum):
    name = "Name"
    line_number = "Line Number"
    line_description = "Line Description"

class CucmSqlSearchLineGroupsModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchLineGroupsEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_LINE_GROUPS_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_LINE_NUMBERS_CRITERIA = {
    "Line Number": "np.dnorpattern",
    "Line Description": "np.description",
    "Partition": "rp.name",
    "Calling Search Space": "css.name",
    "Alerting Name": "np.alertingname",
    "Alerting Name ASCII": "np.alertingnameascii",
}

class CucmSqlSearchLineNumbersEnum(str, Enum):
    line_number = "Line Number"
    line_description = "Line Description"
    partition = "Partition"
    css = "Calling Search Space"
    alertingname = "Alerting Name"
    alertingnameascii = "Alerting Name ASCII"

class CucmSqlSearchLineNumbersModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchLineNumbersEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_LINE_NUMBERS_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_PATTERNS_CRITERIA = {
    "Pattern": "np.dnorpattern",
    "Description": "np.description",
    "Partition": "rp.name",
    "Calling Search Space": "css.name",
    "Pattern Usage": "tpu.enum"
}

class CucmSqlSearchPatternsEnum(str, Enum):
    pattern = "Pattern"
    description = "Description"
    partition = "Partition"
    css = "Calling Search Space"
    pattern_usage = "Pattern Usage"

class CucmSqlSearchPatternsModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchPatternsEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_PATTERNS_CRITERIA[self.criterion]

    @model_validator(mode="after")
    def check_pattern_usage_value(self) -> Self:
        if self.criterion == CucmSqlSearchPatternsEnum.pattern_usage:
            if not self.value:
                raise ValueError("The 'value' field must be a non-empty digits string when criterion is 'Pattern Usage'.")

            if not self.value.isdigit():
                raise ValueError("The 'value' must contain only digits and be between 0-30 or equal 104 or 105.")

            int_value = int(self.value)
            if not (0 <= int_value <= 30 or int_value in (104, 105)):
                raise ValueError("The 'value' must be between 0-30 or equal 104 or 105.")
        return self


########################################################################################################################


CUCM_SQL_SEARCH_REMOTE_DESTINATIONS_CRITERIA = {
    "Name": "rd.name",
    "Remote Destination": "rdd.destination",
}

class CucmSqlSearchRemoteDestinationsEnum(str, Enum):
    name = "Name"
    remote_destination = "Remote Destination"

class CucmSqlSearchRemoteDestinationsModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchRemoteDestinationsEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_REMOTE_DESTINATIONS_CRITERIA[self.criterion]


########################################################################################################################


CUCM_SQL_SEARCH_TRANSLATION_PATTERNS_CRITERIA = {
    "Pattern": "np.dnorpattern",
    "Description": "np.description",
    "Partition": "rp.name",
    "Calling Search Space": "css.name",
    "Called Party Transform Mask": "np.calledpartytransformationmask",
    "Prefix Digits Out": "np.prefixdigitsout",
}

class CucmSqlSearchTranslationPatternsEnum(str, Enum):
    pattern = "Pattern"
    description = "Description"
    partition = "Partition"
    css = "Calling Search Space"
    cptm = "Called Party Transform Mask"
    pdo = "Prefix Digits Out"

class CucmSqlSearchTranslationPatternsModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchTranslationPatternsEnum

    @property
    def sql_criterion(self):
        return CUCM_SQL_SEARCH_TRANSLATION_PATTERNS_CRITERIA[self.criterion]

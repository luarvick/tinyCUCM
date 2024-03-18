from enum import Enum
from pydantic import BaseModel, model_validator


CUCM_SQL_SEARCH_CALL_PICKUP_GROUP_CRITERIA = {
    "Name": "cpg.name",
    "Description": "npg.description",
    "Pattern": "npg.dnorpattern",
    "Member Line Number": "npm.dnorpattern",
    "Member Line Description": "npm.description",
}
CUCM_SQL_SEARCH_DEVICE_CRITERIA = {
    "Name": "d.name",
    "Description": "d.description",
    "Line Number": "np.dnorpattern",
    "Line Description": "np.description",
    "Userid": "eu.userid",
    "Device Pool": "dp.name",
    "Device Type": "tprod.name",
}
CUCM_SQL_SEARCH_END_USER_CRITERIA = {
    "Userid": "eu.userid",
    "Display Name": "eu.displayname",
    "Last Name": "eu.lastname",
    "First Name": "eu.firstname",
    "Phone Number": "eu.telephonenumber",
    "Mobile Number": "eu.mobile",
    "Email": "eu.mailid",
    "Directory URI": "eu.directoryuri",
}
CUCM_SQL_SEARCH_LINE_GROUP_CRITERIA = {
    "Name": "lg.name",
    "Member Line Number": "np.dnorpattern",
    "Member Line Description": "np.description",
}
CUCM_SQL_SEARCH_REMOTE_DESTINATION_CRITERIA = {
    "Name": "rd.name",
    "Destination": "rdd.destination",
}
CUCM_SQL_SEARCH_TRANSLATION_PATTERN_CRITERIA = {
    "Pattern": "np.dnorpattern",
    "Description": "np.description",
    "Partition": "rp.name",
    "Calling Search Space": "css.name",
    "Called Party Transform Mask": "np.calledpartytransformationmask",
    "Prefix Digits Out": "np.prefixdigitsout",
}


""" ######################################################### """
""" ****************** TINY CUCM SQL ENUMS ****************** """
""" ######################################################### """


class CucmSqlSearchCallPickupGroupEnum(str, Enum):
    name = "Name"
    description = "Description"
    pattern = "Pattern"
    member_line_number = "Member Line Number"
    member_line_description = "Member Line Description"


class CucmSqlSearchDeviceEnum(str, Enum):
    name = "Name"
    description = "Description"
    line_number = "Line Number"
    line_description = "Line Description"
    userid = "Userid"
    device_pool = "Device Pool"
    device_type = "Device Type"


class CucmSqlSearchEndUserEnum(str, Enum):
    userid = "Userid"
    display_name = "Display Name"
    last_name = "Last Name"
    first_name = "First Name"
    phone_number = "Phone Number"
    mobile_number = "Mobile Number"
    email = "Email"
    directory_uri = "Directory URI"


class CucmSqlSearchLineGroupEnum(str, Enum):
    name = "Name"
    member_line_number = "Member Line Number"
    member_line_description = "Member Line Description"


class CucmSqlSearchRemoteDestinationEnum(str, Enum):
    name = "Name"
    destination = "Destination"


class CucmSqlSearchTranslationPatternEnum(str, Enum):
    pattern = "Pattern"
    description = "Description"
    partition = "Partition"
    css = "Calling Search Space"
    cptm = "Called Party Transform Mask"
    pdo = "Prefix Digits Out"


""" ######################################################### """
""" ****************** TINY CUCM SQL MODELS ***************** """
""" ######################################################### """


class CucmSqlBaseSearchModel(BaseModel):
    value: str


class CucmSqlSearchCallPickupGroupModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchCallPickupGroupEnum

    @model_validator(mode="after")
    def check_fields(self):
        self.criterion = CUCM_SQL_SEARCH_CALL_PICKUP_GROUP_CRITERIA[self.criterion]
        return self


class CucmSqlSearchDeviceModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchDeviceEnum

    @model_validator(mode="after")
    def check_fields(self):
        self.criterion = CUCM_SQL_SEARCH_DEVICE_CRITERIA[self.criterion]
        return self.criterion


class CucmSqlSearchEndUserModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchEndUserEnum

    @model_validator(mode="after")
    def check_fields(self):
        self.criterion = CUCM_SQL_SEARCH_END_USER_CRITERIA[self.criterion]
        return self


class CucmSqlSearchLineGroupModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchLineGroupEnum

    @model_validator(mode="after")
    def check_fields(self):
        self.criterion = CUCM_SQL_SEARCH_LINE_GROUP_CRITERIA[self.criterion]
        return self


class CucmSqlSearchRemoteDestinationModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchRemoteDestinationEnum

    @model_validator(mode="after")
    def check_fields(self):
        self.criterion = CUCM_SQL_SEARCH_REMOTE_DESTINATION_CRITERIA[self.criterion]
        return self


class CucmSqlSearchTranslationPatternModel(CucmSqlBaseSearchModel):
    criterion: CucmSqlSearchTranslationPatternEnum

    @model_validator(mode="after")
    def check_fields(self):
        self.criterion = CUCM_SQL_SEARCH_TRANSLATION_PATTERN_CRITERIA[self.criterion]
        return self

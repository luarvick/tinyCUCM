from collections.abc import Iterable
from enum import Enum
from pydantic import BaseModel, model_validator
from typing import Union


""" ######################################################### """
""" ****************** TINY CUCM RIS MODELS ***************** """
""" ######################################################### """


class CucmRisCtiCollectionNameEnum(str, Enum):
    dev_names = "DevNames"
    dir_numbers = "DirNumbers"


class CucmRisCtiMgrClassEnum(str, Enum):
    provider = "Provider"
    device = "Device"
    line = "Line"


class CucmRisGetCtiModel(BaseModel):
    collection_name: CucmRisCtiCollectionNameEnum
    items_collection: Union[Iterable[dict], list[dict]]
    cti_mgr_class: CucmRisCtiMgrClassEnum = CucmRisCtiMgrClassEnum.line

    @model_validator(mode="after")
    def check_fields(self):
        match self.collection_name:
            case "DevNames":
                item_key = "name"
            case "DirNumbers":
                item_key = "pattern"

        self.items_collection = [
            {self.collection_name[0:-1]: item[item_key]} for item in self.items_collection
        ]
        return self

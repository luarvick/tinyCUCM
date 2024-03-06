from enum import Enum
from pydantic import BaseModel


""" ######################################################### """
""" ****************** TINY CUCM CCS MODELS ***************** """
""" ######################################################### """


class CucmCcsDoControlCommandsEnum(str, Enum):
    restart = "Restart"
    start = "Start"
    stop = "Stop"


class CucmCcsDoDeploymentCommandsEnum(str, Enum):
    deploy = "Deploy"
    undeploy = "UnDeploy"


class CucmCcsServiceListField(BaseModel):
    item: list[str]


class CucmCcsDoControlModel(BaseModel):
    # NodeName: str
    ControlType: CucmCcsDoControlCommandsEnum = CucmCcsDoControlCommandsEnum.restart
    ServiceList: CucmCcsServiceListField

    class Config:
        use_enum_values = True


class CucmCcsDoDeploymentModel(BaseModel):
    # NodeName: str
    DeployType: CucmCcsDoDeploymentCommandsEnum = CucmCcsDoDeploymentCommandsEnum.deploy
    ServiceList: CucmCcsServiceListField

    class Config:
        use_enum_values = True

# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/microsoft/winget-cli/master/schemas/JSON/manifests/v1.2.0/manifest.version.1.2.0.json
#   timestamp: 2022-08-09T12:21:34+00:00

from __future__ import annotations

from pydantic import BaseModel, Field, constr


class Model(BaseModel):
    PackageIdentifier: constr(
        regex=r'^[^\.\s\\/:\*\?"<>\|\x01-\x1f]{1,32}(\.[^\.\s\\/:\*\?"<>\|\x01-\x1f]{1,32}){1,3}$',
        max_length=128,
    ) = Field(..., description='The package unique identifier')
    PackageVersion: constr(
        regex=r'^[^\\/:\*\?"<>\|\x01-\x1f]+$', max_length=128
    ) = Field(..., description='The package version')
    DefaultLocale: constr(
        regex=r'^([a-zA-Z]{2,3}|[iI]-[a-zA-Z]+|[xX]-[a-zA-Z]{1,8})(-[a-zA-Z]{1,8})*$',
        max_length=20,
    ) = Field(..., description='The default package meta-data locale')
    ManifestType: str = Field(..., description='The manifest type')
    ManifestVersion: constr(
        regex=r'^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])(\.(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])){2}$'
    ) = Field(..., description='The manifest syntax version')

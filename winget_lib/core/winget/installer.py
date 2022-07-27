# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/microsoft/winget-cli/master/schemas/JSON/manifests/v1.1.0/manifest.installer.1.1.0.json
#   timestamp: 2022-07-27T01:31:46+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, conint, constr


class PackageIdentifier(BaseModel):
    __root__: constr(
        regex=r'^[^\.\s\\/:\*\?"<>\|\x01-\x1f]{1,32}(\.[^\.\s\\/:\*\?"<>\|\x01-\x1f]{1,32}){1,3}$',
        max_length=128,
    ) = Field(..., description='The package unique identifier')


class PackageVersion(BaseModel):
    __root__: constr(regex=r'^[^\\/:\*\?"<>\|\x01-\x1f]+$', max_length=128) = Field(
        ..., description='The package version'
    )


class Locale(BaseModel):
    __root__: Optional[
        constr(
            regex=r'^([a-zA-Z]{2,3}|[iI]-[a-zA-Z]+|[xX]-[a-zA-Z]{1,8})(-[a-zA-Z]{1,8})*$',
            max_length=20,
        )
    ] = Field(..., description='The installer meta-data locale')


class Channel(BaseModel):
    __root__: Optional[constr(min_length=1, max_length=16)] = Field(
        ..., description='The distribution channel'
    )


class PlatformEnum(Enum):
    Windows_Desktop = 'Windows.Desktop'
    Windows_Universal = 'Windows.Universal'

    class Config:
        use_enum_values = True


class Platform(BaseModel):
    __root__: List[PlatformEnum] = Field(
        ...,
        description='The installer supported operating system',
        max_items=2,
        unique_items=True,
    )


class MinimumOSVersion(BaseModel):
    __root__: Optional[
        constr(
            regex=r'^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])(\.(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])){0,3}$'
        )
    ] = Field(..., description='The installer minimum operating system version')


class InstallerType(Enum):
    msix = 'msix'
    msi = 'msi'
    appx = 'appx'
    exe = 'exe'
    zip = 'zip'
    inno = 'inno'
    nullsoft = 'nullsoft'
    wix = 'wix'
    burn = 'burn'
    pwa = 'pwa'

    class Config:
        use_enum_values = True


class Scope(Enum):
    user = 'user'
    machine = 'machine'

    class Config:
        use_enum_values = True


class InstallMode(Enum):
    interactive = 'interactive'
    silent = 'silent'
    silentWithProgress = 'silentWithProgress'

    class Config:
        use_enum_values = True


class InstallModes(BaseModel):
    __root__: List[InstallMode] = Field(
        ...,
        description='List of supported installer modes',
        max_items=3,
        unique_items=True,
    )


class InstallerSwitches(BaseModel):
    Silent: Optional[Optional[constr(min_length=1, max_length=512)]] = Field(
        None,
        description='Silent is the value that should be passed to the installer when user chooses a silent or quiet install',
    )
    SilentWithProgress: Optional[
        Optional[constr(min_length=1, max_length=512)]
    ] = Field(
        None,
        description='SilentWithProgress is the value that should be passed to the installer when user chooses a non-interactive install',
    )
    Interactive: Optional[Optional[constr(min_length=1, max_length=512)]] = Field(
        None,
        description='Interactive is the value that should be passed to the installer when user chooses an interactive install',
    )
    InstallLocation: Optional[Optional[constr(min_length=1, max_length=512)]] = Field(
        None,
        description='InstallLocation is the value passed to the installer for custom install location. <INSTALLPATH> token can be included in the switch value so that winget will replace the token with user provided path',
    )
    Log: Optional[Optional[constr(min_length=1, max_length=512)]] = Field(
        None,
        description='Log is the value passed to the installer for custom log file path. <LOGPATH> token can be included in the switch value so that winget will replace the token with user provided path',
    )
    Upgrade: Optional[Optional[constr(min_length=1, max_length=512)]] = Field(
        None,
        description='Upgrade is the value that should be passed to the installer when user chooses an upgrade',
    )
    Custom: Optional[Optional[constr(min_length=1, max_length=2048)]] = Field(
        None,
        description='Custom switches will be passed directly to the installer by winget',
    )


class InstallerReturnCode(BaseModel):
    __root__: conint(ge=-2147483648, le=4294967295) = Field(
        ...,
        description='An exit code that can be returned by the installer after execution',
    )


class InstallerSuccessCodes(BaseModel):
    __root__: List[InstallerReturnCode] = Field(
        ...,
        description='List of additional non-zero installer success exit codes other than known default values by winget',
        max_items=16,
        unique_items=True,
    )


class ReturnResponse(Enum):
    packageInUse = 'packageInUse'
    installInProgress = 'installInProgress'
    fileInUse = 'fileInUse'
    missingDependency = 'missingDependency'
    diskFull = 'diskFull'
    insufficientMemory = 'insufficientMemory'
    noNetwork = 'noNetwork'
    contactSupport = 'contactSupport'
    rebootRequiredToFinish = 'rebootRequiredToFinish'
    rebootRequiredForInstall = 'rebootRequiredForInstall'
    rebootInitiated = 'rebootInitiated'
    cancelledByUser = 'cancelledByUser'
    alreadyInstalled = 'alreadyInstalled'
    downgrade = 'downgrade'
    blockedByPolicy = 'blockedByPolicy'

    class Config:
        use_enum_values = True

class ExpectedReturnCode(BaseModel):
    InstallerReturnCode: Optional[InstallerReturnCode] = None
    ReturnResponse: Optional[ReturnResponse] = None


class ExpectedReturnCodes(BaseModel):
    __root__: List[ExpectedReturnCode] = Field(
        ..., description='Installer exit codes for common errors', max_items=128
    )


class UpgradeBehavior(Enum):
    install = 'install'
    uninstallPrevious = 'uninstallPrevious'

    class Config:
        use_enum_values = True


class Command(BaseModel):
    __root__: constr(min_length=1, max_length=40)


class Commands(BaseModel):
    __root__: List[Command] = Field(
        ...,
        description='List of commands or aliases to run the package',
        max_items=16,
        unique_items=True,
    )


class Protocol(BaseModel):
    __root__: constr(regex=r'^[a-z][-a-z0-9\.\+]*$', max_length=2048)


class Protocols(BaseModel):
    __root__: List[Protocol] = Field(
        ...,
        description='List of protocols the package provides a handler for',
        max_items=16,
        unique_items=True,
    )


class FileExtension(BaseModel):
    __root__: constr(regex=r'^[^\\/:\*\?"<>\|\x01-\x1f]+$', max_length=64)


class FileExtensions(BaseModel):
    __root__: List[FileExtension] = Field(
        ...,
        description='List of file extensions the package could support',
        max_items=256,
        unique_items=True,
    )


class WindowsFeature(BaseModel):
    __root__: constr(min_length=1, max_length=128)


class WindowsLibrary(BaseModel):
    __root__: constr(min_length=1, max_length=128)


class PackageDependency(BaseModel):
    PackageIdentifier: PackageIdentifier
    MinimumVersion: Optional[PackageVersion] = None


class ExternalDependency(BaseModel):
    __root__: constr(min_length=1, max_length=128)


class Dependencies(BaseModel):
    WindowsFeatures: Optional[List[WindowsFeature]] = Field(
        None,
        description='List of Windows feature dependencies',
        max_items=16,
        unique_items=True,
    )
    WindowsLibraries: Optional[List[WindowsLibrary]] = Field(
        None,
        description='List of Windows library dependencies',
        max_items=16,
        unique_items=True,
    )
    PackageDependencies: Optional[List[PackageDependency]] = Field(
        None,
        description='List of package dependencies from current source',
        max_items=16,
        unique_items=True,
    )
    ExternalDependencies: Optional[List[ExternalDependency]] = Field(
        None,
        description='List of external package dependencies',
        max_items=16,
        unique_items=True,
    )


class PackageFamilyName(BaseModel):
    __root__: Optional[
        constr(regex=r'^[A-Za-z0-9][-\.A-Za-z0-9]+_[A-Za-z0-9]{13}$', max_length=255)
    ] = Field(
        ...,
        description='PackageFamilyName for appx or msix installer. Could be used for correlation of packages across sources',
    )


class ProductCode(BaseModel):
    __root__: Optional[constr(min_length=1, max_length=255)] = Field(
        ...,
        description='ProductCode could be used for correlation of packages across sources',
    )


class Capability(BaseModel):
    __root__: constr(min_length=1, max_length=40)


class Capabilities(BaseModel):
    __root__: List[Capability] = Field(
        ...,
        description='List of appx or msix installer capabilities',
        max_items=1000,
        unique_items=True,
    )


class RestrictedCapability(BaseModel):
    __root__: constr(min_length=1, max_length=40)


class RestrictedCapabilities(BaseModel):
    __root__: List[RestrictedCapability] = Field(
        ...,
        description='List of appx or msix installer restricted capabilities',
        max_items=1000,
        unique_items=True,
    )


class Market(BaseModel):
    __root__: constr(regex=r'^[A-Z]{2}$') = Field(
        ..., description='The installer target market'
    )


class MarketArray(BaseModel):
    __root__: List[Market] = Field(
        ..., description='Array of markets', max_items=256, unique_items=True
    )


class Market1(BaseModel):
    AllowedMarkets: MarketArray


class Market2(BaseModel):
    ExcludedMarkets: MarketArray


class Markets(BaseModel):
    __root__: Union[Market1, Market2] = Field(..., description='The installer markets')


class InstallerAbortsTerminal(BaseModel):
    __root__: Optional[bool] = Field(
        ...,
        description='Indicates whether the installer will abort terminal. Default is false',
    )


class ReleaseDate(BaseModel):
    __root__: Optional[str] = Field(..., description='The installer release date')


class InstallLocationRequired(BaseModel):
    __root__: Optional[bool] = Field(
        ...,
        description='Indicates whether the installer requires an install location provided',
    )


class RequireExplicitUpgrade(BaseModel):
    __root__: Optional[bool] = Field(
        ...,
        description='Indicates whether the installer should be pinned by default from upgrade',
    )


class UnsupportedOSArchitecture(Enum):
    x86 = 'x86'
    x64 = 'x64'
    arm = 'arm'
    arm64 = 'arm64'

    class Config:
        use_enum_values = True


class UnsupportedOSArchitectures(BaseModel):
    __root__: List[UnsupportedOSArchitecture] = Field(
        ...,
        description='List of OS architectures the installer does not support',
        unique_items=True,
    )


class AppsAndFeaturesEntry(BaseModel):
    DisplayName: Optional[Optional[constr(min_length=1, max_length=256)]] = Field(
        None, description='The DisplayName registry value'
    )
    Publisher: Optional[Optional[constr(min_length=1, max_length=256)]] = Field(
        None, description='The Publisher registry value'
    )
    DisplayVersion: Optional[Optional[constr(min_length=1, max_length=128)]] = Field(
        None, description='The DisplayVersion registry value'
    )
    ProductCode: Optional[ProductCode] = None
    UpgradeCode: Optional[ProductCode] = None
    InstallerType: Optional[InstallerType] = None


class AppsAndFeaturesEntries(BaseModel):
    __root__: List[AppsAndFeaturesEntry] = Field(
        ..., description='List of ARP entries.', max_items=128, unique_items=True
    )


class ElevationRequirement(Enum):
    elevationRequired = 'elevationRequired'
    elevationProhibited = 'elevationProhibited'
    elevatesSelf = 'elevatesSelf'


class Architecture(Enum):
    x86 = 'x86'
    x64 = 'x64'
    arm = 'arm'
    arm64 = 'arm64'
    neutral = 'neutral'

    class Config:
        use_enum_values = True


class Installer(BaseModel):
    InstallerLocale: Optional[Locale] = None
    Platform: Optional[Platform] = None
    MinimumOSVersion: Optional[MinimumOSVersion] = None
    Architecture: Architecture = Field(
        ..., description='The installer target architecture'
    )
    InstallerType: Optional[InstallerType] = None
    Scope: Optional[Scope] = None
    InstallerUrl: constr(
        regex=r'^([Hh][Tt][Tt][Pp][Ss]?)://.+$', max_length=2048
    ) = Field(..., description='The installer Url')
    InstallerSha256: constr(regex=r'^[A-Fa-f0-9]{64}$') = Field(
        ..., description='Sha256 is required. Sha256 of the installer'
    )
    SignatureSha256: Optional[Optional[constr(regex=r'^[A-Fa-f0-9]{64}$')]] = Field(
        None,
        description='SignatureSha256 is recommended for appx or msix. It is the sha256 of signature file inside appx or msix. Could be used during streaming install if applicable',
    )
    InstallModes: Optional[InstallModes] = None
    InstallerSwitches: Optional[InstallerSwitches] = None
    InstallerSuccessCodes: Optional[InstallerSuccessCodes] = None
    ExpectedReturnCodes: Optional[ExpectedReturnCodes] = None
    UpgradeBehavior: Optional[UpgradeBehavior] = None
    Commands: Optional[Commands] = None
    Protocols: Optional[Protocols] = None
    FileExtensions: Optional[FileExtensions] = None
    Dependencies: Optional[Dependencies] = None
    PackageFamilyName: Optional[PackageFamilyName] = None
    ProductCode: Optional[ProductCode] = None
    Capabilities: Optional[Capabilities] = None
    RestrictedCapabilities: Optional[RestrictedCapabilities] = None
    Markets: Optional[Markets] = None
    InstallerAbortsTerminal: Optional[InstallerAbortsTerminal] = None
    ReleaseDate: Optional[ReleaseDate] = None
    InstallLocationRequired: Optional[InstallLocationRequired] = None
    RequireExplicitUpgrade: Optional[RequireExplicitUpgrade] = None
    UnsupportedOSArchitectures: Optional[UnsupportedOSArchitectures] = None
    AppsAndFeaturesEntries: Optional[AppsAndFeaturesEntries] = None
    ElevationRequirement: Optional[ElevationRequirement] = None


class Model(BaseModel):
    PackageIdentifier: PackageIdentifier
    PackageVersion: PackageVersion
    Channel: Optional[Channel] = None
    InstallerLocale: Optional[Locale] = None
    Platform: Optional[Platform] = None
    MinimumOSVersion: Optional[MinimumOSVersion] = None
    InstallerType: Optional[InstallerType] = None
    Scope: Optional[Scope] = None
    InstallModes: Optional[InstallModes] = None
    InstallerSwitches: Optional[InstallerSwitches] = None
    InstallerSuccessCodes: Optional[InstallerSuccessCodes] = None
    ExpectedReturnCodes: Optional[ExpectedReturnCodes] = None
    UpgradeBehavior: Optional[UpgradeBehavior] = None
    Commands: Optional[Commands] = None
    Protocols: Optional[Protocols] = None
    FileExtensions: Optional[FileExtensions] = None
    Dependencies: Optional[Dependencies] = None
    PackageFamilyName: Optional[PackageFamilyName] = None
    ProductCode: Optional[ProductCode] = None
    Capabilities: Optional[Capabilities] = None
    RestrictedCapabilities: Optional[RestrictedCapabilities] = None
    Markets: Optional[Markets] = None
    InstallerAbortsTerminal: Optional[InstallerAbortsTerminal] = None
    ReleaseDate: Optional[ReleaseDate] = None
    InstallLocationRequired: Optional[InstallLocationRequired] = None
    RequireExplicitUpgrade: Optional[RequireExplicitUpgrade] = None
    UnsupportedOSArchitectures: Optional[UnsupportedOSArchitectures] = None
    AppsAndFeaturesEntries: Optional[AppsAndFeaturesEntries] = None
    ElevationRequirement: Optional[ElevationRequirement] = None
    Installers: List[Installer] = Field(..., max_items=1024, min_items=1)
    ManifestType: str = Field(..., description='The manifest type')
    ManifestVersion: constr(
        regex=r'^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])(\.(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])){2}$'
    ) = Field(..., description='The manifest syntax version')

from enum import Enum
from glob import glob
from typing import List
from pathlib import Path
from winget_lib.core.winget import defaultLocale, installer, locale, singleton, version
import yaml

class MyDumper(yaml.SafeDumper):
    def represent_data(self, data):
        if isinstance(data, Enum):
            return self.represent_data(data.value)
        return super().represent_data(data)

class Manifest:
    DefaultLocale: defaultLocale.Model = None
    Installer: installer.Model = None
    Locales: List[locale.Model] = []
    Singleton: singleton.Model = None
    Version: version.Model = None
    Path: Path = None

    def getPackageVersion(self) -> str:
        """Get the package version across all of the manifest's files."""
        if (self.Singleton is not None):
            return self.Singleton.PackageVersion
        return self.Version.PackageVersion
    
    def setPackageVersion(self, packageVersion: str) -> None:
        """Set the package version across all of the manifest's files."""
        if (self.Singleton is not None):
            self.Singleton.PackageVersion = packageVersion
        else:
            self.DefaultLocale.PackageVersion = packageVersion
            self.Installer.PackageVersion = packageVersion
            for i in self.Locales:
                i.PackageVersion = packageVersion
            self.Version.PackageVersion = packageVersion
    
    def getPackageIdentifier(self):
        """Get the package identifier across all of the manifest's files."""
        if (self.Singleton is not None):
            return self.Singleton.PackageIdentifier
        else:
            return self.Version.PackageIdentifier
    
    def setPackageIdentifier(self, packageIdentifier: str) -> None:
        """Set the package identifier across all of the manifest's files."""
        if (self.Singleton is not None):
            self.Singleton.PackageIdentifier = packageIdentifier
        else:
            self.DefaultLocale.PackageIdentifier = packageIdentifier
            self.Installer.PackageIdentifier = packageIdentifier
            for i in self.Locales:
                i.PackageIdentifier = packageIdentifier
            self.Version.PackageIdentifier = packageIdentifier
    
    def getManifestType(self) -> str:
        """Get the manifest type (singleton or multifile)."""
        if (self.Singleton is not None):
            return "singleton"
        else:
            return "multifile"
    
    def writeToFolder(self, path: Path = None, manifestsFolderLocation: Path = None) -> Path:
        """Write the manifest to a path (or the manifests folder if no path is specified)."""
        packageIdentifier = self.getPackageIdentifier()
        packageVersion = self.getPackageVersion()
        if (path is None):
            # Example: Google.Chrome version 1.0 -> manifests/g/Google/Chrome/1.0/
            pathParts = [packageIdentifier[0].lower()]
            pathParts.extend(packageIdentifier.split('.'))
            pathParts.append(packageVersion)
            path = Path("manifests/" + "/".join(pathParts))
            if (manifestsFolderLocation is not None):
                path = manifestsFolderLocation / path
        path.mkdir(parents=True, exist_ok=True)
        # Denormalize InstallerTypes.
        if (self.Installer is not None and self.Installer.InstallerType is not None):
            for i in self.Installer.Installers:
                if (i.InstallerType is None):
                    i.InstallerType = self.Installer.InstallerType
            self.Installer.InstallerType = None
        # Write the files.
        if (self.getManifestType() == "singleton"):
            with open (path / f"{packageIdentifier}.yaml", 'w', encoding="utf-8") as stream:
                stream.write(f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.singleton.{self.Singleton.ManifestVersion}.schema.json\r\n")
                outputString = yaml.dump(self.Singleton.dict(exclude_none=True, exclude_unset=True), Dumper=MyDumper, sort_keys=False, allow_unicode=True)
                stream.write(outputString.replace("\n", "\r\n"))
        else:
            with open (path / f"{packageIdentifier}.locale.{self.DefaultLocale.PackageLocale}.yaml", 'w', encoding="utf-8") as stream:
                stream.write(f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.defaultLocale.{self.DefaultLocale.ManifestVersion}.schema.json\r\n")
                outputString = yaml.dump(self.DefaultLocale.dict(exclude_none=True, exclude_unset=True), Dumper=MyDumper, sort_keys=False, allow_unicode=True)
                stream.write(outputString.replace("\n", "\r\n"))
            with open (path / f"{packageIdentifier}.installer.yaml", 'w', encoding="utf-8") as stream:
                stream.write(f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.installer.{self.Installer.ManifestVersion}.schema.json\r\n")
                outputString = yaml.dump(self.Installer.dict(exclude_none=True, exclude_unset=True), Dumper=MyDumper, sort_keys=False, allow_unicode=True)
                stream.write(outputString.replace("\n", "\r\n"))
            for i in self.Locales:
                with open (path / f"{packageIdentifier}.locale.{i.PackageLocale}.yaml", 'w', encoding="utf-8") as stream:
                    stream.write(f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.locale.{i.ManifestVersion}.schema.json\r\n")
                    outputString = yaml.dump(i.dict(exclude_none=True, exclude_unset=True), Dumper=MyDumper, sort_keys=False, allow_unicode=True)
                    stream.write(outputString.replace("\n", "\r\n"))
            with open (path / f"{packageIdentifier}.yaml", 'w', encoding="utf-8") as stream:
                stream.write(f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.version.{self.Version.ManifestVersion}.schema.json\r\n")
                outputString = yaml.dump(self.Version.dict(exclude_none=True, exclude_unset=True), Dumper=MyDumper, sort_keys=False, allow_unicode=True)
                stream.write(outputString.replace("\n", "\r\n"))
        return path



def readManifestFromFolder(folder: Path) -> Manifest:
    """Read a manifest from a folder."""
    manifest = Manifest()
    manifest.Locales = []
    files = list(folder.glob('*.yaml'))
    if (len(files) == 0):
        raise "This folder does not contain any yaml files :("
    manifest.Path = folder
    for file in files:
        with open(file, 'r', encoding="utf-8") as stream:
            try:
                manifestFile = yaml.safe_load(stream)
                if (manifestFile["ManifestVersion"] != "1.2.0"):
                    manifestFile["ManifestVersion"] = "1.2.0"
                if (manifestFile["ManifestType"].lower() == "singleton"):
                    # If it's a singleton, then we only need to load this file.
                    manifest.Singleton = singleton.Model(**manifestFile)
                    return manifest
                elif (manifestFile["ManifestType"].lower() == "defaultlocale"):
                    manifest.DefaultLocale = defaultLocale.Model(**manifestFile)
                elif (manifestFile["ManifestType"].lower() == "locale"):
                    manifest.Locales.append(locale.Model(**manifestFile))
                elif (manifestFile["ManifestType"].lower() == "installer"):
                    manifest.Installer = installer.Model(**manifestFile)
                elif (manifestFile["ManifestType"].lower() == "version"):
                    manifest.Version = version.Model(**manifestFile)
                else:
                    raise Exception("Unknown manifest file type: " + manifestFile["ManifestType"])
            except:
                raise Exception("Error reading manifest file: " + str(file))
    return manifest
def readManifestByIdentifierAndVersion(packageIdentifier: str, packageVersion: str, manifestsFolderRoot: Path = None) -> Manifest:
    """Given a package identifier and a version, find the manifest in the manifests folder (you can set the root of the manifests folder too, if it's not the current directory)"""
    pathParts = [packageIdentifier[0].lower()]
    pathParts.extend(packageIdentifier.split('.'))
    pathParts.append(packageVersion)
    path = Path("manifests/" + "/".join(pathParts))
    if (manifestsFolderRoot is not None):
        path = manifestsFolderRoot / path
    return readManifestFromFolder(path)
def getAllManifestsForIdentifier(packageIdentifier: str, manifestsFolderRoot: Path = None) -> List[Manifest]:
    """Given a package identifier, get a list of manifests from the manifests folder. Optionally, you can provide the manifestsFolderRoot if it isn't the current directory."""
    pathParts = [packageIdentifier[0].lower()]
    pathParts.extend(packageIdentifier.split('.'))
    path = Path("manifests/" + "/".join(pathParts))
    if (manifestsFolderRoot is not None):
        path = manifestsFolderRoot / path
    allFolders = list(path.glob("*"))
    allManifestFolders = list(filter(lambda x: len(list(x.glob("*.yaml"))) > 0, allFolders))
    manifests = []
    for i in allManifestFolders:
        manifests.append(readManifestFromFolder(i))
    return manifests
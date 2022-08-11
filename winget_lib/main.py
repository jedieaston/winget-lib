from pathlib import Path
import typer
import core.manifest
from core.winget.installer import Installer
import hashlib
import requests
import os
import tempfile
from rich import print_json
from rich.progress import Progress

app = typer.Typer()


def downloadFileSync(url: str, path: Path = None) -> Path:
    """
    Download a file, sync. 
    If no path is specified, then it is downloaded to your temporary files.
    """
    tempDir = tempfile.gettempdir()
    if path is None:
        path = Path(tempDir, Path(url).name)
    with Progress() as progress:
        response = requests.get(url, stream=True)
        total = int(response.headers.get('content-length'), 0)

        download = progress.add_task(f"Downloading {url}", total=total)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if not chunk:
                    break
                f.write(chunk)
                progress.update(download, advance=1024)
        return path
def getSha256Hash(path: Path) -> str:
    """
    Given the path to a file, get the SHA256 hash of that file.
    """
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()

def updateInstallerEntry(installer: Installer, originalVersion: str | None = None, autoReplaceVersion: str | None = None) -> Installer:
    """
    Update a installer entry.
    If a originalVersion and autoReplaceVersion is specified, we will replace all of the instance of the version in the URL with that.
    """
    if autoReplaceVersion is not None and originalVersion is not None:
        newInstallerUrl = installer.InstallerUrl.replace(originalVersion, autoReplaceVersion)
        if (newInstallerUrl == installer.InstallerUrl):
            typer.secho(f"Could not replace {originalVersion} with {autoReplaceVersion} in {installer.InstallerUrl}. Continuing.", fg="yellow")
    else:
        print_json(installer.json(exclude_unset=True))
        newInstallerUrl = typer.prompt("What's the installer URL for this entry?", default=installer.InstallerUrl)
    tempFilePath = downloadFileSync(newInstallerUrl)
    newInstallerSha256 = getSha256Hash(tempFilePath)
    installer.InstallerUrl = newInstallerUrl
    installer.InstallerSha256 = newInstallerSha256

    os.remove(tempFilePath)
    typer.secho("Updated installer entry!", fg="green")
    print_json(installer.json(exclude_unset=True))
    typer.echo("\n")
    return installer



@app.command(name="update")
def update(
    manifest_path: Path = typer.Argument(..., file_okay=False, dir_okay=True, exists=True), 
    new_version: str = typer.Argument(..., help="The new version to set"),
    auto_replace: bool = typer.Option(False, "--auto-replace", "-r", help="Automatically replace the old version with the new one in installer links."),
    ):
    """
    Update a winget manifest.
    """
    manifest = None
    try:
        manifest = core.manifest.readManifestFromFolder(manifest_path)
    except:
        typer.secho(f"Could not read manifest from path {str(manifest_path)}", fg="red")
        raise typer.Exit(1)
    
    for installer in manifest.Installer.Installers:
        if (manifest.Installer.InstallerType is not None):
            # Denormalize installer types.
            installer.InstallerType = manifest.Installer.InstallerType
        if (auto_replace):
            installer = updateInstallerEntry(installer, manifest.Installer.Version, new_version)
        else:
            installer = updateInstallerEntry(installer)
        
    manifest.Installer.InstallerType = None
    manifest.setPackageVersion(new_version)
    manifest.writeToFolder()

@app.command(name="info")
def info():
    typer.secho("easton's little winget tool", fg="green") 

if __name__ == "__main__":
    app()

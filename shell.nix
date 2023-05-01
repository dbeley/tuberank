with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  name = "YtvdPythonEnv";
  venvDir = "./venv";
  buildInputs = [
    nodejs
    pythonPackages.python

    pythonPackages.pip
    ruff
    gettext
  ];

}

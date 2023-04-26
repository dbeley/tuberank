with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  name = "YtvdPythonEnv";
  venvDir = "./venv";
  buildInputs = [
    pythonPackages.python

    pythonPackages.pip
    ruff
  ];

}

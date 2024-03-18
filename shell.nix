with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  name = "TubeRankPythonEnv";
  venvDir = "./venv";
  buildInputs = [
    nodejs
    pythonPackages.python

    pythonPackages.pip
    poetry
    ruff
    gettext
    postgresql
    libpqxx

    flyctl
  ];

}

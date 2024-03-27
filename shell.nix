with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  buildInputs = [
    nodejs
    python3
    pythonPackages.pip
    poetry
    ruff
    gettext
    postgresql
    libpqxx
    flyctl
  ];

}

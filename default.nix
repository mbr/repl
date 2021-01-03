{ pkgs ? (import <nixpkgs>) { } }:
let
  pyDeps = python-packages: with python-packages; [ click ];
  python = pkgs.python3.withPackages pyDeps;
in python.pkgs.buildPythonPackage {
  name = "repl";
  version = "1.1.dev1";
  src = ./.;
  propagatedBuildInputs = [ python ];
}

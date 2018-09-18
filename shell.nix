with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "teambot";
  buildInputs = [
    git
    python36
  ];
}

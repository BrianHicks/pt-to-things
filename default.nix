let
  pkgs = import <nixpkgs> {};

  token = builtins.readFile ./token;
in pkgs.stdenv.mkDerivation {
  name = "pt-to-things";
  src = ./.;

  installPhase = ''
    mkdir -p $out/{bin,share/pt-to-things}
    cp -r pt-to-things.py README.md LICENSE $out/share/pt-to-things/

    bin=$out/bin/pt-to-things
    echo "#!/bin/sh -e" > $bin
    echo "exec ${pkgs.python35}/bin/python $out/share/pt-to-things/pt-to-things.py --token ${token} \"\$@\"" >> $bin
    chmod +x $bin
  '';
}

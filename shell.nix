with import <nixpkgs> {};

let
  # need an ancient versions of yosys for solver :/
  yosys = pkgs.callPackage ./yosys.nix {};

in pkgs.mkShell {
  buildInputs = with pkgs; [
    yosys nextpnr icestorm verilog
    (python3.withPackages (ps: with ps; [ z3 ] ))
  ];
}

{
  description = "Development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-26.05-darwin";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch_64-linux"
        "x86_64-darwin"
        "aarch_64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              # Native development tools. mise supplies uv; uv supplies Python
              # and all Python dependencies declared in pyproject.toml.
              mise
            ];

            # Keep the editor and shell happy in an interactive session.
            shellHook = ''
              echo ""
              echo "Development shell"
              echo "   mise    : $(mise --version 2>&1)"
              echo ""
              echo "Run 'mise install', then 'mise run sync'."
              echo ""
            '';
          };
        }
      );
    };
}

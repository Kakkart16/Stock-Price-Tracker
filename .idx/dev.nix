{ pkgs, ... }: {

  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"
  services.docker.enable = true;
  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python3
    pkgs.redis
    pkgs.python311Packages.redis
  ];

  # Sets environment variables in the workspace
  env = {

  };

  # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
  idx.extensions = [
    
  ];

  # Enable previews and customize configuration
  idx.previews = {
    enable = false;
    previews = [
        {
            command = [ "bash" "-c" "source env/bin/activate && cd stocks && python manage.py runserver" ];
            cwd = "/home/user/Stock-Price-Tracker/";
            manager = "web";
            id = "web";
        }
    ];
  };
}
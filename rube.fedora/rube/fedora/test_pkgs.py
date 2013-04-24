
import rube.fedora


class TestPkgs(rube.fedora.FedoraRubeTest):
    base = "http://pkgs.stg.fedoraproject.org/cgit"
    title = "Fedora Project Packages GIT repositories"
    no_auth = True

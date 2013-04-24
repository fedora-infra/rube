
import rube.fedora


class TestBusmon(rube.fedora.FedoraRubeTest):
    base = "https://apps.stg.fedoraproject.org/busmon/"
    title = "Fedora Busmon"
    no_auth = True

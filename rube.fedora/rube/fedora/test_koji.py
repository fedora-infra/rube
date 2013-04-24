
import rube.fedora


class TestKoji(rube.fedora.FedoraRubeTest):
    base = "http://koji.stg.fedoraproject.org/koji"
    title = "Build System Info | koji"
    no_auth = True


import rube.fedora


class TestEasyFix(rube.fedora.FedoraRubeTest):
    base = "https://stg.fedoraproject.org/easyfix/"
    title = "Fedora Project easyfix"
    no_auth = True

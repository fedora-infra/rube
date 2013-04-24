
import rube.fedora


class TestBasePage(rube.fedora.FedoraRubeTest):
    base = "https://stg.fedoraproject.org/"
    title = "Fedora Project Homepage"
    no_auth = True

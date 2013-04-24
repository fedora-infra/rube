
import rube.fedora


class TestDocs(rube.fedora.FedoraRubeTest):
    base = "https://docs.stg.fedoraproject.org/en-US/index.html"
    title = "Welcome"
    no_auth = True

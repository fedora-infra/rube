
import rube.fedora


class TestNagios(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/nagios/"
    title = "Nagios Core"
    no_auth = True

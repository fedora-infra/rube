
import rube.fedora


class TestHAProxy(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/haproxy/proxy1"
    title = "Statistics Report for HAProxy"
    no_auth = True

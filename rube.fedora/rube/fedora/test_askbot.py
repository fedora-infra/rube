
import rube.fedora


class TestAskbot(rube.fedora.FedoraRubeTest):
    base = "https://ask.stg.fedoraproject.org/questions/"
    title = "Questions - Ask Fedora: Knowledge Base and Community Wiki"
    no_auth = True

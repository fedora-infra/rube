
import rube.core
import rube.fedora


class TestCollectd(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/collectd/"
    title = "collection.cgi, Version 3"
    no_auth = True

    @rube.core.tolerant()
    def test_app01_page(self):
        url = self.base + "bin/index.cgi" + \
            "?hostname=app01&plugin=apache&timespan=86400" + \
            "&action=show_selection&ok_button=OK"
        self.driver.get(url)
        self.wait_for("ApacheBytes")

"""
Plugin definition for the iframeapi OPAL plugin
"""
from opal.core import plugins

from iframeapi.urls import urlpatterns

class iframeapiPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.iframeapi': [
            # 'js/iframeapi/app.js',
            # 'js/iframeapi/controllers/larry.js',
            # 'js/iframeapi/services/larry.js',
        ]
    }

    def restricted_teams(self, user):
        """
        Return any restricted teams for particualr users that our
        plugin may define.
        """
        return []

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {}

    def flows(self):
        """
        Return any custom flows that our plugin may define
        """
        return {}

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}


plugins.register(iframeapiPlugin)
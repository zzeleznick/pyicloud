"""Find my Friends service."""
from __future__ import absolute_import
import json


class FindFriendsService(object):
    """
    The 'Find My' (FKA 'Find My Friends') iCloud service

    This connects to iCloud and returns friend data including
    latitude and longitude.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._friend_endpoint = "%s/fmipservice/client/fmfWeb/initClient" % (
            self._service_root,
        )
        self.refresh_always = False
        self.should_refresh_client_fnc = None
        self.response = {}

    def refresh_client(self):
        """
        Refreshes all data from 'Find My' endpoint,
        """
        params = dict(self.params)
        # This is a request payload we mock to fetch the data
        mock_payload = json.dumps(
            {
                "clientContext": {
                    "appVersion": "1.0",
                    "contextApp": "com.icloud.web.fmf",
                    "mapkitAvailable": True,
                    "productType": "fmfWeb",
                    "tileServer": "Apple",
                    "userInactivityTimeInMS": 537,
                    "windowInFocus": False,
                    "windowVisible": True,
                },
                "dataContext": None,
                "serverContext": None,
            }
        )
        req = self.session.post(self._friend_endpoint, data=mock_payload, params=params)
        self.response = req.json()

    def should_refresh_client(self):
        """
        Customizable logic to determine whether the data should be refreshed.

        By default, this returns False.

        Consumers can set `refresh_always` to True or assign their own function
        that takes a single-argument (the last reponse) and returns a boolean.
        """
        fnc = self.should_refresh_client_fnc
        if not fnc or not callable(fnc):
            return self.refresh_always
        return fnc(self.response)

    @property
    def data(self):
        """
        Convenience property to return data from the 'Find My' endpoint.

        Call `refresh_client()` before property access for latest data.
        """
        if not self.response or self.should_refresh_client():
            self.refresh_client()
        return self.response

    @property
    def locations(self):
        """Returns a list of your friends' locations"""
        return self.data.get("locations")

    @property
    def followers(self):
        """Returns a list of friends who follow you"""
        return self.data.get("followers")

    @property
    def following(self):
        """Returns a list of friends who you follow"""
        return self.data.get("following")

    @property
    def contact_details(self):
        """Returns a list of your friends contact details"""
        return self.data.get("contactDetails")

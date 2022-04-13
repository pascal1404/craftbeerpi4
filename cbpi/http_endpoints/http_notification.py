
from aiohttp import web
from cbpi.api import request_mapping
from cbpi.utils import json_dumps
import logging

class NotificationHttpEndpoints:

    def __init__(self,cbpi):
        self.cbpi = cbpi
        self.cbpi.register(self, url_prefix="/notification")

    @request_mapping(path="/{id}/action/{action_id}", method="POST", auth_required=False)
    async def action(self, request):
        """
        ---
        description: Update an actor
        tags:
        - Notification
        parameters:
        - name: "id"
          in: "path"
          description: "Notification Id"
          required: true
          type: "string"
        - name: "action_id"
          in: "path"
          description: "Action Id"
          required: true
          type: "string"

        responses:
            "200":
                description: successful operation
        """

        notification_id = request.match_info['id']
        action_id = request.match_info['action_id']
        print(notification_id, action_id)
        self.cbpi.notification.notify_callback(notification_id, action_id)  
        return web.Response(status=204)
        

    @request_mapping(path="/", auth_required=False)
    async def http_get_all(self, request):
        """

        ---
        description: get notification with action
        tags:
        - Notification
        responses:
            "204":
                description: successful operation
        """
        notify_dict={}
        for key in self.cbpi.notification.callback_cache:
            actions = list(map(lambda item: item.to_dict(), self.cbpi.notification.callback_cache[key]))
            if actions:
                notify_dict = {'Notification-Id': key, 'Actions': actions}
        return web.json_response(data=notify_dict)
        
        self.cbpi.register(self, url_prefix="/notification")

    @request_mapping(path="/{id}", method="POST", auth_required=False)
    async def delete_notify_dialog(self, request):
        """
        ---
        description: delete a notifcation dialog
        tags:
        - Notification
        parameters:
        - name: "id"
          in: "path"
          description: "Notification Id"
          required: true
          type: "string"

        responses:
            "204":
                description: successful operation
        """

        notification_id = request.match_info['id']
        self.cbpi.notification.nofity_delete_dialog(notification_id)
        return web.Response(status=204)
        
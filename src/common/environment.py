from tornado.gen import coroutine, Return

from . import cached
import internal
import logging


class AppNotFound(Exception):
    pass


class EnvironmentClient(object):
    def __init__(self, cache):
        self.internal = internal.Internal()
        self.cache = cache

    @coroutine
    def list_apps(self, gamespace_id):
        @cached(kv=self.cache,
                h="apps:" + str(gamespace_id),
                json=True)
        @coroutine
        def get():

            try:
                response = yield self.internal.request(
                    "environment",
                    "get_apps",
                    gamespace_id=gamespace_id)
            except internal.InternalError:
                logging.exception("Failed to list apps")
                raise Return([])
            else:
                raise Return(response)

        all_apps = yield get()

        raise Return({
            app_data["app_name"]: app_data["app_title"]
            for app_data in all_apps
        })

    @coroutine
    def get_app_info(self, gamespace_id, app_name):
        @cached(kv=self.cache,
                h=lambda: "app:" + app_name + ":" + str(gamespace_id),
                json=True)
        @coroutine
        def get():
            response = yield self.internal.request(
                "environment",
                "get_app_info",
                app_name=app_name,
                gamespace_id=gamespace_id)

            raise Return(response)

        try:
            app_info = yield get()
            raise Return(app_info)

        except internal.InternalError as e:
            if e.code == 404:
                raise AppNotFound()
            else:
                raise e

    @coroutine
    def get_app_title(self, gamespace_id, app_name):
        app_info = yield self.get_app_info(gamespace_id, app_name)
        raise Return(app_info["title"])

    @coroutine
    def get_app_versions(self, gamespace_id, app_name):
        app_info = yield self.get_app_info(gamespace_id, app_name)
        raise Return(app_info["versions"])

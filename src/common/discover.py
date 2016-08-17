
from tornado.gen import coroutine, Return
from common.options import define, options

import internal
import singleton


class Discovery(object):
    __metaclass__ = singleton.Singleton

    def __init__(self):
        self.discovery_service = options.discovery_service
        self.services = {
            "internal:discovery": self.discovery_service
        }
        self.internal = internal.Internal()

    @coroutine
    def get_services(self, services, network="internal"):

        if all([(network + ":" + service_id) in self.services for service_id in services]):
            raise Return({service_id: self.services[network + ":" + service_id] for service_id in services})

        if self.discovery_service is None:
            raise DiscoveryError("Cannon fetch discovery service because it's None")

        required_also = [service_id for service_id in services if service_id not in self.services]

        try:
            response_services = yield self.internal.get(
                self.discovery_service,
                "services/" + ",".join(required_also) + "/" + network, {},
                discover_service=False)

        except internal.InternalError as e:
            raise DiscoveryError("Discovery error: {0} {1}.".format(e.code, e.body))

        self.services.update({
            (network + ":" + service_id): service_location
            for service_id, service_location in response_services.iteritems()
        })

        raise Return({
            service_id: self.services[network + service_id]
            for service_id in services
        })

    @coroutine
    def get_service(self, service_id, network="internal", version=True):
        record_id = network + ":" + service_id

        if record_id in self.services:
            raise Return(self.services[record_id])

        if self.discovery_service is None:
            raise DiscoveryError(
                "Cannon fetch discovery service because it's None")

        try:
            response = yield self.internal.get(
                self.discovery_service,
                "service/" + service_id + "/" + network,
                {
                    "version": "true" if version else "false"
                },
                use_json=False,
                discover_service=False)

        except internal.InternalError as e:
            if e.code == 404:
                raise DiscoveryError("404 No such service")
            elif e.code == 502:
                raise DiscoveryError("502 Service is down")
            else:
                raise DiscoveryError("Discovery error: {0} {1}.".format(
                    e.code, e.body))

        self.services[record_id] = response

        raise Return(response)

    def location(self):
        return self.discovery_service


class DiscoveryError(Exception):
    pass


cache = None


def init():
    global cache
    if cache is None:
        cache = Discovery()

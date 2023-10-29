import etcd3

import sys
import time
from threading import Event

# The current leader is going to be the value with this key.
LEADER_KEY = "/election/leader"
LEADER_LEASE_TTL = 5

# Better directly use IP address of the container: 
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' etcd-local
ETCD_HOST = "172.17.0.2"
ETCD_PORT = 2379

# Endpoint of the program.
def main(server_name):
    # Create a new client to etcd.
    client = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)

    while True:
        is_leader, lease = leader_election(client, server_name)

        if is_leader:
            print("I am the leader.")
            on_leadership_gained(lease)
        else:
            print("I am the follower.")
            wait_for_next_election(client)

# This election mechanism consists of all clients trying to put their name
# into a single key, but in a way that only works if the key does not
# exists (or has expired before).
def leader_election(client, server_name):
    print("New leader election happening")
    # Create a lease before creating a key. This way, if this client ever
    # lets the lease expire, the keys associated with that lease will all
    # exprire as well.
    # Here, if the client fails to renew lease (network partition or
    # machine goes down), then the leader election key will
    # expire.
    lease = client.lease(LEADER_LEASE_TTL)

    # Try to create the key with server name as the value. If it fails, then
    # another server got there first.
    is_leader = try_insert(client, LEADER_KEY, server_name, lease)
    return is_leader, lease

def on_leadership_gained(lease):
    while True:
        # As long as this process is alive and we're the leader,
        # we try to renew the lease. We don't give up leadership
        # unless the process / machine crashes or some exception
        # is raised.
        try:
            print("Refreshing lease; still the leader.")
            lease.refresh()
            # This is where the business logic would go.
            do_work()
        except Exception:
            print("\nRevoking lease; no longer the leader")
            # Here we most likely got a client timeout (from
            # network issue). Try to revoke the current lease
            # so another member can get leadership.
            lease.revoke()
            return
        except KeyboardInterrupt:
            print("\nRevoking lease; no longer the leader")
            # Here we're killing the process. Revoke the lease and exit.
            lease.revoke()
            sys.exit(1)

def wait_for_next_election(client):
    election_event = Event()

    def watch_callback(resp):
        for event in resp.events:
            # For each event in the watch event, if the event is a deletion
            # it means the key expired / got deleted, which means the
            # leadership is up for grabs.
            if isinstance(event, etcd3.events.DeleteEvent):
                print("LEADERSHIP CHANGE REQUIRED")
                election_event.set()

    watch_id = client.add_watch_callback(LEADER_KEY, watch_callback)
    
    # While we haven't seen that leadership needs change, just sleep.
    try:
        while not election_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        client.cancel_watch(watch_id)
        sys.exit(1)

    # Cancel the watch; we see that election should happen again.
    client.cancel_watch(watch_id)

# Try to insert a key into etcd with a value and a lease. If the lease expires
# that key will get automatically deleted behind the scenes. If that key
# was already present, this will raise an exception.
def try_insert(client, key, value, lease):
    insert_succeeded, _ = client.transaction(
        failure=[],
        success=[client.transactions.put(key, value, lease)],
        compare=[client.transactions.version(key) == 0],
    )
    return insert_succeeded

def do_work():
    time.sleep(1)

if __name__ == "__main__":
    server_name = sys.argv[1]
    main(server_name)
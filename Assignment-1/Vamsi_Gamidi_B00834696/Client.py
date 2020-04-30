import random
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import Server

class Client:

    def send_request(self, user_type_prob):
        cloud_request_load_balancer = Server.CloudRequestLoadBalancer()
        client_id = random.randint(0,10000000)
        users = ['Public Cloud User', 'Hybrid Cloud User', 'Private Cloud User']
        print("User id", client_id, users[user_type_prob-1])
        cloud_request_load_balancer.service(client_id, user_type_prob, "Request")

    def initialize_users_services(self):
        user_types = [1, 2, 3]
        user_type_probabilities = [0.3, 0.2, 0.5]
        user_count = 1000
        for _ in range(user_count):
            pass
        for _ in range(user_count):
            user_type_prob = random.choices(user_types, user_type_probabilities)
            self.send_request(user_type_prob[0])

        cloud_request_load_balancer = Server.CloudRequestLoadBalancer()
        print(cloud_request_load_balancer.resource_utilization)

        # plotting graph for public cloud users
        x = range(len(cloud_request_load_balancer.resource_utilization[1]))
        y = cloud_request_load_balancer.resource_utilization[1]
        plt.plot(x, y, label='public cloud user', color = 'black')

        # plotting graph for hybrid cloud users
        x = range(len(cloud_request_load_balancer.resource_utilization[2]))
        y = cloud_request_load_balancer.resource_utilization[2]
        plt.plot(x, y, label='hybrid cloud user', color = 'red')

        # plotting graph for private cloud users
        x = range(len(cloud_request_load_balancer.resource_utilization[3]))
        y = cloud_request_load_balancer.resource_utilization[3]
        plt.plot(x, y, label='private cloud user', color = 'purple')
        plt.legend()
        plt.show()

client = Client()
client.initialize_users_services()
import random
from concurrent.futures import ThreadPoolExecutor

class CloudResourceAllocation:
    def __init__(self, private_res_count, hybrid_res_count, public_res_count):
        self.private_res_count = private_res_count
        self.hybrid_res_count = hybrid_res_count
        self.public_res_count = public_res_count

    def initialize_lists(self):
        public_cloud_users = []
        private_cloud_users = []
        hybrid_cloud_users = []

    def available_cloud_resources(self, user_type):
        if user_type == 3:
            return self.private_res_count
        elif user_type == 2:
            return self.hybrid_res_count
        else:
            return self.public_res_count

    def obtain_cloud_resource(self, res_count, user_type):
        if user_type == 3:
            self.private_res_count -= res_count
        elif user_type == 2:
            self.hybrid_res_count -= res_count
        else:
            self.public_res_count -= res_count

    def free_cloud_resource(self, res_count, user_type):
        if user_type == 3:
            self.private_res_count += res_count
        elif user_type == 2:
            self.hybrid_res_count += res_count
        else:
            self.public_res_count += res_count

def singleton(cls):
    obj = cls()
    cls.__new__ = staticmethod(lambda cls: obj)
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls


@singleton
class CloudRequestLoadBalancer:
    request_list = []

    def __init__(self):
        self.request_list = []
        self.resource_utilization = {1:[], 2:[], 3:[]}
        self.pool = CloudResourceAllocation(50, 30, 20)

    def request_resource(self, user_id, user_type, resources_required):
        auto_scale = AutoScale(resources_required, user_type)
        auto_scale.scale_requests()
        CloudRequestLoadBalancer().task_complete(user_id, user_type, resources_required)

    def service(self, user_id, user_type, text):
        resources_required = random.randint(1, user_type*2+1)
        print("resources required:", resources_required)
        self.pool.obtain_cloud_resource(resources_required, user_type)

        self.request_list.append(user_id)
        self.request_resource(user_id, user_type, resources_required)

    def task_complete(self, user_id, user_type, resources_used):
        self.request_list.remove(user_id)
        self.resource_utilization[user_type].append(self.pool.available_cloud_resources(user_type))
        self.pool.free_cloud_resource(resources_used, user_type)
        print("Task completed")

class Task:
    def __init__(self, resources):
        self.resources = resources

    def execute(self, requests_completed = 100):
        for _ in range(self.resources):
            for count in range(round(requests_completed/self.resources)):
                if count+1 == requests_completed:
                    print()
                    return True

    def complete(self, requests_completed):
        return self.execute(requests_completed)

class AutoScale:
    def __init__(self, resources_required, user_type):
        self.resources_required = resources_required
        self.user_type = user_type

    def scale_requests(self):
        executor = ThreadPoolExecutor(max_workers=self.resources_required)
        if self.user_type == 3:
            print("Private Cloud User: Autoscaling Completed")
            task = Task(self.resources_required)
            executor.submit(task.execute())
        elif self.user_type == 2:
            print("Hybrid Cloud User: Autoscaling will be performed after 60% of requests")
            partial_task = Task(1)
            if partial_task.complete(60):
                print("Autoscaling Completed")
                finish_task = Task(self.resources_required-1)
                executor.submit(finish_task.execute())
        else:
            print("Public Cloud User: No Autoscaling")
            task = Task(self.resources_required)
            executor.submit(task.execute())

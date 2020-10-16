# Copyright 2019 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Creates deployment, service, and ingress objects. The ingress allows external
network access to the cluster.
"""

from kubernetes import client, config

def create_service_lb():
    core_v1_api = client.CoreV1Api()
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="lb-example"
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "deployment"},
            type="LoadBalancer",
            ports=[client.V1ServicePort(
                port=5678,
                target_port=5678
            )]
        )
    )
    # Creation of the Deployment in specified namespace
    # (Can replace "default" with a namespace you may have created)
    core_v1_api.create_namespaced_service(namespace="default", body=body)


def update_lb(api, svc):
    svc.spec.external_i_ps =  ["10.0.0.1"]
    ingress = client.V1LoadBalancerIngress(ip="123.123.123.123", hostname="dims.dk")
    lb = client.V1LoadBalancerStatus([ingress])
    service_status = client.V1ServiceStatus(lb)
    svc.status = service_status
    api.patch_namespaced_service(namespace="default",body=svc, name=svc.metadata.name)


def main():
    # Fetching and loading local Kubernetes Information
    config.load_kube_config()
    apps_v1_api = client.AppsV1Api()

    v1 = client.CoreV1Api()
    svc = v1.list_service_for_all_namespaces(watch=False)

    #create_service_lb()
    for s in svc.items:
        if s.spec.type == "LoadBalancer":
            print("Updating LB service: {}".format(s.metadata.name))
            update_lb(v1,s)

if __name__ == "__main__":
    main()


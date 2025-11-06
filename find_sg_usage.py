import boto3

def find_ec2_instances(sg_id, region):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances(
        Filters=[{"Name": "instance.group-id", "Values": [sg_id]}]
    )
    instances = []
    for r in response["Reservations"]:
        for i in r["Instances"]:
            instances.append(i["InstanceId"])
    return instances


def find_enis(sg_id, region):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_network_interfaces(
        Filters=[{"Name": "group-id", "Values": [sg_id]}]
    )
    return [eni["NetworkInterfaceId"] for eni in response["NetworkInterfaces"]]


def find_rds_instances(sg_id, region):
    rds = boto3.client("rds", region_name=region)
    response = rds.describe_db_instances()
    return [
        db["DBInstanceIdentifier"]
        for db in response["DBInstances"]
        if any(sg["VpcSecurityGroupId"] == sg_id for sg in db["VpcSecurityGroups"])
    ]


def find_docdb_clusters(sg_id, region):
    client = boto3.client("docdb", region_name=region)
    response = client.describe_db_clusters()
    return [
        db["DBClusterIdentifier"]
        for db in response["DBClusters"]
        if any(sg["VpcSecurityGroupId"] == sg_id for sg in db["VpcSecurityGroups"])
    ]


def find_elasticache_clusters(sg_id, region):
    client = boto3.client("elasticache", region_name=region)
    response = client.describe_cache_clusters(ShowCacheNodeInfo=False)
    return [
        c["CacheClusterId"]
        for c in response["CacheClusters"]
        if any(sg["SecurityGroupId"] == sg_id for sg in c.get("SecurityGroups", []))
    ]


def find_opensearch_domains(sg_id, region):
    client = boto3.client("opensearch", region_name=region)
    domains = client.list_domain_names()["DomainNames"]
    results = []
    for d in domains:
        info = client.describe_domain(DomainName=d["DomainName"])
        sg_list = info["DomainStatus"].get("VPCOptions", {}).get("SecurityGroupIds", [])
        if sg_id in sg_list:
            results.append(d["DomainName"])
    return results


def find_elbv2_loadbalancers(sg_id, region):
    client = boto3.client("elbv2", region_name=region)
    lbs = client.describe_load_balancers()["LoadBalancers"]
    return [lb["LoadBalancerName"] for lb in lbs if sg_id in lb.get("SecurityGroups", [])]


def find_ecs_services(sg_id, region):
    ecs = boto3.client("ecs", region_name=region)
    clusters = ecs.list_clusters()["clusterArns"]
    results = []
    for cluster in clusters:
        services = ecs.list_services(cluster=cluster)["serviceArns"]
        if not services:
            continue
        desc = ecs.describe_services(cluster=cluster, services=services)
        for s in desc["services"]:
            sg_list = s.get("networkConfiguration", {}).get("awsvpcConfiguration", {}).get("securityGroups", [])
            if sg_id in sg_list:
                results.append(f"{s['serviceName']} ({cluster})")
    return results


def find_eks_clusters(sg_id, region):
    eks = boto3.client("eks", region_name=region)
    clusters = eks.list_clusters()["clusters"]
    results = []
    for c in clusters:
        desc = eks.describe_cluster(name=c)
        sg_list = desc["cluster"]["resourcesVpcConfig"]["securityGroupIds"]
        if sg_id in sg_list:
            results.append(c)
    return results


def find_redshift_clusters(sg_id, region):
    client = boto3.client("redshift", region_name=region)
    clusters = client.describe_clusters()["Clusters"]
    return [
        c["ClusterIdentifier"]
        for c in clusters
        if any(sg["VpcSecurityGroupId"] == sg_id for sg in c.get("VpcSecurityGroups", []))
    ]


def find_emr_clusters(sg_id, region):
    client = boto3.client("emr", region_name=region)
    clusters = client.list_clusters(ClusterStates=["STARTING", "RUNNING", "WAITING"])["Clusters"]
    results = []
    for c in clusters:
        desc = client.describe_cluster(ClusterId=c["Id"])
        sg_list = [
            desc["Cluster"]["Ec2InstanceAttributes"].get("EmrManagedMasterSecurityGroup"),
            desc["Cluster"]["Ec2InstanceAttributes"].get("EmrManagedSlaveSecurityGroup"),
        ]
        if sg_id in sg_list:
            results.append(c["Name"])
    return results


def find_beanstalk_envs(sg_id, region):
    client = boto3.client("elasticbeanstalk", region_name=region)
    envs = client.describe_environments()["Environments"]
    results = []
    for e in envs:
        cfgs = client.describe_configuration_settings(
            ApplicationName=e["ApplicationName"],
            EnvironmentName=e["EnvironmentName"]
        )
        for option in cfgs["ConfigurationSettings"][0]["OptionSettings"]:
            if option["OptionName"] == "SecurityGroups" and sg_id in option["Value"]:
                results.append(e["EnvironmentName"])
    return results


def find_sagemaker_endpoints(sg_id, region):
    client = boto3.client("sagemaker", region_name=region)
    endpoints = client.list_endpoints()["Endpoints"]
    results = []
    for e in endpoints:
        desc = client.describe_endpoint(EndpointName=e["EndpointName"])
        sg_list = desc.get("VpcConfig", {}).get("SecurityGroupIds", [])
        if sg_id in sg_list:
            results.append(e["EndpointName"])
    return results


def find_batch_compute_envs(sg_id, region):
    client = boto3.client("batch", region_name=region)
    envs = client.describe_compute_environments()["computeEnvironments"]
    return [
        e["computeEnvironmentName"]
        for e in envs
        if sg_id in e.get("computeResources", {}).get("securityGroupIds", [])
    ]


def find_glue_connections(sg_id, region):
    client = boto3.client("glue", region_name=region)
    conns = client.get_connections()["ConnectionList"]
    return [
        c["Name"]
        for c in conns
        if sg_id in c.get("PhysicalConnectionRequirements", {}).get("SecurityGroupIdList", [])
    ]


def main():
    region = input("Ingrese la región AWS (ej: us-east-1): ").strip()
    sg_id = input("Ingrese el ID del Security Group (ej: sg-0abc12345): ").strip()

    print(f"\n🔍 Buscando recursos asociados al Security Group {sg_id} en {region}...\n")

    checks = {
        "EC2 Instances": find_ec2_instances,
        "ENIs": find_enis,
        "RDS Instances": find_rds_instances,
        "DocumentDB": find_docdb_clusters,
        "ElastiCache": find_elasticache_clusters,
        "OpenSearch": find_opensearch_domains,
        "ELBv2 LoadBalancers": find_elbv2_loadbalancers,
        "ECS Services": find_ecs_services,
        "EKS Clusters": find_eks_clusters,
        "Redshift Clusters": find_redshift_clusters,
        "EMR Clusters": find_emr_clusters,
        "Elastic Beanstalk Environments": find_beanstalk_envs,
        "SageMaker Endpoints": find_sagemaker_endpoints,
        "AWS Batch Compute Envs": find_batch_compute_envs,
        "Glue Connections": find_glue_connections,
    }

    found_any = False

    for name, func in checks.items():
        try:
            results = func(sg_id, region)
            if results:
                print(f"✅ {name}:\n   {results}\n")
                found_any = True
            else:
                print(f"🔸 {name}: no se encontraron recursos asociados.")
        except Exception as e:
            print(f"⚠️  {name}: Error ({e})")

    print("\n🧾 --- Resumen de búsqueda ---")
    print(f"🔍 Servicios analizados: {len(checks)}")
    if not found_any:
        print("❌ No se encontró ningún recurso usando este Security Group.")
    else:
        print("✅ Se encontraron recursos asociados en uno o más servicios.")

    print("\n🏁 Búsqueda finalizada.\n")


if __name__ == "__main__":
    main()

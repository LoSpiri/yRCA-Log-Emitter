import yaml, sys, subprocess

def configureAccessLogs(config):
    config["spec"]["meshConfig"]["accessLogFile"] = "/dev/stdout"
    config["spec"]["meshConfig"]["accessLogEncoding"] = "JSON"
    config["spec"]["meshConfig"]["accessLogFormat"] = '{\n  "start_time": "%START_TIME%",\n  "method": "%REQ(:METHOD)%",\n  "protocol": "%PROTOCOL%",\n  "response_code": "%RESPONSE_CODE%",\n  "response_code_details": "%RESPONSE_CODE_DETAILS%",\n  "connection_termination_details": "%CONNECTION_TERMINATION_DETAILS%",\n  "upstream_request_attempt_count": "%UPSTREAM_REQUEST_ATTEMPT_COUNT%",\n  "duration": "%DURATION%",\n  "request_duration": "%REQUEST_DURATION%",\n  "request_tx_duration": "%REQUEST_TX_DURATION%",\n  "response_duration": "%RESPONSE_DURATION%",\n  "response_tx_duration": "%RESPONSE_TX_DURATION%",\n  "response_flags": "%RESPONSE_FLAGS%",\n  "route_name": "%ROUTE_NAME%",\n  "authority": "%REQ(:AUTHORITY)%",\n  "connection_id": "%CONNECTION_ID%",\n  "x-request-id": "%REQ(X-REQUEST-ID)%",\n  "x-envoy-upstream-service-time": "%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%"\n}'
    return config

def main():
    argumentsNumber = len(sys.argv)
    if(argumentsNumber>2):
        print("Too many arguments")
    elif(argumentsNumber<2):
        print("Using Istio 'default' configuration")
        newFileName = "defaultAccessLogEnabled2.yaml"
        with open(newFileName,"w") as fw:
            yaml.dump(
                {'apiVersion': 'install.istio.io/v1alpha1', 'kind': 'IstioOperator', 'metadata': {'namespace': 'istio-system'}, 'spec': {'components': {'base': {'enabled': True}, 'cni': {'enabled': False}, 'egressGateways': [{'enabled': False, 'name': 'istio-egressgateway'}], 'ingressGateways': [{'enabled': True, 'name': 'istio-ingressgateway'}], 'istiodRemote': {'enabled': False}, 'pilot': {'enabled': True}}, 'hub': 'gcr.io/istio-testing', 'meshConfig': {'defaultConfig': {'proxyMetadata': {}}, 'enablePrometheusMerge': True, 'accessLogFile': '/dev/stdout', 'accessLogEncoding': 'JSON', 'accessLogFormat': '{\n  "start_time": "%START_TIME%",\n  "method": "%REQ(:METHOD)%",\n  "protocol": "%PROTOCOL%",\n  "response_code": "%RESPONSE_CODE%",\n  "response_code_details": "%RESPONSE_CODE_DETAILS%",\n  "connection_termination_details": "%CONNECTION_TERMINATION_DETAILS%",\n  "upstream_request_attempt_count": "%UPSTREAM_REQUEST_ATTEMPT_COUNT%",\n  "duration": "%DURATION%",\n  "request_duration": "%REQUEST_DURATION%",\n  "request_tx_duration": "%REQUEST_TX_DURATION%",\n  "response_duration": "%RESPONSE_DURATION%",\n  "response_tx_duration": "%RESPONSE_TX_DURATION%",\n  "response_flags": "%RESPONSE_FLAGS%",\n  "route_name": "%ROUTE_NAME%",\n  "authority": "%REQ(:AUTHORITY)%",\n  "connection_id": "%CONNECTION_ID%",\n  "x-request-id": "%REQ(X-REQUEST-ID)%",\n  "x-envoy-upstream-service-time": "%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%"\n}'}, 'tag': 'latest', 'values': {'base': {'enableCRDTemplates': False, 'validationURL': ''}, 'defaultRevision': '', 'gateways': {'istio-egressgateway': {'autoscaleEnabled': True, 'env': {}, 'name': 'istio-egressgateway', 'secretVolumes': [{'mountPath': '/etc/istio/egressgateway-certs', 'name': 'egressgateway-certs', 'secretName': 'istio-egressgateway-certs'}, {'mountPath': '/etc/istio/egressgateway-ca-certs', 'name': 'egressgateway-ca-certs', 'secretName': 'istio-egressgateway-ca-certs'}], 'type': 'ClusterIP'}, 'istio-ingressgateway': {'autoscaleEnabled': True, 'env': {}, 'name': 'istio-ingressgateway', 'secretVolumes': [{'mountPath': '/etc/istio/ingressgateway-certs', 'name': 'ingressgateway-certs', 'secretName': 'istio-ingressgateway-certs'}, {'mountPath': '/etc/istio/ingressgateway-ca-certs', 'name': 'ingressgateway-ca-certs', 'secretName': 'istio-ingressgateway-ca-certs'}], 'type': 'LoadBalancer'}}, 'global': {'configValidation': True, 'defaultNodeSelector': {}, 'defaultPodDisruptionBudget': {'enabled': True}, 'defaultResources': {'requests': {'cpu': '10m'}}, 'imagePullPolicy': '', 'imagePullSecrets': [], 'istioNamespace': 'istio-system', 'istiod': {'enableAnalysis': False}, 'jwtPolicy': 'third-party-jwt', 'logAsJson': False, 'logging': {'level': 'default:info'}, 'meshNetworks': {}, 'mountMtlsCerts': False, 'multiCluster': {'clusterName': '', 'enabled': False}, 'network': '', 'omitSidecarInjectorConfigMap': False, 'oneNamespace': False, 'operatorManageWebhooks': False, 'pilotCertProvider': 'istiod', 'priorityClassName': '', 'proxy': {'autoInject': 'enabled', 'clusterDomain': 'cluster.local', 'componentLogLevel': 'misc:error', 'enableCoreDump': False, 'excludeIPRanges': '', 'excludeInboundPorts': '', 'excludeOutboundPorts': '', 'image': 'proxyv2', 'includeIPRanges': '*', 'logLevel': 'warning', 'privileged': False, 'readinessFailureThreshold': 30, 'readinessInitialDelaySeconds': 1, 'readinessPeriodSeconds': 2, 'resources': {'limits': {'cpu': '2000m', 'memory': '1024Mi'}, 'requests': {'cpu': '100m', 'memory': '128Mi'}}, 'statusPort': 15020, 'tracer': 'zipkin'}, 'proxy_init': {'image': 'proxyv2', 'resources': {'limits': {'cpu': '2000m', 'memory': '1024Mi'}, 'requests': {'cpu': '10m', 'memory': '10Mi'}}}, 'sds': {'token': {'aud': 'istio-ca'}}, 'sts': {'servicePort': 0}, 'tracer': {'datadog': {}, 'lightstep': {}, 'stackdriver': {}, 'zipkin': {}}, 'useMCP': False}, 'istiodRemote': {'injectionURL': ''}, 'pilot': {'autoscaleEnabled': True, 'autoscaleMax': 5, 'autoscaleMin': 1, 'configMap': True, 'cpu': {'targetAverageUtilization': 80}, 'deploymentLabels': None, 'enableProtocolSniffingForInbound': True, 'enableProtocolSniffingForOutbound': True, 'env': {}, 'image': 'pilot', 'keepaliveMaxServerConnectionAge': '30m', 'nodeSelector': {}, 'podLabels': {}, 'replicaCount': 1, 'traceSampling': 1.0}, 'telemetry': {'enabled': True, 'v2': {'enabled': True, 'metadataExchange': {'wasmEnabled': False}, 'prometheus': {'enabled': True, 'wasmEnabled': False}, 'stackdriver': {'configOverride': {}, 'enabled': False, 'logging': False, 'monitoring': False, 'topology': False}}}}}},
                fw,
                default_flow_style=False
            )
        cmd = "istioctl install -f " + newFileName
        subprocess.run(cmd, shell=True)
    else:
        with open(sys.argv[1]) as fr:
            data = yaml.safe_load(fr)
            dataKeys = list(data.keys())
            if("spec" in dataKeys):
                if("meshConfig" in list(data.get("spec"))):
                    data = configureAccessLogs(data)
                else:
                    data["spec"]["meshConfig"] = {}
                    data = configureAccessLogs(data)    
                newFileName = sys.argv[1].replace(".","AccessLogsEnabled.")
                with open(newFileName,"w") as fw:
                    yaml.dump(data,fw,default_flow_style=False)
                cmd = "istioctl install -f " + newFileName
                subprocess.run(cmd, shell=True)
            else:
                print("spec not found, the configuration is not valid")

if(__name__ == "__main__"):
    main()
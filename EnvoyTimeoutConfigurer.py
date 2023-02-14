import yaml, sys, subprocess

def main():
    argumentsNumber = len(sys.argv)
    if(argumentsNumber>3):
        print("Too many arguments")
    elif(argumentsNumber<2):
        print("Service name not specified")
    elif(argumentsNumber<3):
        print("Timeout duration not specified")
    else:
        serviceName = sys.argv[1]
        timeoutDuration = sys.argv[2]
        newFileName = serviceName + "_TimeoutEnvoy"
        with open(newFileName + ".yaml","w") as f:
            defaultVirtualService = {
                "apiVersion": "networking.istio.io/v1alpha3",
                "kind": "VirtualService",
                "metadata": {
                    "name": "",
                },
                "spec": {
                    "hosts": [
                        ""
                    ],
                    "http": [
                        {
                            "route": [
                                {
                                    "destination": {
                                        "host": ""
                                    },
                                }
                            ],
                            "timeout": ""
                        }
                    ]
                }
            }
            defaultVirtualService["metadata"]["name"] = serviceName + "-timeout"
            defaultVirtualService["spec"]["hosts"][0] = serviceName
            defaultVirtualService["spec"]["http"][0]["route"][0]["destination"]["host"] = serviceName
            defaultVirtualService["spec"]["http"][0]["timeout"] = timeoutDuration + "s"
            yaml.dump(
                defaultVirtualService,
                f,
                default_flow_style=False
            )
        print("Applying the VirtualService...")
        cmd = "kubectl apply -f " + newFileName + ".yaml"
        subprocess.run(cmd,shell=True)
        print("Istio has installed the timeout for the service " + serviceName + " with duration " + timeoutDuration)

        
if(__name__ == "__main__"):
    main()
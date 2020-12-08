NS=mth
REPO=markthebault/azurefunction-queue
TAG=latest

all: build-function deploy azure

deploy:
	helm repo add kedacore https://kedacore.github.io/charts
	kubectl create namespace $(NS) || true
	kubectl apply -n $(NS) -f keda-msi.yaml
	helm upgrade -i keda kedacore/keda --namespace $(NS) --set podIdentity.activeDirectory.identity=keda-msi

build-function:
	docker build -t $(REPO):$(TAG) test
	docker push $(REPO):$(TAG)

azure:
	kubectl apply -n $(NS) -f queue-reader-func.yaml
	kubectl apply -n $(NS) -f sa-evt-triggers.yaml

azure.delete:
	kubectl delete -n $(NS) -f queue-reader-func.yaml
	kubectl delete -n $(NS) -f sa-evt-triggers.yaml


destroy: azure.delete
	helm uninstall -n $(NS) keda
	kubectl delete -n $(NS) -f keda-msi.yaml
	kubectl delete -f https://raw.githubusercontent.com/kedacore/keda/main/config/crd/bases/keda.sh_scaledobjects.yaml
	kubectl delete -f https://raw.githubusercontent.com/kedacore/keda/main/config/crd/bases/keda.sh_scaledjobs.yaml
	kubectl delete -f https://raw.githubusercontent.com/kedacore/keda/main/config/crd/bases/keda.sh_triggerauthentications.yaml

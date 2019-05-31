GIT_BACKEND=https://github.com/kwkoo/pywordcount.git

.PHONY: deploy newproject entityextract exposeentityextract wordcloud exposewordcloud

deploy: newproject exposeentityextract exposewordcloud

newproject:
	@echo "Creating new project..."
	oc new-project mha

entityextract:
	@echo "Creating entity extract..."
	oc new-app \
		registry.access.redhat.com/rhscl/python-36-rhel7:latest~$(GIT_BACKEND) \
		--context-dir=entity-extract \
		--name=wc-ety-extract

exposeentityextract: entityextract
	@echo "Exposing entity extract..."
	sleep 5
	oc expose svc/wc-ety-extract

wordcloud:
	@echo "Creating word cloud..."
	oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~$(GIT_BACKEND) \
		--context-dir=world-cloud \
		--name=wc-wcloud

exposewordcloud: wordcloud
	@echo "Exposing word cloud..."
	sleep 5
	oc expose svc/wc-wcloud

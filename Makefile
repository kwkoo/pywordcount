GIT_BACKEND=https://github.com/kwkoo/pywordcount.git
#GIT_BACKEND=https://github.com/robinfoe/pywordcount.git
PROJECT=mha

.PHONY: deploy newproject pvc cm wc-web configvolumes exposewcweb entityextract exposeentityextract sentimentanalysis topicdetection wordcloud exposewordcloud

deployall: newproject exposeentityextract sentimentanalysis topicdetection exposewordcloud exposewcweb

deploycore: newproject exposeentityextract exposewordcloud

newproject:
	@echo "Creating new project..."
	oc new-project $(PROJECT)

pvc:
	@echo "Creating PVC..."
	oc create -f pvc.yaml

 cm:
	@echo "Creating config map..."
	oc create -f word-config.yaml

 wc-web: pvc cm
	@echo "Creating wc-web..."	
	oc new-app \
	  registry.access.redhat.com/rhscl/python-27-rhel7:latest~$(GIT_BACKEND) \
	  --context-dir=web \
	  --name=wc-web \
	  --env=URL_WORLD_CLOUD_API=http://wc-wcloud.$(PROJECT).svc:8080/wordcloud_api \
	  --env=URL_ENTITY_API=http://wc-ety-extract.$(PROJECT).svc:8080/extract_entity_api \
	  --env=URL_TOPIC_API=http://wc-topic.$(PROJECT).svc:8080/topic_detection_api \
	  --env=URL_SENTIMENT_API=http://wc-sentiment.$(PROJECT).svc:8080/sentiment_analysis_api

 configvolumes: wc-web
	@echo "Configuring volumes..."	
	oc set volume \
	  dc/wc-web \
	  --add \
	  --name=cfmapsearchword \
	  --type=configmap \
	  --configmap-name=word-config-map \
	  --mount-path=/opt/app-root/src/vocab
	oc set volume \
	  dc/wc-web \
	  --add \
	  --name=v-web-output-keyword \
	  --type=persistentVolumeClaim \
	  --claim-name=web-output-keyword \
	  --mount-path=/opt/app-root/src/outputs/keywordhits
	oc set volume \
	  dc/wc-web \
	  --add \
	  --name=v-web-upload-folder \
	  --type=persistentVolumeClaim \
	  --claim-name=web-upload-folder \
	  --mount-path=/opt/app-root/src/uploads

 exposewcweb: configvolumes
	@echo "Exposing wc-web..."
	oc expose svc/wc-web

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

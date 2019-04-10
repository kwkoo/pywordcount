# pywordcount
Quick start python based word count 


## Configure PV 
oc create -f pvc.yaml

## Configure Config Map
oc create -f word-config.yaml

## Configure wc-web
oc new-app registry.access.redhat.com/rhscl/python-27-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
--context-dir=web \
--name=wc-web \
--env=URL_WORLD_CLOUD_API=http://wc-wcloud.mha.svc:8080/wordcloud_api \
--env=URL_ENTITY_API=http://wc-ety-extract.mha.svc:8080/extract_entity_api \
--env=URL_TOPIC_API=http://wc-topic.mha.svc:8080/topic_detection_api \
--env=URL_SENTIMENT_API=http://wc-sentiment.mha.svc:8080/sentiment_analysis_api 



## Configure Volume
oc set volume dc/wc-web --add --name=cfmapsearchword --type=configmap --configmap-name=word-config-map --mount-path=/opt/app-root/src/vocab


oc set volume dc/wc-web --add --name=v-web-output-keyword --type=persistentVolumeClaim --claim-name=web-output-keyword --mount-path=/opt/app-root/src/outputs/keywordhits

oc set volume dc/wc-web --add --name=v-web-upload-folder --type=persistentVolumeClaim --claim-name=web-upload-folder --mount-path=/opt/app-root/src/uploads

## Configure route
oc expose svc wc-web


## Configure entity extract
oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
--context-dir=entity-extract \
--name=wc-ety-extract

## Configure sentiment analysis
oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
--context-dir=sentiment-anaysis \
--name=wc-sentiment

## configure topic detectiom
oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
--context-dir=topic-detection \
--name=wc-topic

## Configure World Cloud
oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
--context-dir=world-cloud \
--name=wc-wcloud

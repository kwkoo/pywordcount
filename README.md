# pywordcount
Quick start python based word count 




oc new-app registry.access.redhat.com/rhscl/python-27-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
	--context-dir=web \
	--name=wc-web \
	--env=URL_WORLD_CLOUD_API=http://wc-wcloud.mha.svc:8080/wordcloud_api \
	--env=URL_ENTITY_API=http://wc-ety-extract.mha.svc:8080/extract_entity_api \
	--env=URL_TOPIC_API=http://wc-topic.mha.svc:8080/topic_detection_api \
	--env=URL_SENTIMENT_API=http://wc-sentiment.mha.svc:8080/sentiment_analysis_api 


oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
	--context-dir=entity-extract \
	--name=wc-ety-extract

oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
	--context-dir=sentiment-anaysis \
	--name=wc-sentiment

oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
	--context-dir=topic-detection \
	--name=wc-topic


oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:latest~https://github.com/robinfoe/pywordcount.git \
	--context-dir=world-cloud \
	--name=wc-wcloud

oc expose svc wc-web






oc new-app https://github.com/robinfoe/pywordcount.git --context-dir=sentiment-anaysis
oc new-app https://github.com/robinfoe/pywordcount.git --context-dir=topic-detection
oc new-app https://github.com/robinfoe/pywordcount.git --context-dir=world-cloud



oc new-app https://github.com/sclorg/s2i-ruby-container.git \
    --context-dir=2.0/test/puma-test-app


oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git



https://github.com/sclorg/ruby-ex.git
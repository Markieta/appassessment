FROM registry.access.redhat.com/ubi8/python-36:1-155
USER root
ADD ./report.py ./
ADD ./requirements.txt ./
ENV HOME=/tmp/

RUN pip install -r ./requirements.txt
# RUN yum install wget -y
# Install OC CLI
RUN curl https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/oc.tar.gz --output ./oc.tar.gz
RUN tar -xzf ./oc.tar.gz -C /usr/local/bin/
RUN chmod 755 /usr/local/bin/oc
RUN oc version
USER 1001
CMD ["python3" "./report.py" "-n ${TARGET_NAMESPACE}"]
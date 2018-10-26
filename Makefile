# can be overridden by setting command line env
imageName := "tess4"

build:
	docker build -t ${imageName} .

run-shell:
	docker run --device=/dev/video0 --rm -it -v ${PWD}:${PWD} -w ${PWD} ${imageName} /bin/bash


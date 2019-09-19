CONTAINER_NAME:=vlad
IMAGE_NAME:=rootfsimage

default: plugin

$(IMAGE_NAME):
	@mkdir -p tmp/
	@cp -r ../vlad/ tmp/
	@cp ../main.py tmp/
	@cp ../requirements.txt tmp/
	docker build -t $(IMAGE_NAME) .
	@rm -r tmp/
	@mkdir -p rootfs
	docker create --name $(CONTAINER_NAME) $(IMAGE_NAME) true
	docker export $(CONTAINER_NAME) | tar -x -C rootfs

plugin: $(IMAGE_NAME)
	docker plugin create vlad .


.PHONY: clean
clean:
	@docker rm -vf $(CONTAINER_NAME)
	@docker rmi -f $(IMAGE_NAME)
	@rm -rf tmp/

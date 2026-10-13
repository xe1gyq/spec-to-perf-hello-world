CC = gcc
CFLAGS = -O2 -g -std=c11 -Wall -Wextra -Werror -fno-omit-frame-pointer

.PHONY: all test demo profile clean
all: build/matrix-scan
build/matrix-scan: src/main.c
	mkdir -p build
	$(CC) $(CFLAGS) $< -o $@
test: all
	python3 tests/test_cli.py
demo: all
	./build/matrix-scan row 2048 20
	./build/matrix-scan column 2048 20
profile: all
	bash scripts/profile.sh
clean:
	rm -rf build

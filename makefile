all: main.c
	gcc main.c -o main -g -lncurses
debug:
	make all
	gdb main
run:
	make all
	./main
clean:
	rm -rf main

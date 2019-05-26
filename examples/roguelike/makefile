build:
	cd ../..; ./main compile examples/roguelike/main.pw; cd out/target; clang++ main.cpp -O3 -std=c++17 -o main -lSDL2 -lSDL2_image
	cp *.bmp ../../out/target; ../../out/target/main
	
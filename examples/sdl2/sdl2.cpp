#include "../cable/cable.cpp"
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_ttf.h>
#include <iostream>
#include <string>
#include <stdio.h>



SDL_Window* window = NULL;
Map<std::string, SDL_Texture*> textures = Map<std::string, SDL_Texture*>();
SDL_Rect texture_rect;
SDL_Renderer *renderer = NULL;

bool sdl_init(std::string window_name, int width, int height) {
    // SDL_Init(SDL_INIT_VIDEO);
    // window = SDL_CreateWindow("SDL Tutorial", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    
    //Initialization flag
	bool success = true;

	//Initialize SDL
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
		success = false;
	} else {
		//Create window
		window = SDL_CreateWindow(window_name.c_str(), SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_SHOWN);
		if (window == NULL) {
			printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
			success = false;
		} else {
			//Get window surface
            renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
		}
	}

    std::cout << SDL_GetError() << std::endl;

	return success;
}


void sdl_close() {
	SDL_DestroyWindow(window);
	window = NULL;
	SDL_Quit();
}


void sdl_blit_image(std::string path, int x, int y, int w, int h) {
    Option<SDL_Texture*> texture = textures.get(path);

    if (texture) {
        texture_rect.x = x;
        texture_rect.y = y;
        texture_rect.w = w;
        texture_rect.h = h;

        SDL_RenderCopy(renderer, texture.unwrap(), NULL, &texture_rect);
    } else {
        textures.set(path, IMG_LoadTexture(renderer, path.c_str()));
        sdl_blit_image(path, x, y, w, h);
    }
}


void sdl_clear() {
    SDL_RenderClear(renderer); //clears the renderer
}


void sdl_refresh() {
    SDL_RenderPresent(renderer); //updates the renderer
}



// int main() {
//     if (!init())
//         std::cout << "ERROR IN INIT" << std::endl;
//     else
//         std::cout << "SUCCESS" << std::endl;


//     SDL_Event e;
//     bool quit = false;
//     while (!quit){
//         while (SDL_PollEvent(&e)){
//             if (e.type == SDL_QUIT){
//                 quit = true;
//             }
//             if (e.type == SDL_KEYDOWN){
//                 quit = true;
//             }
//             if (e.type == SDL_MOUSEBUTTONDOWN){
//                 quit = true;
//             }
//         }

//         clear();
//         blit_image("hello_world.bmp", 50, 200, 100, 100);
//         refresh();
//     }


//     close();
// }

std::string sdl_key_to_string(SDL_Keycode k) {
    switch (k) {
        case SDLK_a: return "a";
        case SDLK_b: return "b";
        case SDLK_c: return "c";
        case SDLK_d: return "d";
        case SDLK_e: return "e";
        case SDLK_f: return "f";
        case SDLK_g: return "g";
        case SDLK_h: return "h";
        case SDLK_i: return "i";
        case SDLK_j: return "j";
        case SDLK_k: return "k";
        case SDLK_l: return "l";
        case SDLK_m: return "m";
        case SDLK_n: return "n";
        case SDLK_o: return "o";
        case SDLK_p: return "p";
        case SDLK_q: return "q";
        case SDLK_r: return "r";
        case SDLK_s: return "s";
        case SDLK_t: return "t";
        case SDLK_u: return "u";
        case SDLK_v: return "v";
        case SDLK_w: return "w";
        case SDLK_x: return "x";
        case SDLK_y: return "y";
        case SDLK_z: return "z";
        default: return "?";
    }
}

std::string sdl_get_event() {
    SDL_Event e;
    while (SDL_PollEvent(&e)) {
        switch (e.type) {
            case SDL_QUIT:
                std::exit(0);
                return "QUIT.";
            case SDL_KEYDOWN:
                return "KEYD" + sdl_key_to_string(e.key.keysym.sym);
            case SDL_KEYUP:
                // return "KEYU" + sdl_key_to_string(e.key.keysym.sym);
                return "KEYU?";
            default: return "NONE.";
        }
    }

    return "NONE.";
}


char sdl_get_key(std::string event) {
    return event[4];
}




const Fn sdl_init_fn = Fn([](Value args) {
    string win_name = args[0].get_string().unwrap();
    int w = args[1].get_i32().unwrap();
    int h = args[2].get_i32().unwrap();
    return Value(sdl_init(win_name, w, h));
});


const Fn sdl_clear_fn = Fn([](Value args) {
    sdl_clear();
    return Value();
});

const Fn sdl_refresh_fn = Fn([](Value args) {
    sdl_refresh();
    return Value();
});


const Fn sdl_blit_fn = Fn([](Value args) {
    string path = args[0].get_string().unwrap();
    int x = args[1].get_i32().unwrap();
    int y = args[2].get_i32().unwrap();
    int w = args[3].get_i32().unwrap();
    int h = args[4].get_i32().unwrap();

    sdl_blit_image(path, x, y, w, h);
    return Value();
});


const Fn sdl_close_fn = Fn([](Value args) {
    sdl_close();
    return Value();
});


const Fn sdl_get_input_fn = Fn([](Value args) {
    return Value(string(1, sdl_get_key(sdl_get_event())));
});



#include <ncurses.h>
#include "../cable/cable.cpp"


const Fn curses_init = Fn([](Value _) {
    initscr();
    cbreak();
    halfdelay(1);
    noecho();
    clear();
    curs_set(0);
    return Value();
});


const Fn curses_write_str = Fn([](Value args) {
    int x = (args[0]).get_i32().unwrap();
    int y = (args[1]).get_i32().unwrap();
    const char *s = (args[2]).to_string().c_str();
    mvaddstr(y, x, s);
    return Value();
});


const Fn curses_refresh = Fn([](Value args) {
    refresh();
    return Value();
});


const Fn curses_clear = Fn([](Value args) {
    clear();
    return Value();
});


const Fn curses_get_char = Fn([](Value args) {
    char ch = getch();
    string s;
    s += ch;
    napms(3);
    return Value(s);
});


const Fn curses_exit = Fn([](Value args) {
    endwin();
    return Value();
});
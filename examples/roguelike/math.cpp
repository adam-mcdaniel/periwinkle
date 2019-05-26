#include "../cable/cable.cpp"
#include <cmath>


const Fn round_fn = Fn([](Value args) {
    return Value(round(args[0].get_f64().unwrap()));
});


const Fn to_float_fn = Fn([](Value args) {
    Value n = args[0];
    switch (n.type) {
        case Type::I32:
            return Value(f64(n.get_i32().unwrap()));
            break;

        case Type::F64:
            return n;
            break;

        default: break;
    }
    return Value();
});


const Fn to_int_fn = Fn([](Value args) {
    Value n = args[0];
    switch (n.type) {
        case Type::I32:
            return n;
            break;

        case Type::F64:
            return Value(i32(n.get_f64().unwrap()));
            break;

        default: break;
    }
    return Value();
});
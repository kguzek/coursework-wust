let curry4 (f: ('w * 'x * 'y * 'z -> 'r)) = fun (w: 'w) (x: 'x) (y: 'y) (z: 'z) -> f(w, x, y, z);;
let curry4 (f: ('w * 'x * 'y * 'z -> 'r)) (w: 'w) (x: 'x) (y: 'y) (z: 'z) = f(w, x, y, z);;

let uncurry4 (f: 'w -> 'x -> 'y -> 'z -> 'r) = fun ((w: 'w), (x: 'x), (y: 'y), (z: 'z)) -> f w x y z;;
let uncurry4 (f: 'w -> 'x -> 'y -> 'z -> 'r) ((w: 'w), (x: 'x), (y: 'y), (z: 'z)) = f w x y z;;

let sum_tupled (w, x, y, z) = w + x + y + z;;
let sum_curried w x y z = w + x + y + z;;

curry4 sum_tupled 1 2 3 4;;
uncurry4 sum_curried (1, 2, 3, 4);;

module type TUPLE_OPERATIONS = sig 
  val element_count : ('a * 'b * 'c) -> 'c;;

  val all_greater_than : (int * int * int) -> int -> bool;;

  val sum_element : (int * int * int) -> int;;

  val subtract : (int * int * int) -> (int * int * int) -> (int * int * int);;

  val all_negative : (int * int * int) -> bool;;
end

module TupleOperations : TUPLE_OPERATIONS = struct
  let element_count (x, y, z) = z;;

  let all_greater_than (x, y, z) value = 
    x > value && y > value && z > value
  ;;

  let sum_element (a, b, c) = a + b + c;;

  let subtract (a, b, c) (d, e, f) = (a - d, b - e, c - f);;

  let all_negative (a, b, c) = a < 0 && b < 0 && c < 0;;
end;;

TupleOperations.element_count (1, 2, 3);;
TupleOperations.element_count (5, 6, 7);;

TupleOperations.all_greater_than (4, 5, 6) 1;;
TupleOperations.all_greater_than (1, 2, 3) 2;;
TupleOperations.all_greater_than (1, 2, 3) 3;;
TupleOperations.all_greater_than (1, 2, 3) 0;;
TupleOperations.all_greater_than (1, 2, -1) 10;;

TupleOperations.sum_element (0, 0, 0);;
TupleOperations.sum_element (-60, 50, 10);;
TupleOperations.sum_element (1, 2, 3);;
TupleOperations.sum_element (5, 5, 5);;

TupleOperations.subtract (1, 2, 3) (1, 2, 3);;
TupleOperations.subtract (1, 2, 3) (4, 5, 6);;
TupleOperations.subtract (2, 3, 4) (1, 2, 3);;

TupleOperations.all_negative (1, 2, 3);;
TupleOperations.all_negative (-1, -2, -3);;
TupleOperations.all_negative (-1, 0, -3);;
TupleOperations.all_negative (0, 0, 0);;
TupleOperations.all_negative (-0, -0, -0);;

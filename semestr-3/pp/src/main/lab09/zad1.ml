module type LIST_OPERATIONS = sig 
  val empty : int list

  val sum : int list -> int

  val filter_even : int list -> int -> int list

  val alternate_merge : int list -> int list -> int list
end

module ListOperations : LIST_OPERATIONS = struct 
  let rec reverse list: int list = 
    let rec aux acc list_tail = 
      match list_tail with
      | [] -> acc
      | head::tail -> aux (head::acc) tail
    in
    aux [] list
  ;;
  
  let empty = [];;

  let sum list = 
    let rec aux (acc: int) (list_tail: int list) = 
    match list_tail with
    | [] -> acc
    | head::tail -> if head < 0 then (aux (acc + head) tail) else (aux acc tail)
    in
    aux 0 list;;

  let filter_even list value = 
    let rec aux acc list_tail = 
      match list_tail with 
        | [] -> acc
        | head::tail -> match (head mod value) with 
          | 0 -> aux (head::acc) tail
          | _ -> aux acc tail
    in
    if value == 0 then failwith "nie można dzielić przez 0" 
    else reverse (aux [] list)
  ;;

  let alternate_merge left right = 
    let rec aux acc left_tail right_tail =
      match left_tail with
        | [] -> if right_tail == [] then acc else (aux acc right_tail [])
        | head::tail -> aux (head::acc) right_tail tail
    in 
    reverse (aux [] left right)
  ;;
end;;

ListOperations.empty;;

ListOperations.sum [1;2;3;-5;-1;-10;0];;
ListOperations.sum [];;
ListOperations.sum [-5];;

ListOperations.filter_even [2;4;6;8;10;12] 2;;
ListOperations.filter_even [2;4;6;8;10;12] 3;;
ListOperations.filter_even [2;4;6;8;10;12] 11;;
ListOperations.filter_even [2;4;6;8;10;12] 1;;
ListOperations.filter_even [] 1;;
ListOperations.filter_even [5] 0;;

ListOperations.alternate_merge [1;3;5] [2;4;6];;
ListOperations.alternate_merge [1;3;5] [2;4;6;7;8;9];;
ListOperations.alternate_merge [1;3;5;7;8;9] [2;4;6];;
ListOperations.alternate_merge [] [2;4;6];;
ListOperations.alternate_merge [] [];;

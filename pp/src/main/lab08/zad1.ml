let rec insert list item =
  match list with
    | [] -> [item]
    | head::tail -> 
      match item <= head with
        | true ->  item::head::tail 
        | false ->  head::(insert tail item)
;;

insert [1;3;5;7] 4;;
insert [1;3;5;7] 5;;
insert [1;3;5;7] 6;;
insert [1;3;5;7] 0;;
insert [1] 0;;
insert [] 0;;
insert [] 30;;

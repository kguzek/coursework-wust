type 'a nlist = Koniec | Element of 'a * ('a nlist);;
type 'a llist = LKoniec | LElement of 'a * (unit -> 'a llist);;

let rec repeat item count =
  if count == 0 then []
  else item::(repeat item (count - 1))

let flatten lists =
  let rec flatten_sublist sub acc =
    match sub with
    | [] -> acc
    | x::xs -> flatten_sublist xs (x::acc)
  in
  let rec aux lists acc =
    match lists with
    | [] -> acc
    | sub::rest -> aux rest (flatten_sublist sub acc)
  in List.rev (aux lists [])
  
let polacz list =
  let rec aux list = match list with
    | [] -> []
    | head::tail -> if head >=0 then (repeat head head)::(aux tail) else failwith "ujemna liczba"
  in flatten (aux list)
;;

let rec lrepeat value count xf =
  if count == 0 then xf()
  else LElement(value, fun () -> (lrepeat value (count - 1) xf))

let rec stworz_lliste lista =
  match lista with
  | [] -> LKoniec
  | head :: tail -> LElement(head, fun () -> stworz_lliste tail)
;;

let rec ltakeall lxs =
  match lxs with
  | LKoniec -> []
  | LElement(x,xf) -> x::ltakeall(xf())
  ;;

let lpolacz lxs =
  let rec aux lxs =
    match lxs with
    | LKoniec -> LKoniec
    | LElement(x, xf) ->
        let rec rep value count cont =
          if count = 0 then cont()
          else LElement (value, fun () -> rep value (count - 1) cont)
        in
        rep x x (fun () -> aux (xf ()))
  in
  aux lxs
;;

polacz [1;2;3];;
polacz [1];;
polacz [1;1;2];;
polacz [0;5;1];;

ltakeall (lpolacz (stworz_lliste [1;2;3]));;
ltakeall (lpolacz (stworz_lliste [1]));;
ltakeall (lpolacz (stworz_lliste [1;1;2]));;
ltakeall (lpolacz (stworz_lliste [0;5;1]));;

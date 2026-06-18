type 'a nlist = Koniec | Element of 'a * ('a nlist);;
type 'a llist = LKoniec | LElement of 'a * (unit -> 'a llist);;

let rec dzialanie op lista1 lista2 =
  match (lista1, lista2) with
  | (Element(x, xs), Element(y, ys)) -> (op x y) :: dzialanie op xs ys
  | (Element(x, xs), Koniec) -> (op x 0) :: dzialanie op xs Koniec
  | (Koniec, Element(y, ys)) -> (op 0 y) :: dzialanie op Koniec ys
  | (Koniec, Koniec) -> []
;;

let rec ldzialanie op lista1 lista2 =
  match (lista1, lista2) with
  | (LKoniec, LKoniec) -> LKoniec
  | (LKoniec, LElement(y, ys)) -> LElement(op 0 y, fun () -> ldzialanie op LKoniec (ys ())) 
  | (LElement(x, xs), LKoniec) -> LElement(op x 0, fun () -> ldzialanie op (xs ()) LKoniec) 
  | (LElement(x, xs), LElement(y, ys)) -> LElement(op x y, fun () -> ldzialanie op (xs ()) (ys ())) 
  ;;

let rec stworz_nliste lista =
  match lista with
  | [] -> Koniec
  | head :: tail -> Element(head, stworz_nliste tail)
;;

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
  
dzialanie (fun x y -> x + y) (stworz_nliste [1;2;3]) (stworz_nliste [2;3;4;5]);;
dzialanie (fun x y -> x * y) (stworz_nliste [1;2;3]) (stworz_nliste [2;3;4;5;7]);;
dzialanie (fun x y -> x + y) (stworz_nliste [1;2;3]) (stworz_nliste [4;5;6]);;
dzialanie (fun x y -> x - y) (stworz_nliste [1;2;3]) (stworz_nliste [4;5;6]);;
dzialanie (fun x y -> x * y) (stworz_nliste [1;2;3]) (stworz_nliste [4;5;6]);;
dzialanie (fun x y -> x / y) (stworz_nliste [4;5;6]) (stworz_nliste [1;2;3]);;
ltakeall (ldzialanie (fun x y -> x + y) (stworz_lliste [1;2;3]) (stworz_lliste [2;3;4;5]));;
ltakeall (ldzialanie (fun x y -> x + y) (stworz_lliste [1;2;3]) (stworz_lliste [4;5;6]));;
ltakeall (ldzialanie (fun x y -> x - y) (stworz_lliste [1;2;3]) (stworz_lliste [4;5;6]));;
ltakeall (ldzialanie (fun x y -> x * y) (stworz_lliste [1;2;3]) (stworz_lliste [4;5;6]));;
ltakeall (ldzialanie (fun x y -> x / y) (stworz_lliste [1;2;3]) (stworz_lliste [4;5;6]));;

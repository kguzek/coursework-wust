let rec suma_listy lista = 
  match lista with
    | [] -> 0
    | head::tail -> head + suma_listy tail
;;

let rec filtruj_listy listy suma =
  match listy with
    | [] -> []
    | head::tail ->
        match suma_listy head == suma with
          | true -> head::(filtruj_listy tail suma)
          | false -> (filtruj_listy tail suma)
;;


filtruj_listy [[1;2;3];[2;4];[5;6]] 6;;
filtruj_listy [[10;20];[5;5;5];[1;2;3;4]] 15;;
filtruj_listy [[0;0;0];[1;-1];[2;2;2]] 0;;
filtruj_listy [[];[1];[2;3]] 0;;
filtruj_listy [[-1;-2;-3];[-4;-5];[-6]] (-6);;  
filtruj_listy [[100];[50;50];[25;25;25;25]] 100;;
filtruj_listy [[1;1;1;1;1];[2;2;1];[3;0]] 5;;
filtruj_listy [[]] 10;;
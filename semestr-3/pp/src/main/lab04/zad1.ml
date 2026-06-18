let rec reverse numbers acc = 
  match numbers with 
  | [] -> acc
  | h::t -> reverse t (h::acc)
;;

let podziel_ogon numbers value = 
  let rec podziel_ogon_it numbers greater less divider =
    match numbers with
    | [] -> (reverse greater [], reverse less [])
    | h::t ->
      if h > divider then podziel_ogon_it t (h::greater) less divider
      else if h < divider then podziel_ogon_it t greater (h::less) divider
      else podziel_ogon_it t greater less divider
  in podziel_ogon_it numbers [] [] value
;;

let rec podziel_nie_ogon numbers value = 
  match numbers with
  | [] -> ([], [])
  | h::t ->
      let (greater, less) = podziel_nie_ogon t value in
      match h with
        | _ when h == value -> (greater, less)
        | _ when h < value -> (greater, h::less)
        | _ -> (h::greater, less)
  ;;
;;

podziel_ogon [5;4;3;2;1] 3;;
podziel_nie_ogon [5;4;3;2;1] 3;;
podziel_ogon [3;6;8;9;13] 7;;
podziel_nie_ogon [3;6;8;9;13] 7;;
podziel_ogon [1;2;3;4;5;6] 4;;
podziel_nie_ogon [1;2;3;4;5;6] 4;;
podziel_ogon [1;3;5;7;9] 5;;
podziel_nie_ogon [1;3;5;7;9] 5;;
podziel_ogon [2;4;6;8] 1;;
podziel_nie_ogon [2;4;6;8] 1;;
podziel_ogon [2] 2;;
podziel_nie_ogon [2] 2;;
podziel_ogon [] 10;;
podziel_nie_ogon [] 10;;

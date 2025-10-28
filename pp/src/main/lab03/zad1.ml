let rec podziel numbers = 
  match numbers with
  | [] -> ([], [])
  | h::t ->
      let (evens, odds) = podziel t in
      match h mod 2 with
        | 0 -> (h::evens, odds)
        | 1 -> (evens, h::odds)

podziel [3;6;8;9;13];;
podziel [1;2;3;4;5;6];;
podziel [1;3;5;7;9];;
podziel [2;4;6;8];;
podziel [2];;
podziel [];;

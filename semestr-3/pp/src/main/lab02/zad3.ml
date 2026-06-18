let rec polacz texts separator =
  if texts = [] then ""
  else 
    if List.tl texts = [] then List.hd texts
    else List.hd texts ^ separator ^ polacz (List.tl texts) separator;;

polacz ["To"; "jest"; "napis"] "-";;
polacz ["Ala"; "ma"; "kota"] " ";;
polacz ["OCaml"; "to"; "fajny"; "jezyk"] ", ";;
polacz ["Jednoelementowy"] " ";;
polacz [] ", ";;

let rec szesnastkowo_rev liczba: int list =
  match liczba with
    | 0 -> []
    | _ -> 
    let cal = liczba / 16 in
    let reszta = liczba - cal * 16 in
    reszta::(szesnastkowo_rev cal)
  ;;

let szesnastkowo liczba =
  List.rev(szesnastkowo_rev liczba)
;;

szesnastkowo 31;;
szesnastkowo 1;;
szesnastkowo 16;;
szesnastkowo 17;;
szesnastkowo 256;;
szesnastkowo (-31);;
szesnastkowo (-1);;
szesnastkowo (-16);;
szesnastkowo (-17);;
szesnastkowo (-256);;

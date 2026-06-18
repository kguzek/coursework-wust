let rec krotki napisy =
  match napisy with
   | [] -> []
   | (a, b, c, d)::tail -> (a ^ b ^ c ^ d)::(krotki tail)
;;

  krotki [("ala","ma","kot","a");("kot","nie","ma","ali")];;
  krotki [("test","slowo","krotka","czwarta");("1","2","3","4")];;
  krotki [("","slowo","","sdf");("1","","3","")];;
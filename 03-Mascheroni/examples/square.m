to construct circleheight circle a, ray h given point A, point B do
  define circle[A, B] as a
  with circle[B, A] as b and circle[a ∩0 b, A] as e and circle[a ∩1 e, A] as f and e ∩1 f as H do
      define ray[A, H] as h
  done
  show
done

to construct cdvertices point C, point D given point A, point B do
  with circleheight(A, B) as a, h do
    define h ∩ a as D
    define circle[B, A] ∩1 circle[D, A] as C
  done
  show
done

to construct main segment a, segment b, segment c, segment d given point A, point B do
  define cdvertices(A, B) as C, D
  define segment[A, B] as a
  define segment[B, C] as b
  define segment[C, D] as c
  define segment[D, A] as d
  show
done

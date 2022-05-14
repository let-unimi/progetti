to construct transport circle c given point A, point B, point C do
  with circle[A, B] ∩1 circle[B, A] as D and
       line[D, B] as r and line[D, A] as s and
       r ∩1 circle[B, C] as E and
       s ∩0 circle[D, E] as F do
    define circle[A, F] as c
  done
  show
done

to construct main point Q, line p given point A, point B, point P do
  with circle[A, P] ∩1 line[A, B] as R and
       transport(A, P, R) as c do
  define circle[P, A] ∩1 c as Q 
  define line[P, Q] as p
  done
  show
done
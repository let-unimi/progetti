to construct main circle c given point A, point B, point C do
  define circle[A, B] ∩1 circle[B, A] as D 
  define line[D, B] as r
  define line[D, A] as s
  define r ∩1 circle[B, C] as E
  define s ∩0 circle[D, E] as F
  define circle[A, F] as c
  show
done
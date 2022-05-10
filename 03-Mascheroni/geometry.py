from operator import itemgetter
from functools import partial

from typing import Mapping, Union, Optional, Tuple, Set

import drawSvg as draw

from sympy.geometry.entity import GeometryEntity
from sympy import Point, Line, Ray, Circle, Segment, Polygon, atan2, pi

class CirclePoint(Circle):
  """Un cerchio definito dal centro e da un punto sulla circonferenza.
  
  Args:
    center: il centro della circonferenza
    point: un punto sulla circonferenza
  """
  def __new__(cls, center, point):
    return Circle.__new__(cls, center, center.distance(point))
  def __init__(self, center: Point, point: Point):
    self.point = point
  def __repr__(self):
    return f'CirclePoint({self.center}, {self.point})'

def intersection(first: GeometryEntity, second: GeometryEntity, which_one: Optional[int] = None) -> Union[Point, Tuple[Point, Point]]:
  """Restituisce in modo ordinato i punti di una intersezione tra enti
  geometrici.

  Args:
    first: il primo ente,
    second: il secondo ente.
    which_one: se diverso da :samp:`None`, 
      quale dei due punti tornare (in caso l'intersezione ne contenga due).

  Returns:
    I punti che costituiscono l'intersezione.
  """
  intersection = first.intersect(second)
  if len(intersection) not in {1, 2}:
    raise ValueError(f'One, or two intersections where expected, found {len(intersection)} instead')

  def angle(c, p):
    p = p - c
    a = atan2(p.y, p.x)
    return a if a >= 0 else 2 * pi + a

  if len(intersection) == 1:
    if which_one is not None: raise ValueError(f'There is just one intersection, cannot return the {which_one}th one')
    e = next(iter(intersection))
    if not isinstance(e, Point): raise ValueError(f'Intersection {e} is not a point')
    return e
  else: # 2 points
    e0, e1 = intersection
    if not isinstance(e0, Point): raise ValueError(f'Intersection {e0} is not a point')
    if not isinstance(e1, Point): raise ValueError(f'Intersection {e1} is not a point')
    if isinstance(first, (Segment, Line, Ray)):
      d0, d1 = first.p1.distance(e0), first.p1.distance(e1)
      if d0 > d1: e0, e1 = e1, e0
    elif isinstance(first, CirclePoint):
      ap = angle(first.center, first.point)
      a0 = angle(first.center, e0)
      a1 = angle(first.center, e1)
      if a0 > a1: 
        a0, a1 = a1, a0
        e0, e1 = e1, e0
      if a0 < ap <= a1: # first must be < not <=
        e0, e1 = e1, e0
    if which_one is None:
      return e0, e1
    else:
      return e0 if which_one == 0 else e1

TYPENAME2MAKER = {
  'point': Point,
  'segment': Segment,
  'ray': Ray,
  'line': Line,
  'circle': CirclePoint,
  'intersection': intersection,
  'intersection0': partial(intersection, whichone = 0),
  'intersection1': partial(intersection, whichone = 1)
}

def make_entity(type_name: str, first: Point, second: Point) -> Union[Point, Segment, Ray, Line, CirclePoint]:
  """Costruisce un ente dato il nome del suo tipo in Mascheroni e i due punti
  che lo caratterizzano.
  
  Args:
    type_name: il nome del tipo (a scelta tra: :samp:`segment`,
      :samp:`ray`, :samp:`line`, :samp:`circle`), 
    first: il primo punto che
      definisce l'ente, 
    second: il secondo punto 
      che definisce l'ente.

  Returns:
    L'ente creato a partire dai punti dati.
  """
  try:
    return TYPENAME2MAKER[type_name](first, second)
  except KeyError:
    raise ValueError(f'Name {type_name} unknown')

def isnamedinstance(entity: GeometryEntity, type_name: Union[str, Tuple[str]]) -> bool:
  """Versione di :func:`isinstance` basata sui nomi di tipo di Mascheroni.
  
  Args:
    entity: un ente di cui si 
      intende valutare il tipo,
    type_name: un nome di tipo, o una tupla di nomi di tipo (a scelta 
      tra: :samp:`point`, :samp:`segment`, :samp:`ray`, :samp:`line`, :samp:`circle`).
  """
  try:
    if isinstance(type_name, tuple):
      return isinstance(entity, tuple(TYPENAME2MAKER[n] for n in type_name))
    else:
      return isinstance(entity, TYPENAME2MAKER[type_name])
  except KeyError:
    raise ValueError('One of the type name(s) is unknown')

def to_svg(name2entities : Mapping[str, object], given: Set[str] = None, constructed: Set[str] = None, show_names: bool = False) -> str:
  """Restituisce una rappresentazione SVG (in forma di :obj:`str`) degli enti dati.

  Args:
    name2entities: una mappa da nomi di enti a enti,
    given: gli enti da visualizzare come dati,
    constructed: gli enti da visualizzare come costruiti,
    show_names: se :samp:`True` la visualizzazione includerà i nomi dei punti.
  """
  if given is None: given = set()
  if constructed is None: constructed = set()

  name2entities = {n: e for n, e in name2entities.items() if isnamedinstance(e, ('point', 'segment', 'ray', 'line', 'circle'))}
  if not len(name2entities): return

  bounds = list(map(lambda _: _.bounds, name2entities.values()))
  xmin = min(map(itemgetter(0), bounds))
  ymin = min(map(itemgetter(1), bounds))
  xmax = max(map(itemgetter(2), bounds))
  ymax = max(map(itemgetter(3), bounds))

  if xmin == xmax:
    xmin -= 25
    xmax += 25
  if ymin == ymax:
    ymin -= 25
    ymax += 25

  width = (xmax - xmin) * 1.2
  height =(ymax - ymin) * 1.2

  bbox = Polygon(
    Point(xmin - .1 * width, ymin - .1 * height),
    Point(xmax + .1 * width, ymin - .1 * height),
    Point(xmax + .1 * width, ymax + .1 * height),
    Point(xmin - .1 * width, ymax + .1 * height)
  )

  origin = float(xmin - .1 * width), float(ymin - .1 * height)
  
  d = draw.Drawing(float(width), float(height), origin = origin, displayInline = False)
  d.append(draw.Rectangle(
    origin[0], origin[1],
    float(width), float(height),
    fill = 'lightyellow'
  ))
  for name, entity in name2entities.items():
    if name in given: color = 'red'
    elif name in constructed: color = 'green'
    else: color = 'black'
    if isinstance(entity, Point):
      p = draw.Circle(float(entity.x), float(entity.y), 3, fill = color)
      if show_names: d.append(draw.Text(name, 14, float(entity.x) - 14, float(entity.y) - 14))
    elif isinstance(entity, Circle):
      p = draw.Circle(float(entity.center.x), float(entity.center.y), float(entity.radius), fill = 'transparent', stroke = color)
    else:
      if isinstance(entity, Line): entity = Segment(*bbox.intersect(entity))
      elif isinstance(entity, Ray): entity = Segment(entity.p1, *bbox.intersect(entity))
      p = draw.Line(float(entity.p1.x), float(entity.p1.y), float(entity.p2.x), float(entity.p2.y), stroke = color)
    d.append(p)
  return d.asSvg()

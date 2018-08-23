from hask.lang import deriving, data, d, Show, Eq

Unit, Star = data.Unit == d.Star & deriving(Show, Eq)
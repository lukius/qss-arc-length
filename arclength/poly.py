from math import sqrt, log


class PolyArcLength(object):
    
    # Arc length calculation for two-dimensional parametric curves of the
    # form
    # x(t) = a_0 + a_1 * t + ... + a_k * t^k
    # y(t) = b_0 + b_1 * t + ... + b_k * t^k
    
    # As apparently there is no closed form solution for the indefinite  
    # integral that arises when k > 2, we currently support polynomials
    # of degree at most 2.   
    
    @classmethod
    def for_polys(cls, x_t, y_t):
        # TODO: only valid for polynomials of degree < 3.
        if len(x_t) < 3 and len(y_t) < 3:
            subclass = Poly1ArcLength
        elif x_t[2] == 0 and y_t[2] == 0:
            subclass = Poly1ArcLength
            x_t = x_t[:2]
            y_t = y_t[:2]
        else:
            subclass = Poly2ArcLength
        return subclass(x_t, y_t)

    def _eval_integral(self, t):
        # This method evaluates in t the indefinite integral of
        # sqrt(x'(z)^2 + y'(z)^2) dz
        raise NotImplementedError

    def value(self, t0, t1):
        # Returns the arc length of the parametric curve (x(t), y(t)) between
        # t0 and t1. 
        if t1 < t0:
            t0, t1 = t1, t0

        return self._eval_integral(t1) - self._eval_integral(t0)
            
    
class Poly1ArcLength(PolyArcLength):
    
    def __init__(self, x_t, y_t):
        self.a0, self.a1 = x_t
        self.b0, self.b1 = y_t
        
    def _eval_integral(self, t):
        return t * sqrt(self.a1*self.a1 + self.b1*self.b1)


class Poly2ArcLength(PolyArcLength):

    def __init__(self, x_t, y_t):
        self.a0, self.a1, self.a2 = x_t
        self.b0, self.b1, self.b2 = y_t

    def _eval_integral(self, t):
        tsq, a1sq, a2sq, b2sq = t*t, self.a1*self.a1, self.a2*self.a2, self.b2*self.b2
        
        bssq = (2*self.b2*t + self.b1)**2
        ab2sq = a2sq + b2sq
        
        s11 = 2*a2sq*t + self.a1*self.a2 + 2*b2sq*t + self.b1*self.b2
        s12 = sqrt(4*a2sq*tsq + 4*self.a1*self.a2*t + a1sq + bssq)
        s1 = (s11 * s12) / (4*ab2sq)

        s21 = (self.a2*self.b1 - self.a1*self.b2)**2 / (4*ab2sq**1.5)
        s22 = sqrt(ab2sq) * s12 + s11
        s2 = s21 * log(s22)

        return s1 + s2
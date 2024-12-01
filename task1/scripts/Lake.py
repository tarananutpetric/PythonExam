class Lake:
    """
    Class that describes a lake

    :param e: energy coefficient [MWh/m3]
    :param Vmin: minimal lake volume [m3]
    :param Vmax: maximal lake volume [m3]
    :param Qmin: minimal flow on turbine [m3/s]
    :param Qmax: maximal flow on turbine [m3/s]
    :param coeff: desired % of lake level
    """

    def __init__(self, e, Vmin, Vmax, Qmin, Qmax, coeff):
        self.e = e
        self.Vmin = Vmin
        self._Vmax = Vmax
        self.Qmin = Qmin
        self.Qmax = Qmax
        self.coeff = coeff

    @property
    def Vmax(self):
        """
        Returns Vmax.
        """
        return self._Vmax

    @property
    def V0(self):
        """
        Returns desired % of Vmax.
        """
        return self.coeff * self.Vmax

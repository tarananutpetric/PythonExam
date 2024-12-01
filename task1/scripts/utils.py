import pyomo.environ as pyo

# plotting colors definitions
colourON = "mediumseagreen"
colourOFF = "indianred"


def flowOptimisation(Lake, data):
    """
    Creates a Pyomo model and defines the mathematical formalism for desired optimisation.
    Performs optimisation and returns model object.

    :param Lake: Lake object with members e,Vmin,Vmax,Qmin,Qmax
    :param data: pandas dataframe with columns price, Inflow
    :returns: Pyomo model
    """
    # Create a model
    model = pyo.ConcreteModel()

    # Index set
    N = range(len(data))  # 1h steps for 1 yr equivalent
    model.N = pyo.Set(initialize=N)

    # Parameters
    model.e = pyo.Param(initialize=Lake.e)
    model.P = pyo.Param(N, initialize=data["Price"].to_dict())
    model.A = pyo.Param(N, initialize=data["Inflow"].to_dict())

    # Variables
    model.q = pyo.Var(N, bounds=(Lake.Qmin, Lake.Qmax))
    model.v = pyo.Var(N, bounds=(Lake.Vmin, Lake.Vmax))
    model.d = pyo.Var(N, domain=pyo.NonNegativeIntegers)

    # Objective function
    model.obj = pyo.Objective(
        expr=model.e * sum(model.q[i] * 3600 * model.P[i] for i in N),
        sense=pyo.maximize,
    )

    # Constraints
    model.v[0].fix(Lake.V0)

    def volume_condition(model, i):
        if i == 0:
            return pyo.Constraint.Skip  # Skip for the first index
        return (
            model.v[i]
            == model.v[i - 1]
            - model.q[i - 1] * 3600
            - model.d[i - 1] * 3600
            + model.A[i - 1] * 3600
        )  # assume d(i) has units m3/s

    model.balance = pyo.Constraint(model.N, rule=volume_condition)

    # v(TF) can be smaller than v(TF+1)=V0 maximally by A(TF). No maximum condition as d(i) can be arbitrarily big
    final_volume_min = Lake.V0 - data.loc[data["Month"] == 12, "Inflow"].iloc[0] * 3600
    model.final_condition = pyo.Constraint(expr=model.v[8759] >= final_volume_min)

    # Specify the solver
    solver = pyo.SolverFactory("cbc")

    # Solve the problem
    result = solver.solve(model)
    print("Status:", result.solver.status)
    print("Termination Condition:", result.solver.termination_condition)

    return model

#include "Evaluator.hpp"

using namespace LcVRPContest;

Evaluator::Evaluator(const ProblemData& problem_data, const int num_groups)
  : problem_data_(problem_data), num_groups_(num_groups)
{
  num_customers_ = problem_data_.GetNumCustomers();
}

double Evaluator::Evaluate(const vector<int>* solution) const
{
  if (solution == nullptr)
  {
    return PENALTY_INVALID_SOLUTION;
  }
  return Evaluate(*solution);
}

double Evaluator::Evaluate(const vector<int>& solution) const
{
  if (!IsValidSolution(solution))
  {
    return PENALTY_INVALID_SOLUTION;
  }

  vector<vector<int>> routes;
  BuildRoutes(solution, routes);

  double total_cost = 0.0;
  double capacity_penalty = 0.0;
  double distance_penalty = 0.0;

  for (int i = 0; i < static_cast<int>(routes.size()); ++i)
  {
    const vector<int>& route = routes[i];

    if (route.empty())
    {
      continue;
    }

    const double route_distance = CalculateTotalDistance(route);
    if (route_distance < 0.0)
    {
      return PENALTY_INVALID_SOLUTION;
    }
    total_cost += route_distance;

    if (!CheckCapacityConstraint(route))
    {
      const double demand = CalculateRouteDemand(route);
      capacity_penalty += (demand - problem_data_.GetCapacity()) * 100.0;
    }

    if (problem_data_.HasDistanceConstraint() &&
      !CheckDistanceConstraint(route))
    {
      distance_penalty +=
        (route_distance - problem_data_.GetDistance()) * 100.0;
    }
  }

  const double fitness =
    1000000.0 - (total_cost + capacity_penalty + distance_penalty);

  return fitness;
}

double Evaluator::Evaluate(const int* solution) const
{
  if (solution == nullptr)
  {
    return PENALTY_INVALID_SOLUTION;
  }

  vector<int> solution_vec(num_customers_);
  for (int i = 0; i < num_customers_; ++i)
  {
    solution_vec[i] = solution[i];
  }

  return Evaluate(solution_vec);
}

double Evaluator::CalculateRouteCost(const vector<int>& route) const
{
  return CalculateTotalDistance(route);
}

bool Evaluator::IsValidSolution(const vector<int>& grouping) const
{
  if (static_cast<int>(grouping.size()) != num_customers_)
  {
    return false;
  }

  for (int i = 0; i < static_cast<int>(grouping.size()); ++i)
  {
    if (grouping[i] < 0 || grouping[i] >= num_groups_)
    {
      return false;
    }
  }

  return true;
}

bool Evaluator::ValidateConstraints() const
{
  const int dimension = problem_data_.GetDimension();
  const int depot = problem_data_.GetDepot();
  const int capacity = problem_data_.GetCapacity();
  const vector<int>& demands = problem_data_.GetDemands();

  if (dimension < 2)
  {
    return false;
  }

  if (depot < 1 || depot > dimension)
  {
    return false;
  }

  if (capacity <= 0)
  {
    return false;
  }

  if (static_cast<int>(demands.size()) != dimension)
  {
    return false;
  }

  for (int i = 0; i < static_cast<int>(demands.size()); ++i)
  {
    if (demands[i] < 0)
    {
      return false;
    }
  }

  const int depot_index = depot - 1;
  if (depot_index >= 0 && depot_index < static_cast<int>(demands.size()))
  {
    if (demands[depot_index] != 0)
    {
      return false;
    }
  }

  if (problem_data_.HasDistanceConstraint())
  {
    if (double max_dist = problem_data_.GetDistance(); max_dist <= 0.0)
    {
      return false;
    }
  }

  double total_demand = 0.0;
  for (int i = 0; i < dimension; ++i)
  {
    if (i != depot_index)
    {
      total_demand += demands[i];
    }
  }

  if (double min_vehicles_needed = total_demand / capacity; min_vehicles_needed > num_groups_)
  {
    return false;
  }

  if (string edge_type = problem_data_.GetEdgeWeightType(); edge_type == "EUC_2D")
  {
    if (const vector<Coordinate>& coords = problem_data_.GetCoordinates(); static_cast<int>(coords.size()) != dimension)
    {
      return false;
    }
  }
  else if (edge_type == "EXPLICIT")
  {
    if (const vector<vector<double>>& weights = problem_data_.GetEdgeWeights();
      static_cast<int>(weights.size()) != dimension)
    {
      return false;
    }
  }
  else
  {
    return false;
  }

  return true;
}

void Evaluator::BuildRoutes(const vector<int>& grouping, vector<vector<int>>& routes) const
{
  routes.resize(num_groups_);

  for (int customer = 0; customer < static_cast<int>(grouping.size()); ++customer)
  {
    int group = grouping[customer];
    // customer 0 maps to node 1 (depot is node 0/1 depending on indexing)
    routes[group].push_back(customer + 1);
  }
}

bool Evaluator::CheckCapacityConstraint(const vector<int>& route) const
{
  double demand = CalculateRouteDemand(route);
  return demand <= problem_data_.GetCapacity();
}

bool Evaluator::CheckDistanceConstraint(const vector<int>& route) const
{
  if (!problem_data_.HasDistanceConstraint())
  {
    return true;
  }

  double distance = CalculateTotalDistance(route);
  return distance <= problem_data_.GetDistance();
}

double Evaluator::CalculateRouteDemand(const vector<int>& route) const
{
  double total_demand = 0.0;
  const vector<int>& demands = problem_data_.GetDemands();

  for (int i = 0; i < static_cast<int>(route.size()); ++i)
  {
    int customer = route[i];
    if (IsValidCustomerIndex(customer))
    {
      total_demand += demands[customer];
    }
  }

  return total_demand;
}

double Evaluator::CalculateTotalDistance(const vector<int>& route) const
{
  if (route.empty())
  {
    return 0.0;
  }

  double total_distance = 0.0;
  int depot = problem_data_.GetDepot();

  if (!IsValidCustomerIndex(route[0]))
  {
    return WRONG_VAL;
  }
  total_distance += problem_data_.CalculateDistance(depot, route[0]);

  for (int i = 0; i < static_cast<int>(route.size()) - 1; ++i)
  {
    if (!IsValidCustomerIndex(route[i]) ||
      !IsValidCustomerIndex(route[i + 1]))
    {
      return WRONG_VAL;
    }
    double dist = problem_data_.CalculateDistance(route[i], route[i + 1]);
    if (dist < 0.0)
    {
      return WRONG_VAL;
    }
    total_distance += dist;
  }

  if (!IsValidCustomerIndex(route[route.size() - 1]))
  {
    return WRONG_VAL;
  }
  total_distance +=
    problem_data_.CalculateDistance(route[route.size() - 1], depot);

  return total_distance;
}

bool Evaluator::IsValidCustomerIndex(int customer_id) const
{
  return customer_id >= 0 && customer_id < problem_data_.GetDimension();
}
